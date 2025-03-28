import os

from NoKeeA.UI import start_ui
from huggingface_hub import snapshot_download


def main():
    """Initialize and start the NoKeeA application.

    This function serves as the entry point for the NoKeeA application.
    It initializes the user interface and waits for the process to complete.

    Returns:
        subprocess.Popen: The Streamlit process object that was started.

    Note:
        This function should be called directly when running the application
        as the main script.
    """
    if os.getenv("SKIPP_LARGE_AI_TESTS", "NO") != "YES":
        snapshot_download(repo_id="Salesforce/blip2-opt-2.7b",
                          local_dir="blip2_model")

    streamlit_process = start_ui()
    streamlit_process.wait()  # Wait for the process to complete
    return streamlit_process


if __name__ == "__main__":
    main()
