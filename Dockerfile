FROM python:3.8.5-alpine as base

WORKDIR /usr/src/app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache \
      ca-certificates \
      libstdc++

FROM base as poetry

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.5

RUN apk add --no-cache \
      ca-certificates \
      curl \
      g++ \
      gcc \
      git \
      make \
      musl-dev \
      openssh-client \
      openssl-dev \
      libffi-dev

RUN pip install "poetry==$POETRY_VERSION"

FROM poetry as build

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi
COPY . ./
RUN make build

FROM poetry as install

RUN python -m venv /opt/venv
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /opt/venv/bin/pip install -r /dev/stdin
COPY --from=build /usr/src/app .
RUN /opt/venv/bin/pip install dist/*.whl

FROM base

RUN addgroup -g 1000 python \
 && adduser -D -G python -u 1000 python

COPY --from=install /opt/venv /opt/venv

ENV PYAPP_ENV=production \
    PYAPP_CONFIG_PATH=/usr/src/app/config \
    PORT=8080

EXPOSE 8080

ENTRYPOINT ["/opt/venv/bin/python"]

CMD ["-m", "makenew_python_app"]

USER python
