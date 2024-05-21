FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN apt update -y && apt upgrade -y
RUN pip3 install -r /tmp/requirements.txt

EXPOSE 8000