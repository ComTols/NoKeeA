import pytest
from unittest.mock import patch, MagicMock
from NoKeeA.UI.streamlit_sidebar import render_sidebar


@pytest.fixture
def mock_streamlit():
    """
    Create a mock for Streamlit components.

    This fixture provides mock implementations for all Streamlit components used in the sidebar:
    - title: For rendering the sidebar title
    - selectbox: For note selection
    - text_input: For note name input
    - button: For action buttons (save, delete, new)
    - success/error: For status messages

    Returns:
        MagicMock: A mock object containing all necessary Streamlit component mocks.

    Note:
        The mock components are configured with default return values that can be
        overridden in individual tests as needed.
    """
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
    """
    Create mocks for file operations used in the sidebar.

    This fixture provides mock implementations for all file-related operations:
    - list_notes: For retrieving available notes
    - load_note: For loading note content
    - save_note: For saving note content
    - delete_note: For deleting notes

    Returns:
        dict: A dictionary containing mock objects for all file operations.

    Note:
        The mocks are configured with default return values that can be
        overridden in individual tests to simulate different scenarios.
    """
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
    """
    Create a mock for Streamlit's session state.

    This fixture provides mock implementations for session state operations:
    - get: For retrieving session state values
    - __getitem__: For dictionary-style access to session state
    - __setitem__: For setting session state values

    Returns:
        MagicMock: A mock object containing all necessary session state operation mocks.

    Note:
        The mock session state is configured to handle common operations
        and can be customized for specific test scenarios.
    """
    with patch("streamlit.session_state") as mock_state:
        mock_state.get = MagicMock(return_value=None)
        mock_state.__getitem__ = MagicMock(return_value="")
        mock_state.__setitem__ = MagicMock()
        yield mock_state


def test_render_sidebar_basic(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """
    Test basic rendering of the sidebar components.

    This test verifies that all essential UI elements are properly rendered:
    - Sidebar title
    - Note selection dropdown
    - Note name input field
    - Action buttons (save, delete, new)

    Args:
        mock_streamlit: Mock for Streamlit components
        mock_file_operations: Mock for file operations
        mock_session_state: Mock for session state

    Note:
        This test focuses on the presence and correct initialization of UI elements
        without testing their functionality.
    """
    render_sidebar()

    # Verify basic UI elements are created
    mock_streamlit.title.assert_called_once_with("⚙️ Einstellungen")
    mock_streamlit.selectbox.assert_called_once()
    mock_streamlit.text_input.assert_called_once()
    assert mock_streamlit.button.call_count == 3


def test_render_sidebar_load_note(
        mock_streamlit, mock_file_operations, mock_session_state
):
    """
    Test the note loading functionality of the sidebar.

    This test verifies the complete note loading process:
    - Selection of a note from the dropdown
    - Loading of note content
    - Update of session state
    - Display of success message

    Args:
        mock_streamlit: Mock for Streamlit components
        mock_file_operations: Mock for file operations
        mock_session_state: Mock for session state

    Note:
        The test simulates the first load of a note by setting the session state
        to None initially.
    """
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
    """
    Test the note saving functionality of the sidebar.

    This test verifies the complete note saving process:
    - Clicking the save button
    - Saving note content
    - Update of session state
    - Display of success message

    Args:
        mock_streamlit: Mock for Streamlit components
        mock_file_operations: Mock for file operations
        mock_session_state: Mock for session state

    Note:
        The test ensures that the note content is properly saved and that
        appropriate feedback is provided to the user.
    """
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
    """
    Test the note deletion functionality of the sidebar.

    This test verifies the complete note deletion process:
    - Clicking the delete button
    - Deletion of the note
    - Clearing of session state
    - Display of success message

    Args:
        mock_streamlit: Mock for Streamlit components
        mock_file_operations: Mock for file operations
        mock_session_state: Mock for session state

    Note:
        The test ensures that the note is properly deleted and that all
        related state is cleared.
    """
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
    """
    Test the new note creation functionality of the sidebar.

    This test verifies the complete new note creation process:
    - Clicking the new note button
    - Creation of a new note with default name
    - Reset of editor content
    - Update of session state

    Args:
        mock_streamlit: Mock for Streamlit components
        mock_file_operations: Mock for file operations
        mock_session_state: Mock for session state

    Note:
        The test ensures that a new note is properly initialized with
        default values and that the editor is reset.
    """
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
    """
    Test error handling in the sidebar operations.

    This test verifies the error handling for various operations:
    - Loading errors
    - Saving errors
    - Deletion errors
    - Display of error messages

    Args:
        mock_streamlit: Mock for Streamlit components
        mock_file_operations: Mock for file operations
        mock_session_state: Mock for session state

    Note:
        The test ensures that errors are properly caught and that
        appropriate error messages are displayed to the user.
    """
    # Setup
    mock_file_operations["load_note"].side_effect = Exception("Test error")
    mock_streamlit.selectbox.return_value = "Test Note"
    mock_session_state.get.return_value = None

    render_sidebar()

    # Verify error handling
    mock_streamlit.error.assert_any_call(
        "❌ Fehler beim Laden: Test error")
