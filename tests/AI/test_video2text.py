import numbers
import os
import hashlib
import shutil
import json
from pathlib import Path
from types import GeneratorType

import pytest
from unittest.mock import patch, MagicMock

from NoKeeA.AI.video2text import (
    save_video,
    extract_audio_convert2text,
    extract_frames_convert2text,
    text_recognition,
    describe_image,
    build_prompt,
    video2text,
)

import streamlit as st

st.session_state.clear()

ASSETS_DIR = Path("tests/assets")
TMP_DIR = Path("tmp")


@pytest.fixture(scope="module", autouse=True)
def clean_tmp():
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(TMP_DIR)


def test_save_video():
    class DummyVideo:
        def __init__(self, path):
            self._data = Path(path).read_bytes()
            self.type = "video/mp4"

        def read(self): return self._data

        def getbuffer(self): return self._data

    dummy_video = DummyVideo(ASSETS_DIR / "test_video.mp4")
    gen = save_video(dummy_video)
    assert isinstance(gen, GeneratorType)
    msg = next(gen)
    assert msg == "✅ Datei gespeichert"
    try:
        path = gen.send(None)
    except StopIteration as e:
        path = e.value
    assert os.path.isfile(path)
    expected_hash = hashlib.sha3_256(dummy_video.read()).hexdigest()
    assert expected_hash in path


def test_extract_audio_convert2text():
    video_path = TMP_DIR / os.listdir(TMP_DIR)[0]  # saved mp4
    gen = extract_audio_convert2text(str(video_path))
    assert next(gen) == "✅ Audio extrahiert"
    assert next(gen) == "✅ Audio zu Text konvertiert"
    try:
        result = gen.send(None)
    except StopIteration as e:
        result = e.value
    assert isinstance(result, dict)
    assert "segments" in result


def test_extract_frames_convert2text():
    video_path = TMP_DIR / os.listdir(TMP_DIR)[0]
    gen = extract_frames_convert2text(str(video_path))
    frames = []
    for step in gen:
        if isinstance(step, str) and step.startswith("✅"):
            assert "Frames extrahiert" in step
        elif isinstance(step, float):
            assert 0 <= step <= 1
        elif isinstance(step, list):
            frames = step
    assert isinstance(frames, list)
    assert all("path" in f and "frame_number" in f for f in frames)
    # Vergleiche gegen erwartete Dateien
    extracted_files = os.listdir(str(video_path) + ".frames")
    assert all(f in extracted_files for f in ["frame_0000.jpg"])


def test_text_recognition_known_image():
    test_image = ASSETS_DIR / "text_frame.png"
    data = [{"path": str(test_image), "frame_number": 0}]
    gen = text_recognition(data)
    try:
        while True:
            step = next(gen)
            if isinstance(step, numbers.Number):
                assert 0 <= step <= 1
            elif isinstance(step, str):
                assert step.startswith("✅")
            else:
                raise NotImplementedError(f"Unknown step type: {step}")
    except StopIteration as e:
        result = e.value
    print(result)
    assert "text" in result[0]
    assert "Noisy,image\nto test\nTesseract OCR" in result[0]["text"]


def test_describe_image_does_not_crash():
    test_image = ASSETS_DIR / "sample_frame.jpg"
    data = [{"path": str(test_image), "frame_number": 0, "text": "Test"}]

    with patch("NoKeeA.AI.video2text.load_image_description_model", return_value="✅ Bilderkennung geladen"):
        with patch("NoKeeA.AI.video2text.blip_processor") as mock_proc, \
                patch("NoKeeA.AI.video2text.blip_model") as mock_model:

            mock_proc.return_value = {"pixel_values": MagicMock()}
            mock_model.generate.return_value = [[1, 2, 3]]
            mock_proc.decode.return_value = "Eine Szene mit Menschen."

            gen = describe_image(data)
            try:
                while True:
                    step = next(gen)
                    if isinstance(step, numbers.Number):
                        assert 0 <= step <= 1
                    elif isinstance(step, str):
                        assert step.startswith("✅")
                    else:
                        raise NotImplementedError(f"Unknown step type: {step}")
            except StopIteration as e:
                result = e.value
            assert len(result) == 1
            assert "description" in result[0]
            print(f"description: {result[0]['description']}")


def test_prompt_building():
    video_desc = [
        {
            "start": 0, "end": 2, "text": "Hallo und willkommen!",
            "frames": [
                {"text": "Intro", "description": "Ein Logo wird gezeigt"}
            ]
        },
        {
            "start": 3, "end": 5, "text": "Das ist das Hauptthema",
            "frames": []
        }
    ]

    prompt = build_prompt(video_desc)
    assert isinstance(prompt, str)
    assert "Hallo und willkommen!" in prompt
    assert "Das ist das Hauptthema" in prompt
    assert "* Text on screen: Intro" in prompt
    assert "* Description of szene: Ein Logo wird gezeigt" in prompt


@patch("NoKeeA.AI.video2text.OpenAI")
def test_use_openai_mocked(mock_openai):
    from NoKeeA.AI.video2text import use_openai

    # Setup: Simuliere OpenAI-Client und Rückgabe
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="Das ist ein Test."))]
    mock_client.chat.completions.create.return_value = mock_completion

    response = use_openai("test-key", "Sag etwas Nettes.")

    # Assertions
    assert isinstance(response, str)
    assert "Test" in response
    mock_openai.assert_called_once_with(api_key="test-key")
    mock_client.chat.completions.create.assert_called_once()


def test_video2text_end_to_end(monkeypatch):
    # ---- Vorbereitung ----
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    test_video_path = Path("tests/assets/test_video.mp4")
    video_data = test_video_path.read_bytes()

    class DummyVideo:
        def __init__(self, data):
            self._data = data
            self.type = "video/mp4"

        def read(self): return self._data

        def getbuffer(self): return self._data

    fake_video = DummyVideo(video_data)

    # ---- Mock für OpenAI ----
    with patch("NoKeeA.AI.video2text.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(
                content="Dies ist eine Zusammenfassung des Videos."))
        ]
        mock_client.chat.completions.create.return_value = mock_completion

        # ---- Generator durchlaufen ----
        gen = video2text(fake_video)

        results = []
        try:
            while True:
                step = next(gen)
                print(f"step: {step}")
                results.append(step)
        except StopIteration as e:
            result = e.value
            results.append(result)

    print(results)
    # ---- Assertions ----
    # Mindestens ein Fortschrittswert und mindestens eine Success-Nachricht
    assert any(isinstance(x, str) and x.startswith("✅") for x in results)
    assert any(isinstance(x, float) and 0 <= x <= 1 for x in results)
    assert "Dies ist eine Zusammenfassung des Videos." in results[-1]

    # ---- Pfad ermitteln ----
    expected_hash = fake_video.read()
    hash_hex = f"{os.path.join('tmp', os.path.splitext(hashlib.sha3_256(expected_hash).hexdigest())[0])}"
    output_txt = Path(f"{hash_hex}.video.mp4.txt")

    assert output_txt.exists()

    with open(output_txt, "r") as f:
        video_desc = json.load(f)
    assert isinstance(video_desc, list)
    assert len(video_desc) > 0
    assert "text" in video_desc[0]
