import streamlit as st


def initialize_session_state():
    """Initialize all required session state variables for the NoKeeA application.

    This function ensures that all necessary session state variables are properly
    initialized with default values if they don't already exist. This is crucial
    for maintaining application state across interactions.

    Initializes the following variables:
    - editor_content: The current content of the note being edited
    - loaded_note: The name of the currently loaded note
    - note_name: The name of the note being edited
    - last_loaded_note: The name of the previously loaded note
    - editor_key: The key of the Quill editor

    Returns:
        None: The function modifies the session state but does not return any values.

    Note:
        This function should be called at the start of any component that needs
        access to these session state variables. It ensures that all required
        variables exist before they are accessed, preventing potential KeyError
        exceptions.
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