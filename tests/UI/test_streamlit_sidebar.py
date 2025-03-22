import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_streamlit():
    with patch('NoKeeA.UI.streamlit_sidebar.st') as mock_st:
        mock_st.session_state = {
            "editor_content": "",
            "loaded_note": "",
            "note_name": "",
            "last_loaded_note": None
        }
        mock_st.sidebar = MagicMock()
        mock_st.sidebar.title = MagicMock()
        mock_st.sidebar.text_input = MagicMock()
        mock_st.sidebar.button = MagicMock()
        mock_st.sidebar.selectbox = MagicMock()
        mock_st.sidebar.text = MagicMock()
        mock_st.sidebar.empty = MagicMock()
        mock_st.sidebar.markdown = MagicMock()
        mock_st.sidebar.success = MagicMock()
        mock_st.sidebar.error = MagicMock()
        yield mock_st


@pytest.fixture
def mock_session_state():
    with patch(
        'NoKeeA.UI.streamlit_sidebar.initialize_session_state'
    ) as mock_init:
        yield mock_init


def test_sidebar_initialization(mock_streamlit, mock_session_state):
    """Test if sidebar initializes correctly"""
    from NoKeeA.UI import render_sidebar
    render_sidebar()

    # Verify session state initialization was called at least once
    assert mock_session_state.call_count > 0, \
        "Session state should be initialized at least once"

    # Verify title is set
    mock_streamlit.sidebar.title.assert_called_once_with("📝 Notiz-Verwaltung")


def test_sidebar_password_input(mock_streamlit, mock_session_state):
    """Test if password input is handled correctly"""
    from NoKeeA.UI import render_sidebar

    # Set up mock return values
    mock_streamlit.sidebar.text_input.return_value = "test_password"

    render_sidebar()

    # Verify session state initialization was called at least once
    assert mock_session_state.call_count > 0, \
        "Session state should be initialized at least once"

    # Verify text input is created
    mock_streamlit.sidebar.text_input.assert_any_call(
        "🔤 Notizname",
        "Neue Notiz"
    )


def test_sidebar_buttons(mock_streamlit, mock_session_state):
    """Test if sidebar buttons are created correctly"""
    from NoKeeA.UI import render_sidebar

    render_sidebar()

    # Verify session state initialization was called at least once
    assert mock_session_state.call_count > 0, \
        "Session state should be initialized at least once"

    # Verify buttons are created
    mock_streamlit.sidebar.button.assert_any_call("💾 Speichern")
    mock_streamlit.sidebar.button.assert_any_call("🗑 Notiz löschen")


def test_sidebar_file_selection(mock_streamlit, mock_session_state):
    """Test if file selection is handled correctly"""
    from NoKeeA.UI import render_sidebar

    # Set up mock return values
    mock_streamlit.sidebar.selectbox.return_value = "test_file.txt"

    render_sidebar()

    # Verify session state initialization was called at least once
    assert mock_session_state.call_count > 0, \
        "Session state should be initialized at least once"

    # Verify file selection is created with correct options
    selectbox_calls = mock_streamlit.sidebar.selectbox.call_args_list
    assert len(selectbox_calls) > 0, "selectbox should be called at least once"

    # Get the first call to selectbox
    first_call = selectbox_calls[0]
    args, kwargs = first_call

    # Verify the structure of the call
    assert args[0] == "📝 Notiz laden", "First argument should be the label"
    assert isinstance(args[1], list), "Second argument should be a list"
    assert len(args[1]) > 0, "The list should not be empty"
    assert args[1][0] == "", "First option should be empty string"
    assert kwargs.get("index") == 0, "index should be 0"
    assert kwargs.get(
        "key") == "note_selector", "key should be 'note_selector'"
