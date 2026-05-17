#!/bin/bash
echo "Building project..."
# Use uv to sync dependencies from requirements.txt
uv pip sync requirements.txt
# Collect static files for deployment
python3 manage.py collectstatic --noinput --clear
echo "Build complete."