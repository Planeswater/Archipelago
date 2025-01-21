FROM python:3.11-bookworm

RUN apt update && apt install -y build-essential

COPY docker/config.yaml /usr/local/lib/config.yaml

WORKDIR /app
ENTRYPOINT cp /usr/local/lib/config.yaml /app/config.yaml && python3 WebHost.py
