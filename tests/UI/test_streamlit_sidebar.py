import pytest
from unittest.mock import patch, MagicMock
from NoKeeA.UI.streamlit_sidebar import render_sidebar


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit components"""
    with patch("streamlit.sidebar") as mock_sidebar:
        # Mock basic Streamlit components
        mock_sidebar.title = MagicMock()
        mock_sidebar.selectbox = MagicMock(return_value="Test Note")
        mock_sidebar.text_input = MagicMock(return_value="Test Note")
        mock_sidebar.button = MagicMock(
            side_effect=[False, False, False])  # Save, Delete, New buttons
        mock_sidebar.success = MagicMock()
        mock_sidebar.error = MagicMock()
        yield mock_sidebar


@pytest.fixture
def mock_file_operations():
    """Mock file operations"""
    with patch("NoKeeA.UI.streamlit_sidebar.list_notes") as mock_list_notes, \
            patch("NoKeeA.UI.streamlit_sidebar.load_note") as mock_load_note, \
            patch("NoKeeA.UI.streamlit_sidebar.save_note") as mock_save_note, \
            patch(
                "NoKeeA.UI.streamlit_sidebar.delete_note"
    ) as mock_delete_note:

        # Setup mock returns
        mock_list_notes.return_value = ["Test Note"]
        mock_load_note.return_value = {
            "name": "Test Note", "content": "Test Content"}
        mock_delete_note.return_value = True

        yield {
            "list_notes": mock_list_notes,
            "load_note": mock_load_note,
            "save_note": mock_save_note,
            "delete_note": mock_delete_note
        }


@pytest.fixture
def mock_session_state():
    """Mock session state"""
    with patch("streamlit.session_state") as mock_state:
        mock_state.get = MagicMock(return_value=None)
        mock_state.__getitem__ = MagicMock(return_value="")
        mock_state.__setitem__ = MagicMock()
        yield mock_state


def test_render_sidebar_basic(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """Test basic sidebar rendering"""
    render_sidebar()

    # Verify basic UI elements are created
    mock_streamlit.title.assert_called_once_with("⚙️ Einstellungen")
    mock_streamlit.selectbox.assert_called_once()
    mock_streamlit.text_input.assert_called_once()
    assert mock_streamlit.button.call_count == 3


def test_render_sidebar_load_note(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """Test loading a note"""
    # Setup
    mock_streamlit.selectbox.return_value = "Test Note"
    mock_session_state.get.return_value = None  # Simulate first load

    render_sidebar()

    # Verify note loading
    mock_file_operations["load_note"].assert_called_once_with("Test Note")
    mock_streamlit.success.assert_called_once_with(
        "✅ Notiz 'Test Note' geladen.")


def test_render_sidebar_save_note(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """Test saving a note"""
    # Setup
    mock_streamlit.button.side_effect = [
        True, False, False]  # Save button clicked
    mock_session_state.__getitem__.return_value = "Test Note"
    mock_session_state.get.side_effect = lambda key, \
        default="": "Test Note" if key == "last_loaded_note" else default

    render_sidebar()

    # Verify save operation
    mock_file_operations["save_note"].assert_called_once_with("Test Note", "")
    mock_streamlit.success.assert_called_once_with(
        "✅ Notiz 'Test Note' gespeichert.")


def test_render_sidebar_delete_note(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """Test deleting a note"""
    # Setup
    mock_streamlit.button.side_effect = [
        False, True, False]  # Delete button clicked
    mock_session_state.__getitem__.return_value = "Test Note"
    mock_session_state.get.return_value = "Test Note"

    render_sidebar()

    # Verify delete operation
    mock_file_operations["delete_note"].assert_called_once_with("Test Note")
    mock_streamlit.success.assert_called_once_with(
        "✅ Notiz 'Test Note' gelöscht.")


def test_render_sidebar_new_note(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """Test creating a new note"""
    # Setup
    mock_streamlit.button.side_effect = [
        False, False, True]  # New note button clicked

    render_sidebar()

    # Verify new note creation
    mock_session_state.__setitem__.assert_any_call("note_name", "Neue Notiz2")
    mock_session_state.__setitem__.assert_any_call("editor_content", "")
    mock_session_state.__setitem__.assert_any_call("loaded_note", "")
    mock_session_state.__setitem__.assert_any_call("last_loaded_note", None)


def test_render_sidebar_error_handling(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """Test error handling in sidebar"""
    # Setup
    mock_file_operations["load_note"].side_effect = Exception("Test error")
    mock_streamlit.selectbox.return_value = "Test Note"
    mock_session_state.get.return_value = None

    render_sidebar()

    # Verify error handling
    mock_streamlit.error.assert_any_call(
        "❌ Fehler beim Laden: Test error")
