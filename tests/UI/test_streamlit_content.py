import time
import pytest
from unittest.mock import patch, MagicMock
from NoKeeA.UI import streamlit_content


@pytest.fixture
def mock_streamlit():
    """Create a mock for the Streamlit module with initialized session state.

    This fixture provides a mock object for the Streamlit module with:
    - Pre-initialized session state variables
    - Mocked subheader function
    - All necessary Streamlit components for testing

    Yields:
        unittest.mock.MagicMock: A mock object for the Streamlit module

    Note:
        The fixture initializes the session state with default empty values
        for editor_content, loaded_note, note_name, and last_loaded_note.
    """
    with patch('NoKeeA.UI.streamlit_content.st') as mock_st:
        mock_st.session_state = {
            "editor_content": "",
            "loaded_note": "",
            "note_name": "",
            "last_loaded_note": None,
            "editor_key": time.time()
        }
        mock_st.subheader = MagicMock()
        yield mock_st


@pytest.fixture
def mock_quill():
    """Create a mock for the Streamlit Quill editor component.

    This fixture provides a mock object for the st_quill function,
    allowing tests to verify how the editor is configured and used.

    Yields:
        unittest.mock.MagicMock: A mock object for the st_quill function

    Note:
        The fixture patches the st_quill function to prevent actual
        rendering of the editor during tests.
    """
    with patch('NoKeeA.UI.streamlit_content.st_quill') as mock_st_quill:
        yield mock_st_quill


@pytest.fixture
def mock_session_state():
    """Create a mock for the session state initialization function.

    This fixture provides a mock object for the initialize_session_state
    function, allowing tests to verify that it's called appropriately.

    Yields:
        unittest.mock.MagicMock: A mock object for the initialize_session_state function

    Note:
        The fixture patches the initialize_session_state function to
        track its usage without actually initializing any state.
    """
    with patch(
        'NoKeeA.UI.streamlit_content.initialize_session_state'
    ) as mock_init:
        yield mock_init


def test_editor_initialization(mock_streamlit, mock_quill, mock_session_state):
    """Test if the editor initializes correctly with empty content.

    This test verifies that:
    1. The session state is properly initialized
    2. The Quill editor is created with empty content
    3. All initialization functions are called correctly

    Args:
        mock_streamlit: The mocked Streamlit module
        mock_quill: The mocked Quill editor component
        mock_session_state: The mocked session state initialization function

    Note:
        The test ensures that the editor starts with a clean state
        and all initialization steps are performed in the correct order.
    """
    from NoKeeA.UI.streamlit_content import content
    content()

    mock_session_state.assert_called_once()
    mock_quill.assert_called_once()
    assert mock_quill.call_args[1]['value'] == ""


def test_editor_with_existing_content(mock_streamlit, mock_quill, mock_session_state):
    """Test if the editor correctly loads and displays existing content.

    This test verifies that:
    1. The editor properly loads content from the session state
    2. The content is correctly passed to the Quill editor
    3. The session state is properly initialized

    Args:
        mock_streamlit: The mocked Streamlit module
        mock_quill: The mocked Quill editor component
        mock_session_state: The mocked session state initialization function

    Note:
        The test ensures that existing content is preserved and
        correctly displayed in the editor.
    """
    from NoKeeA.UI.streamlit_content import content
    mock_streamlit.session_state["editor_content"] = "Existing content"
    content()

    mock_session_state.assert_called_once()
    mock_quill.assert_called_once()
    assert mock_quill.call_args[1]['value'] == "Existing content"


def test_editor_toolbar_configuration(mock_streamlit, mock_quill, mock_session_state):
    """Test if the editor toolbar is configured with all required features.

    This test verifies that the Quill editor toolbar includes all necessary
    formatting options:
    1. Text formatting (bold, italic, underline, strike)
    2. Font options (Arial, monospace)
    3. Text size options (small, large)
    4. Alignment options
    5. Indentation controls
    6. List formatting (ordered and unordered)
    7. Media insertion (links, images, videos, formulas)
    8. Special formatting (blockquotes, code blocks)

    Args:
        mock_streamlit: The mocked Streamlit module
        mock_quill: The mocked Quill editor component
        mock_session_state: The mocked session state initialization function

    Note:
        The test ensures that all toolbar features are properly configured
        and available for use in the editor.
    """
    from NoKeeA.UI.streamlit_content import content
    content()

    mock_session_state.assert_called_once()
    toolbar = mock_quill.call_args[1]['toolbar']

    # Basic formatting tools
    assert ["bold", "italic", "underline", "strike"] in toolbar

    # Font and size options
    font_options = None
    size_options = None
    for item in toolbar:
        if isinstance(item[0], dict) and "font" in item[0]:
            font_options = item[0]["font"]
        if isinstance(item[0], dict) and "size" in item[0]:
            size_options = item[0]["size"]

    assert font_options is not None
    assert "Arial" in font_options
    assert "monospace" in font_options

    assert size_options is not None
    assert "small" in size_options
    assert "large" in size_options

    # Alignment options
    align_options = None
    for item in toolbar:
        if isinstance(item[0], dict) and "align" in item[0]:
            align_options = item
            break
    assert align_options is not None

    # Indentation, lists, and other tools
    assert [{"indent": "-1"}, {"indent": "+1"}] in toolbar
    assert [{"list": "ordered"}, {"list": "bullet"}] in toolbar
    assert ["link", "image", "video", "formula"] in toolbar
    assert ["blockquote", "code-block"] in toolbar


