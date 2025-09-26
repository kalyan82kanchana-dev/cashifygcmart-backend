FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi==0.104.1 uvicorn==0.24.0 pymongo==4.6.0 motor==3.3.2 python-dotenv==1.0.0 python-multipart==0.0.6

# Copy application
COPY . .

EXPOSE 8001

CMD ["python", "index.py"]
