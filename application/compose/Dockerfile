# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && apt-get install --no-install-recommends -y python3 python3-pip python3-dev

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start \
    && chmod +x /start

WORKDIR /app