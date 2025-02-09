FROM python:3.12-slim AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=true
ENV PYTHONDONTWRITEBYTECODE=true

FROM base AS build

ENV POETRY_VERSION=1.8.5
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /tmp

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

RUN apt-get update && apt-get install -y --no-install-recommends curl

ADD https://install.python-poetry.org install-poetry.py

RUN python3 install-poetry.py

COPY pyproject.toml poetry.lock ./

RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

WORKDIR /app

RUN python -m venv .venv && \
    ./.venv/bin/pip install -r /tmp/requirements.txt

FROM base AS prod

ENV LOGURU_COLORIZE=false

WORKDIR /app

COPY --from=build /app/.venv ./.venv
COPY . .

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

ENTRYPOINT [ "/app/.venv/bin/python", "-m", "autocomeback" ]
