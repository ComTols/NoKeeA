import streamlit as st


def initialize_session_state():
    """
    Initialize all required keys in the Streamlit session state.

    This ensures that the editor and note-related features work reliably
    by setting default values for keys if they are not already present.
    """
    if "editor_content" not in st.session_state:
        st.session_state["editor_content"] = ""

    if "loaded_note" not in st.session_state:
        st.session_state["loaded_note"] = ""

    if "note_name" not in st.session_state:
        st.session_state["note_name"] = ""

    if "last_loaded_note" not in st.session_state:
        st.session_state["last_loaded_note"] = None

    if "editor_key" not in st.session_state:
        st.session_state["editor_key"] = None
