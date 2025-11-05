FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir capstone
EXPOSE 31341
CMD ["python3", "app.py"]
