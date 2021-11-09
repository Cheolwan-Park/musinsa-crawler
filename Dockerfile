FROM python:3.8.8-alpine3.13

COPY . /crawler
WORKDIR /crawler
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev

RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# Dockerize
RUN apk add --no-cache openssl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz