FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install flask

# Copy application
COPY app.py /app/



# Expose port
EXPOSE 31350

# Run the application
CMD ["python", "app.py"]
