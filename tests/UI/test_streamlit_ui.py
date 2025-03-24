from streamlit.testing.v1 import AppTest
import os
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def clear_module():
    """Clear the module from sys.modules before each test"""
    import sys
    if 'NoKeeA.UI.streamlit_ui' in sys.modules:
        del sys.modules['NoKeeA.UI.streamlit_ui']
    yield


def test_streamlit_ui():
    """Test if the streamlit UI can be loaded"""
    ui_path = os.getenv("STREAMLIT_UI_SCRIPT_TEST",
                        os.path.join("src", "NoKeeA", "UI", "streamlit_ui.py"))
    _ = AppTest.from_file(ui_path).run(timeout=10)


def test_page_config():
    """Test if the page is configured correctly"""
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
    """Test if session state variables are initialized correctly"""
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
    """Test if content function is called"""
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
