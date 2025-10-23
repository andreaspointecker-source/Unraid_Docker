#!/bin/bash
set -e

echo "========================================"
echo "Docker Media Manager - Development Mode"
echo "========================================"

# Start aria2c in background
echo "Starting aria2c RPC server..."
aria2c --enable-rpc \
    --rpc-listen-all=false \
    --rpc-listen-port=6800 \
    --dir=/downloads/incomplete \
    --max-connection-per-server=16 \
    --split=16 \
    --min-split-size=1M \
    --continue=true \
    --check-certificate=false \
    --daemon=true

# Wait a moment for aria2c to start
sleep 2

# Check if aria2c is running
if pgrep -x "aria2c" > /dev/null; then
    echo "✓ aria2c started successfully"
else
    echo "✗ Failed to start aria2c"
    exit 1
fi

echo "Starting FastAPI application..."
echo "========================================"

# Execute the main command
exec "$@"
