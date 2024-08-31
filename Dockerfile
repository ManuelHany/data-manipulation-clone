FROM python:3.8-bullseye
LABEL maintainer="manuelhany"

ENV PYTHONBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app


# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    bash \
    build-essential \
    libgl1-mesa-glx \
    libssl-dev \
    libffi-dev \
    libpng-dev \
    libjpeg-dev \
    zlib1g-dev && \
    python3 -m venv /py && \
    /py/bin/pip3 install --upgrade pip && \
    /py/bin/pip3 install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
    apt-get remove -y libpng-dev libssl-dev libjpeg-dev libffi-dev zlib1g-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home flask-user

ENV PATH="/py/bin:$PATH"

#USER flask-user
