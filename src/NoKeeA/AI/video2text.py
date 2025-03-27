import hashlib
import json
import math
import numbers
import os.path
import subprocess
from pathlib import Path
import whisper
import cv2
import pytesseract
from transformers import Blip2Processor, Blip2ForConditionalGeneration, TextStreamer
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import numpy as np
import torch
from openai import OpenAI
from huggingface_hub import snapshot_download

import streamlit as st
from typing_extensions import TypedDict


class Description(TypedDict):
    path: str
    frame_number: int
    text: str
    description: str


class ExtractedText(TypedDict):
    start: numbers.Number
    end: numbers.Number
    text: str
    frames: list[Description]


blip_processor = None
blip_model = None

deepseek_tokenizer = None
deepseek_model = None


def load_image_description_model():
    global blip_model, blip_processor
    if blip_processor is None or blip_model is None:
        blip_processor = Blip2Processor.from_pretrained("blip2_model")
        blip_model = Blip2ForConditionalGeneration.from_pretrained(
            "blip2_model")
        return "✅ Bilderkennung geladen"
    return "⏭️ Bilderkennung geladen"


def load_summarizer_model():
    snapshot_download(repo_id="deepseek-ai/DeepSeek-V2-Lite",
                      local_dir="deepseek_model")

    global deepseek_tokenizer, deepseek_model
    if deepseek_tokenizer is None or deepseek_model is None:
        deepseek_tokenizer = AutoTokenizer.from_pretrained(
            "deepseek_model", trust_remote_code=False)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        deepseek_model = AutoModelForCausalLM.from_pretrained("deepseek_model", torch_dtype=torch_dtype,
                                                              trust_remote_code=True, device_map="auto")
        return "✅ LLM geladen"
    return "⏭️ LLM geladen"


def match_frames_with_audio(
        video_frames: list[Description],
        video_text: list[ExtractedText]) -> list[ExtractedText]:
    for text_segment in video_text:
        start = math.ceil(text_segment["start"])
        end = math.floor(text_segment["end"])

        text_segment["frames"] = []
        for frame in video_frames:
            if start <= frame["frame_number"] <= end:
                text_segment["frames"].append(frame)
    return video_text


def video2text(video):
    path = None
    try:
        gen = save_video(video)
        while True:
            yield next(gen)
    except StopIteration as e:
        path = e.value

    if not os.path.isfile(f"{path}.txt"):
        video_text = None
        try:
            gen = extract_audio_convert2text(path)
            while True:
                yield next(gen)
        except StopIteration as e:
            video_text = e.value["segments"]

        video_frames = []
        try:
            gen = extract_frames_convert2text(path)
            while True:
                yield next(gen)
        except StopIteration as e:
            video_frames = e.value

        try:
            gen = text_recognition(video_frames)
            while True:
                yield next(gen)
        except StopIteration as e:
            video_frames = e.value

        try:
            gen = describe_image(video_frames)
            while True:
                yield next(gen)
        except StopIteration as e:
            video_frames = e.value

        video_text = match_frames_with_audio(video_frames, video_text)

        save_video_description(video_text, f"{path}.txt")

    else:
        with open(f"{path}.txt") as f:
            video_text = json.load(f)
        yield "⏭️ Informationen geladen"

    prompt = build_prompt(video_text)

    try:
        gen = summarize_with_deepseek(prompt)
        while True:
            yield next(gen)
    except StopIteration as e:
        return e.value

    return "Failed"


def save_video(video):
    Path("tmp").mkdir(parents=True, exist_ok=True)
    extinction = video.type.replace("/", ".")
    path = f"tmp/{hashlib.sha3_256(video.read()).hexdigest()}.{extinction}"

    with open(path, "wb") as f:
        f.write(video.getbuffer())
    yield "✅ Datei gespeichert"

    return path


def save_video_description(video_text, path):
    with open(path, 'w+') as f:
        json.dump(video_text, f)


def image_difference(img1, img2):
    diff = cv2.absdiff(img1, img2)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    non_zero_count = np.count_nonzero(diff_gray)
    total_pixels = diff_gray.size
    return (non_zero_count / total_pixels) * 100


