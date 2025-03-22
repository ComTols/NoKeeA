import pytest
from unittest.mock import patch


@pytest.fixture
def mock_subprocess():
    with patch('NoKeeA.UI.start.subprocess.run') as mock_run:
        yield mock_run


def test_streamlit_start(mock_subprocess):
    """Test if the streamlit UI can be started"""
    from NoKeeA.UI import start_ui

    # Call the function
    start_ui()

    # Verify that subprocess.run was called with correct arguments
    mock_subprocess.assert_called_once()
    args = mock_subprocess.call_args[0][0]

    assert args[0] == "streamlit"
    assert args[1] == "run"
    assert args[-1].endswith("streamlit_ui.py")
    assert "--server.headless" in args
    assert "true" in args
