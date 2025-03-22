# NoKeeA

A note-taking application built with Streamlit.

## Features
- Create and edit notes
- Save notes locally
- Modern and intuitive UI

## Development
This project uses Poetry for dependency management and Docker for containerization.

### Running locally
```bash
poetry install
poetry run streamlit run src/NoKeeA/UI/streamlit_ui.py
```

### Running with Docker
```bash
docker build -t nokeea .
docker run -p 8501:8501 nokeea
```
