# Dockerfile
FROM python:3.11-slim

# create user
RUN adduser --disabled-password --gecos "" ctfuser

# set working directory
WORKDIR /home/ctfuser/app

# copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy challenge files
COPY chall.py serve.py flag.txt client.py .

# fix permissions
RUN chown -R ctfuser:ctfuser /home/ctfuser/app

# switch to non-root user
USER ctfuser

# expose the correct port
EXPOSE 32548

# start the server
CMD ["python3", "serve.py"]

