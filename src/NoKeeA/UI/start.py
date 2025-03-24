import os
import subprocess
import sys
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx


def start_ui():
    # Get the absolute path to the UI script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(current_dir, "streamlit_ui.py")

    print(f"Starting UI with script at: {ui_path}")

    if not os.path.exists(ui_path):
        print(f"Error: UI script not found at {ui_path}")
        sys.exit(1)

    try:
        ctx = get_script_run_ctx()
        process = subprocess.Popen(
            ["poetry", "run", "streamlit", "run",
             "--server.headless", "true",
             "--client.showErrorDetails", "false",
             "--client.toolbarMode", "minimal",
             ui_path],
            cwd=current_dir
        )
        if ctx is not None:
            add_script_run_ctx(process, ctx)
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)
