# Backend Dockerfile - ML Model Server
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the cnnClassifier package
RUN pip install -e .

# Create necessary directories for artifacts
RUN mkdir -p artifacts/data_ingestion \
    artifacts/prepare_base_model \
    artifacts/training \
    logs \
    model

# Copy .env file if it exists
COPY .env* ./

# Expose port
EXPOSE 8080

# Set environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run Flask application
CMD ["python", "app.py"]
