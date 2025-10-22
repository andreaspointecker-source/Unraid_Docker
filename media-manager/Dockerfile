# Multi-stage Docker build for Docker Media Manager

# =============================================================================
# Stage 1: Frontend Build
# =============================================================================
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# =============================================================================
# Stage 2: Backend Dependencies
# =============================================================================
FROM python:3.11-slim AS backend-deps

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 3: Final Runtime Image
# =============================================================================
FROM python:3.11-slim

# Set labels
LABEL maintainer="docker-media-manager"
LABEL description="Automated download, extraction, encoding, and media management"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # Download tools
    aria2 \
    curl \
    wget \
    # Archive extraction
    unrar \
    unzip \
    p7zip-full \
    # Video processing
    ffmpeg \
    # Media info
    mediainfo \
    # Process management
    supervisor \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create app user (non-root)
RUN useradd -m -u 1000 -s /bin/bash appuser

# Copy Python dependencies from builder
COPY --from=backend-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-deps /usr/local/bin /usr/local/bin

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create necessary directories
RUN mkdir -p \
    /config \
    /downloads/incomplete \
    /downloads/complete \
    /downloads/extracted \
    /downloads/quarantine \
    /media/movies \
    /media/tv \
    /cache/tmdb \
    /cache/thumbnails \
    /app/logs \
    && chown -R appuser:appuser /app /config /downloads /media /cache

# Copy configuration files
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/aria2.conf /etc/aria2/aria2.conf
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports
EXPOSE 8080 6800

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Volumes
VOLUME ["/config", "/downloads", "/media", "/cache"]

# Switch to non-root user
USER appuser

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
