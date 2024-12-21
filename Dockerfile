# Use Python slim image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    python3-dev \
    libc6-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies in stages
WORKDIR /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download and cache the model
RUN python -c "from detoxify import Detoxify; Detoxify('original', device='cpu')"

# Copy application code
COPY app/ app/
COPY .env.example .env

# Create non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser $VIRTUAL_ENV && \
    chown -R appuser:appuser /root/.cache
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
