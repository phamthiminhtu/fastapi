#!/bin/bash

# Script to initialize database with migrations

set -e

echo "==================================="
echo "Database Initialization"
echo "==================================="

# Wait for database to be ready
echo "Waiting for database to be ready..."
until PGPASSWORD=postgres psql -h localhost -U postgres -d fastapi_db -c '\q' 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
alembic upgrade head

echo "==================================="
echo "Database initialized successfully!"
echo "==================================="
