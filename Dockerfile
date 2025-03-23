FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Create empty README.md
RUN touch README.md

RUN pip install poetry

# First install dependencies only
RUN poetry install --no-root

# Copy the source code
COPY . .

# Install the package itself and development dependencies
RUN poetry install --with dev

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit UI
CMD ["poetry", "run", "streamlit", "run", "src/NoKeeA/UI/streamlit_ui.py"]
