FROM python:3.11-slim


# System deps required for gmpy2
RUN apt-get update && \
apt-get install -y --no-install-recommends build-essential libgmp-dev && \
rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY . /app


EXPOSE 31338/tcp


CMD ["python3", "serve_tcp.py"]
