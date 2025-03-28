import time
import pytest
from unittest.mock import patch, MagicMock
from NoKeeA.UI import streamlit_content


@pytest.fixture
def mock_streamlit():
    """
    Mocks the Streamlit module and sets up default session state values.
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
    """
    Mocks the st_quill editor.
    """
    with patch('NoKeeA.UI.streamlit_content.st_quill') as mock_st_quill:
        yield mock_st_quill


@pytest.fixture
def mock_session_state():
    """
    Mocks the session state initialization function.
    """
    with patch(
        'NoKeeA.UI.streamlit_content.initialize_session_state'
    ) as mock_init:
        yield mock_init


def test_editor_initialization(mock_streamlit, mock_quill, mock_session_state):
    """
    Tests if the editor initializes with empty content.
    """
    from NoKeeA.UI.streamlit_content import content
    content()

    mock_session_state.assert_called_once()
    mock_quill.assert_called_once()
    assert mock_quill.call_args[1]['value'] == ""


def test_editor_with_existing_content(mock_streamlit, mock_quill, mock_session_state):
    """
    Tests if existing content from session state is loaded into the editor.
    """
    from NoKeeA.UI.streamlit_content import content
    mock_streamlit.session_state["editor_content"] = "Existing content"
    content()

    mock_session_state.assert_called_once()
    mock_quill.assert_called_once()
    assert mock_quill.call_args[1]['value'] == "Existing content"


def test_editor_toolbar_configuration(mock_streamlit, mock_quill, mock_session_state):
    """
    Tests the toolbar configuration for the Quill editor.
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
    """
    Tests if the editor is set to HTML mode.
    """
    from NoKeeA.UI.streamlit_content import content
    content()

    mock_session_state.assert_called_once()
    assert mock_quill.call_args[1]['html'] is True


@pytest.fixture
def setup_session(monkeypatch):
    """
    Sets up a mocked Streamlit environment for Wikipedia search testing.
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
    monkeypatch.setattr(streamlit_content, "st_quill",
                        MagicMock(return_value="test content"))
    monkeypatch.setattr(streamlit_content,
                        "initialize_session_state", MagicMock())
    return mock_st


def test_wikipedia_search_and_insert(setup_session, monkeypatch):
    """
    Tests the Wikipedia search and insert functionality into the note.
    """
    mock_st = setup_session

    # Mock Wikipedia result
    mock_result = {
        "summary": "Python ist eine Programmiersprache.",
        "url": "https://de.wikipedia.org/wiki/Python"
    }
    monkeypatch.setattr(streamlit_content,
                        "get_wikipedia_summary", lambda term: mock_result)

    streamlit_content.content()

    assert "wiki_result" not in mock_st.session_state
    assert "Python ist eine Programmiersprache." in mock_st.session_state["editor_content"]
    mock_st.success.assert_called()
    mock_st.markdown.assert_called()


def test_update_quill_editor_sets_new_key(monkeypatch):
    """
    Tests if `update_quill_editor()` sets a new key in session state.
    """
    monkeypatch.setattr(streamlit_content.st, "session_state", {
                        "loaded_note": "TestNote"})
    streamlit_content.update_quill_editor()
    assert streamlit_content.st.session_state["editor_key"].startswith(
        "editor_")
