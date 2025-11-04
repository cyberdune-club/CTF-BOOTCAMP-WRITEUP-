FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN echo "FLAG{baaaaaaa3_khroof_khabza_m3amra_fake_flag}" > /flag.txt && chmod 644 /flag.txt

ENV FLASK_APP=app.py
ENV SECRET_KEY=secret_key_moroccan_2024
ENV JWT_SECRET=jwt_secret_weak
ENV PORT=8080

RUN useradd -m -u 1000 ctfuser && chown -R ctfuser:ctfuser /app
USER ctfuser

EXPOSE 8080

CMD ["python", "app.py"]
