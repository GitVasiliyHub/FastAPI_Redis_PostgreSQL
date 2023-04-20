# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster@sha256:b878b6e28df2998d4a473137d1a1809c1127d9aba14529c980c049eade870cef
WORKDIR /app
COPY req.txt req.txt
RUN apt-get update -y && apt-get install -y libmagic-dev
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r req.txt
COPY . .
ENV APP_CONFIG=config.yaml
USER root
CMD ["python", "app.py"]