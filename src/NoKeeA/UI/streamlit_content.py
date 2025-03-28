import streamlit as st
from streamlit_quill import st_quill
from NoKeeA.utils.session_state import initialize_session_state
from NoKeeA.utils.wikipedia_api import get_wikipedia_summary
import time


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

    Returns:
        None: The function renders UI elements but does not return any values.
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
