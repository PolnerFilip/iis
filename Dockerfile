FROM python:3.9.13-slim-buster

LABEL authors="Uporabnik"

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

ADD . /app

RUN poetry install

EXPOSE 5001

CMD ["python", "src/serve/server.py"]