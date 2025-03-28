import os
import subprocess
import sys


def start_ui():
    """Initialize and start the Streamlit user interface for NoKeeA.

    This function launches the Streamlit UI in headless mode with minimal
    toolbar and error details disabled. It handles the setup and execution
    of the Streamlit server process.

    Returns:
        None

    Raises:
        SystemExit: If the UI script is not found or if there's an error
                   starting the Streamlit process.

    Note:
        The function runs Streamlit in headless mode with minimal UI elements
        for a cleaner user experience. Error handling is implemented to provide
        meaningful feedback if the startup fails.
    """
    # Get the absolute path to the UI script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(current_dir, "streamlit_ui.py")

    print(f"Starting UI with script at: {ui_path}")

    if not os.path.exists(ui_path):
        print(f"Error: UI script not found at {ui_path}")
        sys.exit(1)

    try:
        subprocess.run(
            ["poetry", "run", "streamlit", "run",
             "--server.headless", "true",
             "--client.showErrorDetails", "false",
             "--client.toolbarMode", "minimal",
             ui_path],
            cwd=current_dir
        )
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)
