FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

COPY . /code
WORKDIR /code

RUN apt update && \ 
    apt -y upgrade && \ 
    pip install -r rest.requirements.txt

EXPOSE 8888