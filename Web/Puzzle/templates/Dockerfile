
# Lightweight Python image
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create flag at runtime via env or keep the baked one
ENV PORT=31346
ENV FLAG_PATH=/app/flag.txt

EXPOSE 31346

CMD ["python", "app.py"]
