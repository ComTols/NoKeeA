import streamlit as st

from NoKeeA.UI.streamlit_content import content
from NoKeeA.UI.streamlit_sidebar import render_sidebar
from NoKeeA.utils.session_state import initialize_session_state


def main():
    """Initialize and run the Streamlit UI"""
    st.set_page_config(page_title="Notiz-App", layout="wide")

    # Initialize session state
    initialize_session_state()

    # Render sidebar
    render_sidebar()

    # Render main content
    content()


if __name__ == "__main__":
    main()
