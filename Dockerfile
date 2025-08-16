# Docker configuration
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 5001
CMD ["python", "app/main.py"]
