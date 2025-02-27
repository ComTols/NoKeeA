FROM python:3.13.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "src/NoKeeA/main.py"]
