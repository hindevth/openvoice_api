# syntax=docker/dockerfile:1

# Base image with CUDA support for GPU acceleration
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt .
RUN pip3 install --no-cache-dir -r requirement.txt

# Copy application code
COPY app/ ./app/

# Create necessary directories
RUN mkdir -p uploads outputs_v2

# Stage for development
FROM base as development
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
CMD ["python3", "-m", "app.main"]

# Stage for production
FROM base as production
ENV PYTHONPATH=/app
# Set non-root user for security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser
# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]