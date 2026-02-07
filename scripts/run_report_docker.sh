#!/usr/bin/env bash
set -euo pipefail

# Ensure this is run from the project root
if [ ! -f "docker-compose.yml" ]; then
  echo "Please run from the project root where docker-compose.yml is located."
  exit 1
fi

echo "project version: $(python -c 'import biodiversity; print(biodiversity.__version__)')"

echo "Building Docker image (no cache)..."
docker compose build --no-cache

echo "Running report (executes notebook inside container)..."
docker compose run --rm report

echo "Executed notebook saved to biodiversity-executed.ipynb"

