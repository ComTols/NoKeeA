import streamlit as st

from NoKeeA.UI.streamlit_content import content
from NoKeeA.UI.streamlit_sidebar import render_sidebar
from NoKeeA.utils.session_state import initialize_session_state

from src.NoKeeA.UI.streamlit_content import ai_functions


def main():
    """Initialize and run the main Streamlit user interface for NoKeeA.

    This function serves as the main entry point for the Streamlit UI. It:
    1. Configures the page settings with a wide layout
    2. Initializes the session state for managing application data
    3. Renders the sidebar navigation
    4. Renders the main content area

    The function orchestrates the overall UI structure and ensures all
    components are properly initialized and displayed.

    Returns:
        None

    Note:
        This function should be called by Streamlit when the application
        starts. It sets up the basic structure of the application's
        user interface.
    """

    st.set_page_config(page_title="Notiz-App", layout="wide")

    # Initialize session state
    initialize_session_state()

    # Render sidebar
    render_sidebar()

    # Render main content
    content()

    # Render ai functions
    ai_functions()


if __name__ == "__main__":
    main()
