import os

from NoKeeA.UI import start_ui
from huggingface_hub import snapshot_download


def main():
    """Start the NoKeeA application"""

    if os.getenv("SKIPP_LARGE_AI_TESTS", "NO") != "YES":
        snapshot_download(repo_id="Salesforce/blip2-opt-2.7b",
                      local_dir="blip2_model")

    streamlit_process = start_ui()
    streamlit_process.wait()  # Wait for the process to complete
    return streamlit_process


if __name__ == "__main__":
    main()
