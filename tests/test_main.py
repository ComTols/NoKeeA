import threading
import time

import main
import psutil


def is_port_open(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False


def test_main(capfd):
    thread = threading.Thread(target=main.main, daemon=True)
    thread.start()
    time.sleep(3)

    assert is_port_open(8501), "Streamlit-Port ist nicht offen!"
