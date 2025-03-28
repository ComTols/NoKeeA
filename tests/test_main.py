import threading
import time
from NoKeeA import main
import psutil


def is_port_open(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False


def test_main():
    """Test if the main application starts correctly"""
    thread = threading.Thread(target=main.main, daemon=True)
    thread.start()
    time.sleep(3)

    assert is_port_open(8501), "Streamlit-Port ist nicht offen!"
