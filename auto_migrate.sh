#!/bin/bash

# Exit immediately if a command fails
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start server
echo "Starting server..."
exec "$@"