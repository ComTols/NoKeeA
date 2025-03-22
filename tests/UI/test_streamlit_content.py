import pytest
from unittest.mock import patch


@pytest.fixture
def mock_streamlit():
    with patch('NoKeeA.UI.streamlit_content.st') as mock_st:
        mock_st.session_state = {}
        yield mock_st


@pytest.fixture
def mock_quill():
    with patch('NoKeeA.UI.streamlit_content.st_quill') as mock_st_quill:
        yield mock_st_quill


def test_editor_initialization(mock_streamlit, mock_quill):
    """Test if editor initializes with empty content"""
    from NoKeeA.UI.streamlit_content import content
    content()
    mock_quill.assert_called_once()
    # Verify default empty content
    assert mock_quill.call_args[1]['value'] == ""


def test_editor_with_existing_content(mock_streamlit, mock_quill):
    """Test if editor loads content from session state"""
    from NoKeeA.UI.streamlit_content import content
    # Set up session state with content
    mock_streamlit.session_state["editor_content"] = "Existing content"
    content()
    mock_quill.assert_called_once()
    # Verify content from session state
    assert mock_quill.call_args[1]['value'] == "Existing content"


def test_editor_toolbar_configuration(mock_streamlit, mock_quill):
    """Test if editor toolbar is configured correctly"""
    from NoKeeA.UI.streamlit_content import content
    content()
    toolbar = mock_quill.call_args[1]['toolbar']

    # Test text formatting features
    assert ["bold", "italic", "underline", "strike"] in toolbar

    # Test font and size options
    font_options = None
    size_options = None
    for item in toolbar:
        if isinstance(item[0], dict) and "font" in item[0]:
            font_options = item[0]["font"]
        if isinstance(item[0], dict) and "size" in item[0]:
            size_options = item[0]["size"]

    assert font_options is not None, "Font options not found in toolbar"
    assert "Arial" in font_options, "Arial font not available"
    assert "monospace" in font_options, "Monospace font not available"

    assert size_options is not None, "Size options not found in toolbar"
    assert "small" in size_options, "Small size not available"
    assert "large" in size_options, "Large size not available"

    # Test alignment options
    align_options = None
    for item in toolbar:
        if isinstance(item[0], dict) and "align" in item[0]:
            align_options = item
            break
    assert align_options is not None, "Alignment options not found"

    # Test indentation
    assert [{"indent": "-1"}, {"indent": "+1"}] in toolbar

    # Test lists
    assert [{"list": "ordered"}, {"list": "bullet"}] in toolbar

    # Test media and special elements
    assert ["link", "image", "video", "formula"] in toolbar

    # Test code blocks
    assert ["blockquote", "code-block"] in toolbar


def test_editor_html_mode(mock_streamlit, mock_quill):
    """Test if editor is configured to use HTML mode"""
    from NoKeeA.UI.streamlit_content import content
    content()
    assert mock_quill.call_args[1]['html'] is True