def extract_frames_convert2text(path: str, frame_rate=1, threshold=20):
    frames_folder = f"{path}.frames"
    Path(frames_folder).mkdir(parents=True, exist_ok=True)

    st.session_state["video2text_progress_bar_text"] = "Frames werden extrahiert."

    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = math.floor(frame_count / fps)
    frame_interval = max(1, fps // frame_rate)
    count = 0
    frame_number = 0
    saved_frames = 0
    frames = []
    prev_frame = None

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        if count % frame_interval == 0:
            if prev_frame is None or image_difference(prev_frame, frame) > threshold:
                frame_path = f"{frames_folder}/frame_{frame_number:04d}.jpg"
                cv2.imwrite(frame_path, frame)
                frames.append({
                    "path": frame_path,
                    "frame_number": frame_number,
                })
                saved_frames += 1
                prev_frame = frame
            frame_number += 1
            yield min(1, frame_number / duration)
        count += 1
    yield f"✅ {saved_frames}/{frame_number} Frames extrahiert"

    cap.release()
    return frames


def extract_audio_convert2text(path: str):
    command = ["ffmpeg", "-i", path, "-q:a",
               "0", "-map", "a", f"{path}.wav", "-y"]
    ffmpeg_result = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ffmpeg_result.returncode != 0:
        raise Exception("ffmpeg failed")
    yield "✅ Audio extrahiert"

    # Oder "medium", "large" für bessere Ergebnisse
    model = whisper.load_model("base")
    result = model.transcribe(f"{path}.wav")

    yield "✅ Audio zu Text konvertiert"

    return result


def text_recognition(images: list[Description]) -> list[Description]:
    st.session_state["video2text_progress_bar_text"] = "Texte werden extrahiert."

    i = 0
    for image_path in images:
        image = Image.open(image_path["path"])
        text = pytesseract.image_to_string(image)
        image_path["text"] = text
        i += 1
        yield i / len(images)
    yield "✅ Text aus Frames extrahiert"
    return images


def describe_image(images: list[Description]) -> list[Description]:
    yield load_image_description_model()

    st.session_state["video2text_progress_bar_text"] = "Frames werden beschreiben. Das kann einige Zeit dauern."

    i = 0
    for image_date in images:
        image = Image.open(image_date["path"]).convert("RGB")
        inputs = blip_processor(image, return_tensors="pt")

        output = blip_model.generate(**inputs, max_length=50)
        description = blip_processor.decode(
            output[0], skip_special_tokens=True)
        image_date["description"] = description.strip()
        i += 1
        yield i / len(images)

    yield "✅ Frames beschrieben"

    return images


def summarize_with_deepseek(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is not None:
        return use_openai(api_key, prompt)

    yield load_summarizer_model()

    inputs = deepseek_tokenizer(prompt, return_tensors="pt", padding=True)
    streamer = TextStreamer(deepseek_tokenizer)
    output = deepseek_model.generate(
        **inputs, streamer=streamer, temperature=0.7, max_new_tokens=500)

    print(output)

    return deepseek_tokenizer.decode(output[0], skip_special_tokens=True)


def use_openai(api_key: str, prompt: str) -> str:
    client = OpenAI(
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


def build_prompt(video_description: list[ExtractedText]):
    prompt = """I want a summary of a video for my notes. All information from the video should be summarized.

The information should be divided into sections and described in detail using bullet points.

The way the information was extracted from the video is inaccurate. Give more weight to the spoken text and use the
frame descriptions only as a support. Different languages may be used.

Context: You are a note-taking expert and want to summarize a video. For this purpose, the spoken text in the video
was transcribed and made available to you. A frame was extracted every second from the video. The frames were only
retained if there was a significant change (more than 20% change). An AI recognized the text on the frame. An AI then
 described what can be seen on the frame.

The video follows
------------------
"""

    for segment in video_description:
        if len(segment["frames"]) > 0:
            prompt += "\n\nThe video shows:\n"
            for frame in segment["frames"]:
                prompt += f"* Text on screen: {frame['text']}\n"
                prompt += f"* Description of szene: {frame['description']}\n"
            prompt += "Spoken text: "
        prompt += segment["text"]

    return prompt
