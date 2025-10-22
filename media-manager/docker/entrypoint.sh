#!/bin/bash
set -e

echo "========================================"
echo "Docker Media Manager - Starting up"
echo "========================================"

# Set user and group IDs
PUID=${PUID:-99}
PGID=${PGID:-100}

echo "Setting up user with PUID=$PUID and PGID=$PGID"

# Update user/group IDs if needed
if [ "$PUID" != "1000" ]; then
    usermod -u "$PUID" appuser
fi

if [ "$PGID" != "1000" ]; then
    groupmod -g "$PGID" appuser
fi

# Ensure proper ownership
echo "Setting permissions..."
chown -R appuser:appuser /config /downloads /media /cache /app/logs 2>/dev/null || true

# Create necessary directories
mkdir -p \
    /config/presets \
    /config/logs \
    /downloads/incomplete \
    /downloads/complete \
    /downloads/extracted \
    /downloads/quarantine \
    /media/movies \
    /media/tv \
    /cache/tmdb \
    /cache/thumbnails

# Initialize database if needed
if [ ! -f "/config/database.db" ]; then
    echo "Initializing database..."
    cd /app/backend && python -c "from app.database import init_db; init_db()"
fi

# Check for required environment variables
if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "change-me-to-a-random-secure-key" ]; then
    echo "WARNING: SECRET_KEY not set or using default. Generating random key..."
    export SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "Generated SECRET_KEY: $SECRET_KEY"
    echo "Please save this key and set it in your environment!"
fi

if [ -z "$TMDB_API_KEY" ]; then
    echo "WARNING: TMDB_API_KEY not set. TMDB features will not work."
fi

# Check FFmpeg installation
if command -v ffmpeg &> /dev/null; then
    echo "FFmpeg version: $(ffmpeg -version | head -n1)"
else
    echo "ERROR: FFmpeg not found!"
fi

# Check aria2c installation
if command -v aria2c &> /dev/null; then
    echo "aria2c version: $(aria2c --version | head -n1)"
else
    echo "ERROR: aria2c not found!"
fi

echo "========================================"
echo "Starting services..."
echo "========================================"

# Execute the main command
exec "$@"
