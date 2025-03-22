import streamlit as st
from NoKeeA.UI.streamlit_content import content


def main():
    """Initialize and run the Streamlit UI"""
    st.set_page_config(page_title="Notiz-App", layout="wide")

    # Saving content in session
    if "editor_content" not in st.session_state:
        st.session_state["editor_content"] = ""

    # Saving loaded name in session
    if "loaded_note" not in st.session_state:
        st.session_state["loaded_note"] = ""

    # Saving uploaded file in session
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None

    content()


if __name__ == "__main__":
    main()
