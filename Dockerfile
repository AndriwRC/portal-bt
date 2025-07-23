FROM python:3.13-slim

# Set working directory
WORKDIR /usr/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Source code
COPY ./app ./app

# Start the FastAPI app
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
