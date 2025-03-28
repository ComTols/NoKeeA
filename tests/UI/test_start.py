import pytest
from unittest.mock import patch


@pytest.fixture
def mock_subprocess():
    """Create a mock for the subprocess.run function.

    This fixture provides a mock object for the subprocess.run function,
    allowing tests to verify how the function is called without actually
    executing system commands.

    Yields:
        unittest.mock.MagicMock: A mock object for subprocess.run

    Note:
        The fixture uses context manager to ensure proper cleanup after
        each test. It patches the subprocess.run function in the NoKeeA.UI.start
        module.
    """
    with patch('NoKeeA.UI.start.subprocess.run') as mock_run:
        yield mock_run


def test_streamlit_start(mock_subprocess):
    """Test if the Streamlit UI can be started with correct configuration.

    This test verifies that the start_ui function:
    1. Calls subprocess.run with the correct command
    2. Uses the proper Streamlit arguments
    3. Points to the correct UI script
    4. Sets up headless mode correctly

    The test checks that:
    - The command starts with "streamlit run"
    - The UI script path is correct
    - Headless mode is enabled
    - All required arguments are present

    Args:
        mock_subprocess: The mocked subprocess.run function

    Note:
        The test uses a mock to avoid actually starting the Streamlit server
        during testing. It verifies the correct configuration of the command
        that would be used to start the server.
    """
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
