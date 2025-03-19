from streamlit.testing.v1 import AppTest
import os

def test_streamlit_ui():
    ui_path = os.getenv("STREAMLIT_UI_SCRIPT_TEST",
                        "src\\NoKeeA\\UI\\streamlit_ui.py")
    _ = AppTest.from_file(ui_path).run()
