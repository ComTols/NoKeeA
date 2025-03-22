from NoKeeA.UI import start_ui


def main():
    """Start the NoKeeA application"""
    streamlit_process = start_ui()
    streamlit_process.wait()  # Wait for the process to complete
    return streamlit_process


if __name__ == "__main__":
    main()
