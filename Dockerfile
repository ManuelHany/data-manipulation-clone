FROM python:3.11-alpine3.17
LABEL maintainer="manuelhany"

ENV PYTHONBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app


RUN apk update

RUN apk add --update --no-cache \
    bash && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    musl-dev \
    python3-dev \
    openssl-dev \
    linux-headers && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        flask-user


ENV PATH="/py/bin:$PATH"

USER flask-user

