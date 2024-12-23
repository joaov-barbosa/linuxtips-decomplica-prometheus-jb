FROM python:3.8-slim

LABEL maintainer Joao Barbosa

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD python3 exporter.py
