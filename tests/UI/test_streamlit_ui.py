from streamlit.testing.v1 import AppTest


def test_streamlit_ui():
    _ = AppTest.from_file("src\\NoKeeA\\UI\\streamlit_ui.py").run()
