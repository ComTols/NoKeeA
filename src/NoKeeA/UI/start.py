import subprocess
import os


def start():
    ui_path = os.getenv("STREAMLIT_UI_SCRIPT",
                        "src\\NoKeeA\\UI\\streamlit_ui.py")

    print("Starting NoKeeA-UI...")
    streamlit_process = subprocess.Popen(
        ["poetry","run", "streamlit", "run", "--server.headless", "true", "--server.port=8501",
         "--server.address=0.0.0.0", ui_path],
        stdout=subprocess.PIPE
    )

    return streamlit_process
