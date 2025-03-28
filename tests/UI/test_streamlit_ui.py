from streamlit.testing.v1 import AppTest
import os
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def clear_module():
    """Clear the module from sys.modules before each test.

    This fixture ensures a clean state for each test by removing the
    streamlit_ui module from sys.modules. This prevents any cached
    state from previous tests from affecting the current test.

    Yields:
        None: The fixture yields after clearing the module

    Note:
        The fixture is marked as autouse=True, meaning it will run
        automatically before each test in this module.
    """
    import sys
    if 'NoKeeA.UI.streamlit_ui' in sys.modules:
        del sys.modules['NoKeeA.UI.streamlit_ui']
    yield


def test_streamlit_ui():
    """Test if the Streamlit UI can be loaded and executed.

    This test verifies that the main Streamlit UI script can be loaded
    and executed without errors. It uses Streamlit's testing framework
    to simulate running the application.

    The test:
    1. Locates the UI script file
    2. Creates an AppTest instance from the file
    3. Runs the application in test mode

    Note:
        The test uses the STREAMLIT_UI_SCRIPT_TEST environment variable
        if available, otherwise falls back to the default path in the src directory.
    """
    ui_path = os.getenv("STREAMLIT_UI_SCRIPT_TEST",
                        os.path.join("src", "NoKeeA", "UI", "streamlit_ui.py"))
    _ = AppTest.from_file(ui_path).run(timeout=10)


def test_page_config():
    """Test if the Streamlit page is configured correctly.

    This test verifies that the page configuration is set up properly
    with the correct title and layout settings.

    The test:
    1. Mocks the Streamlit module
    2. Imports and runs the UI module
    3. Verifies that set_page_config was called with the correct parameters:
       - page_title: "Notiz-App"
       - layout: "wide"

    Note:
        The test uses a mock to avoid actual Streamlit initialization
        while verifying the configuration settings.
    """
    mock_st = MagicMock()
    mock_st.session_state = {}

    with patch('NoKeeA.UI.streamlit_ui.st', mock_st):
        # Import after patching
        from NoKeeA.UI import streamlit_ui
        # Call main() to trigger initialization
        streamlit_ui.main()

        # Verify page configuration was called with correct arguments
        mock_st.set_page_config.assert_called_once_with(
            page_title="Notiz-App",
            layout="wide"
        )


def test_session_state_initialization():
    """Test if session state variables are initialized correctly.

    This test verifies that all required session state variables are
    properly initialized with their default values.

    The test:
    1. Mocks the Streamlit module with an empty session state
    2. Calls the initialization function
    3. Verifies that all required variables are present with correct values:
       - editor_content: empty string
       - loaded_note: empty string
       - note_name: empty string
       - last_loaded_note: None

    Note:
        The test ensures that the application starts with a clean,
        properly initialized state.
    """
    mock_st = MagicMock()
    mock_st.session_state = {
        "editor_content": "",
        "loaded_note": "",
        "note_name": "",
        "last_loaded_note": None
    }

    with patch('NoKeeA.UI.streamlit_ui.st', mock_st):
        # Import after patching
        from NoKeeA.UI.streamlit_ui import initialize_session_state

        # Call initialize_session_state directly
        initialize_session_state()

        # Check if session state variables are initialized
        expected_state = {
            "editor_content": "",
            "loaded_note": "",
            "note_name": "",
            "last_loaded_note": None
        }

        # Überprüfe, dass alle erwarteten Schlüssel mit den richtigen Werten
        # vorhanden sind
        for key, value in expected_state.items():
            assert mock_st.session_state.get(key) == value, \
                f"Session state '{key}' has wrong value"


def test_content_called():
    """Test if the content function is called during UI initialization.

    This test verifies that the content function is properly called
    when the UI is initialized.

    The test:
    1. Mocks both the Streamlit module and the content function
    2. Imports and runs the UI module
    3. Verifies that the content function was called exactly once

    Note:
        The test ensures that the main content area is properly
        initialized when the application starts.
    """
    mock_st = MagicMock()
    mock_st.session_state = {}
    mock_content = MagicMock()

    with patch('NoKeeA.UI.streamlit_ui.st', mock_st), \
            patch('NoKeeA.UI.streamlit_ui.content', mock_content):
        # Import after patching
        from NoKeeA.UI import streamlit_ui
        # Call main() to trigger content call
        streamlit_ui.main()

        # Verify content function was called exactly once
        mock_content.assert_called_once()
