FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY . .
CMD ["python", "launcher.py"]

# https://github.com/poketwo/poketwo/blob/master/Dockerfile