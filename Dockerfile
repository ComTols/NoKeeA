FROM python:3.13.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Create empty README.md
RUN touch README.md

RUN pip install poetry

# First install dependencies only
RUN poetry install --no-root

# Copy the source code
COPY . .

# Install the package itself
RUN poetry install

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit UI
CMD ["poetry", "run", "streamlit", "run", "src/NoKeeA/UI/streamlit_ui.py"]
