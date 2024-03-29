FROM python:3.10.7 as base

WORKDIR /usr/src/app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as poetry

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.2.1

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install "poetry==$POETRY_VERSION"

FROM poetry as build

COPY poetry.lock ./
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/pypoetry/cache \
    --mount=type=cache,target=/root/.cache/pypoetry/artifacts \
    poetry install --sync --no-root --no-interaction --no-ansi

COPY . ./
RUN make build

FROM poetry as install

RUN python -m venv /opt/venv
COPY poetry.lock ./
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/pip \
    poetry export -f requirements.txt | /opt/venv/bin/pip install -r /dev/stdin
COPY --from=build /usr/src/app .
RUN /opt/venv/bin/pip install --no-deps dist/*.whl

FROM base as app

RUN addgroup --gid 10000 python \
 && useradd --gid 10000 --uid 10000 python

COPY --from=install /opt/venv /opt/venv

ENV PYAPP_ENV=production \
    PYAPP_CONFIG_PATH=/usr/src/app/config \
    PORT=8080

EXPOSE 8080

ENTRYPOINT ["/opt/venv/bin/python"]

CMD ["-m", "makenew_python_app"]

USER python

LABEL org.opencontainers.image.source https://github.com/makenew/python-app
