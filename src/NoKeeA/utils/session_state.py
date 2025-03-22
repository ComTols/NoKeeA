import streamlit as st


def initialize_session_state():
    """Initialize all required session state variables."""
    if "editor_content" not in st.session_state:
        st.session_state["editor_content"] = ""
    if "loaded_note" not in st.session_state:
        st.session_state["loaded_note"] = ""
    if "note_name" not in st.session_state:
        st.session_state["note_name"] = ""
    if "last_loaded_note" not in st.session_state:
        st.session_state["last_loaded_note"] = None
