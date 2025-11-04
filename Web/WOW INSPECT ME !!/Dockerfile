# Dockerfile (no nginx)
FROM python:3.11-alpine

WORKDIR /app
COPY . /app

EXPOSE 31348
CMD ["python", "-m", "http.server", "31348", "--bind", "0.0.0.0"]
