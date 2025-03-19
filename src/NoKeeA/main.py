import UI.start as ui

def main():
    streamlit_process = ui.start()

    streamlit_process.wait()


if __name__ == "__main__":
    main()
