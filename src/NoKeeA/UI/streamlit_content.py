import numbers
import sys

import streamlit as st
from streamlit_quill import st_quill
from NoKeeA.utils.session_state import initialize_session_state
from NoKeeA.utils.wikipedia_api import get_wikipedia_summary
import time
from NoKeeA.AI import video2text as v2t


def update_quill_editor():
    """
    Updates the editor key in Streamlit's session state to trigger a re-render.

    The key is dynamically generated based on the current time and the loaded note name.
    This ensures the editor is refreshed, e.g., after inserting new content.
    """
    st.session_state["editor_key"] = f"editor_{time.time()}_{st.session_state.get('loaded_note', 'new')}"


def content():
    """
    Renders the main content area: Quill editor and Wikipedia search.

    Features:
    - Initializes session state.
    - Displays a rich text editor with a configured toolbar.
    - Allows searching for Wikipedia articles.
    - Shows article summaries.
    - Appends article summaries to the note on button click.
    - Uses dynamic keys to force editor refresh when needed.
    """
    initialize_session_state()

    st.subheader("📝 Notiz bearbeiten")

    # Editor with dynamic key
    content = st_quill(
        value=st.session_state.get("editor_content", ""),
        html=True,
        toolbar=[
            ["bold", "italic", "underline", "strike"],
            [{"font": ["Arial", "monospace"]}],
            [{"size": ["small", "large"]}],
            [{"align": ["", "center", "right", "justify"]}],
            [{"indent": "-1"}, {"indent": "+1"}],
            [{"list": "ordered"}, {"list": "bullet"}],
            ["link", "image", "video", "formula"],
            ["blockquote", "code-block"]
        ],
        key=st.session_state["editor_key"]
    )

    if content is not None:
        st.session_state["editor_content"] = content

    # Wikipedia search
    with st.expander("📚 Wikipedia-Suche"):
        wiki_term = st.text_input("🔍 Begriff eingeben", key="wiki_editor_term")

        if st.button("🔎 Wikipedia nachschlagen"):
            if wiki_term and isinstance(wiki_term, str) and wiki_term.strip():
                try:
                    result = get_wikipedia_summary(wiki_term)
                    if "summary" in result:
                        st.session_state["wiki_result"] = result  # store result temporarily
                        st.success(result["summary"])
                        st.markdown(f"[🔗 Zum Artikel]({result['url']})", unsafe_allow_html=True)
                    else:
                        st.error(result["error"])
                except Exception as e:
                    st.error(f"❌ Fehler bei Wikipedia-Abfrage: {e}")
            else:
                st.info("Bitte gib einen gültigen Begriff ein.")

        # Show insert button if a result is available
        if "wiki_result" in st.session_state and st.session_state["wiki_result"]:
            if st.button("📥 In Notiz einfügen"):
                summary = st.session_state["wiki_result"]["summary"]
                current_content = st.session_state.get("editor_content", "")
                new_content = current_content + f"<p>{summary}</p>"
                st.session_state["editor_content"] = new_content

                # Clear only the stored Wikipedia result (not the search term)
                st.session_state.pop("wiki_result", None)

                # Trigger editor refresh with new key
                update_quill_editor()
                st.rerun()


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
                "Wähle ein Video aus, das von der KI zusammengefasst wird. "
                "Die Informationen werden direkt in die Notiz eingefügt.")
            st.session_state["video2text_file_content"] = st.file_uploader(
                "Wähle ein Video aus:", type="mp4")
            if st.session_state["video2text_file_content"] is not None:
                st.write("Die Beschreibung wird ans Ende der Notiz eingefügt.")
                if st.button("📝 Convert"):
                    with st.status("Auf KI warten...", expanded=True) as status:
                        try:
                            gen = v2t.video2text(
                                st.session_state["video2text_file_content"])
                            while True:
                                step = next(gen)
                                if isinstance(step, str):
                                    if "video2text_progress_bar" in st.session_state:
                                        del st.session_state["video2text_progress_bar"]
                                    st.success(step)
                                elif isinstance(step, numbers.Number):
                                    if "video2text_progress_bar_text" not in st.session_state:
                                        st.session_state["video2text_progress_bar_text"] = "Bitte warten..."
                                    if "video2text_progress_bar" not in st.session_state:
                                        st.session_state["video2text_progress_bar"] = st.progress(
                                            0, st.session_state["video2text_progress_bar_text"])

                                    st.session_state["video2text_progress_bar"].progress(
                                        step,
                                        f"{st.session_state['video2text_progress_bar_text']} ~ {(step * 100):.2f}%")
                        except StopIteration as e:
                            st.write(e.value)
                            status.update(
                                label="Video zusammengefasst!",
                                state="complete",
                                expanded=False,
                            )
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
