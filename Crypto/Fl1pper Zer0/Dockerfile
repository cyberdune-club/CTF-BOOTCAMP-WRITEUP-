# Dockerfile
FROM python:3.11-slim

# create non-root user
RUN useradd -m -s /bin/bash ctf
WORKDIR /home/ctf/app

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# copy files
COPY . /home/ctf/app
RUN pip install --no-cache-dir pycryptodome fastecdsa

RUN chown -R ctf:ctf /home/ctf/app
USER ctf

EXPOSE 31337
CMD ["python3", "Challenge.py"]