def test_editor_html_mode(mock_streamlit, mock_quill, mock_session_state):
    """Test if the editor is configured to use HTML mode.

    This test verifies that the Quill editor is properly configured to
    handle HTML content, which is essential for rich text formatting.

    Args:
        mock_streamlit: The mocked Streamlit module
        mock_quill: The mocked Quill editor component
        mock_session_state: The mocked session state initialization function

    Note:
        HTML mode is required for the editor to properly handle rich text
        formatting and maintain document structure.
    """
    from NoKeeA.UI.streamlit_content import content
    content()

    mock_session_state.assert_called_once()
    assert mock_quill.call_args[1]['html'] is True


@pytest.fixture
def setup_session(monkeypatch):
    """Fixture to set up a mocked Streamlit environment for Wikipedia interaction.

    This fixture provides:
    - Predefined session state values for the editor
    - Mocked input fields and buttons
    - Patched `st_quill`, `initialize_session_state`, and Wikipedia search functions

    Args:
        monkeypatch: The pytest monkeypatch utility to inject mocks.

    Yields:
        MagicMock: A fully mocked Streamlit module with UI and state components.
    """
    mock_st = MagicMock()
    mock_st.session_state = {
        "editor_content": "",
        "loaded_note": "",
        "note_name": "",
        "last_loaded_note": None,
        "editor_key": "editor_123"
    }
    mock_st.text_input.return_value = "Python"
    mock_st.button.side_effect = [True, True]  # First: search, second: insert
    mock_st.expander.return_value.__enter__.return_value = True
    mock_st.success = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.error = MagicMock()
    mock_st.info = MagicMock()
    mock_st.subheader = MagicMock()

    monkeypatch.setattr(streamlit_content, "st", mock_st)
    monkeypatch.setattr(streamlit_content, "st_quill", MagicMock(return_value="test content"))
    monkeypatch.setattr(streamlit_content, "initialize_session_state", MagicMock())
    return mock_st


def test_wikipedia_search_and_insert(setup_session, monkeypatch):
    """Test the Wikipedia search and insert functionality into the editor.

    This test verifies that:
    1. The Wikipedia summary is correctly fetched and inserted into the editor content.
    2. The search and insert buttons trigger the correct logic.
    3. The session state is updated with the new content.
    4. User feedback (success and markdown) is displayed appropriately.

    Args:
        setup_session: The mocked Streamlit environment with default session state.
        monkeypatch: The pytest monkeypatch utility to override functions during the test.

    Note:
        This test ensures the integration of Wikipedia search works as intended and
        provides feedback to the user when content is inserted.
    """
    mock_st = setup_session

    # Mock Wikipedia result
    mock_result = {
        "summary": "Python ist eine Programmiersprache.",
        "url": "https://de.wikipedia.org/wiki/Python"
    }
    monkeypatch.setattr(streamlit_content, "get_wikipedia_summary", lambda term: mock_result)

    streamlit_content.content()

    assert "wiki_result" not in mock_st.session_state
    assert "Python ist eine Programmiersprache." in mock_st.session_state["editor_content"]
    mock_st.success.assert_called()
    mock_st.markdown.assert_called()


def test_update_quill_editor_sets_new_key(monkeypatch):
    """Test if `update_quill_editor()` sets a new unique editor key.

    This test verifies that calling `update_quill_editor()` updates the
    `editor_key` in session state with a new timestamp-based identifier.

    Args:
        monkeypatch: The pytest monkeypatch utility to override session state during the test.

    Note:
        The `editor_key` is used to force reinitialization of the Quill editor,
        ensuring changes like content updates or UI refreshes are reflected.
    """
    monkeypatch.setattr(streamlit_content.st, "session_state", {"loaded_note": "TestNote"})
    streamlit_content.update_quill_editor()
    assert streamlit_content.st.session_state["editor_key"].startswith("editor_")
