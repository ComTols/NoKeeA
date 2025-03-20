import sys
import time

import streamlit as st


def ai_functions():
    st.subheader("🤖 AI Features")
    video2text()
    text2text()


def video2text():
    if "show_video2text_uploader" not in st.session_state:
        st.session_state["show_video2text_uploader"] = False

    if st.button("🎞️ Video2Text"):
        st.session_state["show_video2text_uploader"] = not st.session_state["show_video2text_uploader"]

    if st.session_state["show_video2text_uploader"]:
        with st.container():
            st.write(
                "Wähle ein Video aus, das von der KI zusammengefasst wird. " +
                "Die Informationen werden direkt in die Notiz eingefügt.")
            st.session_state["video2text_file_content"] = st.file_uploader(
                "Wähle ein Video aus:", type="mp4")
            if st.session_state["video2text_file_content"] is not None:
                st.write(
                    "Setzte den curser an die Stelle im Text, an der die Beschreibung eingefügt werden soll.")
                if st.button("📝 Convert"):
                    with st.status("Auf KI warten..."):
                        time.sleep(5)  # TODO: Video2Text
                        st.success(
                            "✅ Video zusammengefasst und Text eingefügt")
                    st.session_state["video2text_file_content"] = None


def clear_text():
    st.session_state["show_text2text_area_content"] = ""


def text2text():
    if "show_text2text_area" not in st.session_state:
        st.session_state["show_text2text_area"] = False

    if "show_text2text_area_content" not in st.session_state:
        st.session_state["show_text2text_area_content"] = ""

    if "show_text2text_area_history" not in st.session_state:
        st.session_state["show_text2text_area_history"] = [{
            "role": "user",
            "content": "Was ist die Antwort auf das Leben, das Universum und Allem?",
        }, {
            "role": "assistent",
            "content": "Die Antwort ist 42!",
        }, {
            "role": "user",
            "content": "Was ist die Antwort auf das Leben, das Universum und Allem?",
        }, {
            "role": "assistent",
            "content": "Die Antwort ist 41!",
        }]

    if st.button("🖹 Text2Text"):
        st.session_state["show_text2text_area"] = not st.session_state["show_text2text_area"]

    if st.session_state["show_text2text_area"]:
        with st.container():
            st.markdown("""
                <style>
                .float-left {
                    width: 80%;
                    float: left;
                    margin: 10px;
                    border: 1px solid;
                    padding: 1em;
                    border-radius: 1em;
                }
                .float-right {
                    width: 80%;
                    float: right;
                    text-align: right;
                    margin: 10px;
                    border: 1px solid;
                    padding: 1em;
                    border-radius: 1em;
                }
                </style>
            """, unsafe_allow_html=True)

            for index, message in enumerate(st.session_state["show_text2text_area_history"]):
                if message["role"] == "user":
                    st.markdown(f'<div class="float-right"><h4>User:</h4>{message["content"]}</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="float-left"><h4>System</h4>{message["content"]}</div>',
                                unsafe_allow_html=True)
                    st.button("📑 Nachricht in Notiz einfügen",
                              on_click=lambda msg=message["content"]: paste_text(
                                  msg),
                              key=f"paste_button_{index}")

            st.text_area(
                "Stelle eine Frage:",
                key="show_text2text_area_content"
            )

            if st.button("✅ Senden", on_click=clear_text):
                # TODO: senden
                pass


def paste_text(txt):
    print(txt, file=sys.stderr)
    pass
