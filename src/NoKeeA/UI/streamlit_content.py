import streamlit as st
from streamlit_quill import st_quill
from NoKeeA.utils.session_state import initialize_session_state


def content():
    """Render the main content area with the editor."""
    # Ensure session state is initialized
    initialize_session_state()

    st.subheader("📝 Notiz bearbeiten")

    # Editor mit Callback für Änderungen
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
        key=f"editor_{st.session_state.get('loaded_note', 'new')}"
    )

    # Aktualisiere den Session State IMMER mit dem aktuellen Inhalt
    st.session_state["editor_content"] = (
        content if content is not None
        else st.session_state.get("editor_content", "")
    )
