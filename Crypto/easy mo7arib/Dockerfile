FROM python:3.11-slim

WORKDIR /app

# copy files
COPY enc.py .
COPY flag.txt .
COPY serve.py .

# install dependency
RUN pip install pycryptodome

EXPOSE 1337

CMD ["python3", "serve.py"]
