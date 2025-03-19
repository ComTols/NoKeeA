import time

import UI.start as ui
import psutil

STREAMLIT_PORT = 8501


def is_port_open(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False


def stop_streamlit(process):
    process.terminate()
    process.wait()


def test_streamlit_prod(capfd):
    process = ui.start()
    time.sleep(10)

    out, err = capfd.readouterr()
    assert out == "Starting NoKeeA-UI...\n"
    assert err == ""

    try:
        assert is_port_open(STREAMLIT_PORT), "Streamlit-Port ist nicht offen!"
    finally:
        stop_streamlit(process)
