#!/bin/bash
set -e

echo "Running admin seed..."
python -m app.scripts.seed_admin

echo "Running database seed..."
python -m app.scripts.seed_persons

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
