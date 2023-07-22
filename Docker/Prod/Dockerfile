FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY src /code/src/
COPY config /code/config/