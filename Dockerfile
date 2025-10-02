# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY scraper.py .

# Create worksheets directory
RUN mkdir -p worksheets

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash scraper && \
    chown -R scraper:scraper /app

# Switch to non-root user
USER scraper

# Default command
CMD ["python", "scraper.py"]
