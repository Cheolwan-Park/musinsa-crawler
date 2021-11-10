FROM python:3.8.8-alpine3.13

COPY . /crawler
WORKDIR /crawler
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev bash

RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# wait for it
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh .
RUN chmod +x ./wait-for-it.sh