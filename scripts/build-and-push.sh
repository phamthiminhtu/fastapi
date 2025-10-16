#!/bin/bash

# Exit on error
set -e

# Configuration
DOCKER_USERNAME="${DOCKER_USERNAME:-tototus}"
IMAGE_NAME="${IMAGE_NAME:-fastapi-app}"
REGISTRY="${REGISTRY:-docker.io}"

# Get version from git tag or use 'latest'
if git describe --tags --exact-match 2>/dev/null; then
    VERSION=$(git describe --tags --exact-match)
else
    VERSION="latest"
fi

# Add short commit SHA as additional tag
COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "local")

# Full image names
FULL_IMAGE_NAME="${REGISTRY}/${DOCKER_USERNAME}/${IMAGE_NAME}"

echo "=========================================="
echo "Building and Pushing Docker Image"
echo "=========================================="
echo "Registry: ${REGISTRY}"
echo "Image: ${FULL_IMAGE_NAME}"
echo "Version: ${VERSION}"
echo "Commit: ${COMMIT_SHA}"
echo "=========================================="

# Build the image
echo "Building Docker image..."
docker build \
    --build-arg VERSION="${VERSION}" \
    --build-arg COMMIT_SHA="${COMMIT_SHA}" \
    -t "${FULL_IMAGE_NAME}:${VERSION}" \
    -t "${FULL_IMAGE_NAME}:${COMMIT_SHA}" \
    -t "${FULL_IMAGE_NAME}:latest" \
    .

echo "Docker image built successfully!"

# Push to registry
echo "Pushing Docker image to registry..."
docker push "${FULL_IMAGE_NAME}:${VERSION}"
docker push "${FULL_IMAGE_NAME}:${COMMIT_SHA}"
docker push "${FULL_IMAGE_NAME}:latest"

echo "=========================================="
echo "Successfully pushed:"
echo "  - ${FULL_IMAGE_NAME}:${VERSION}"
echo "  - ${FULL_IMAGE_NAME}:${COMMIT_SHA}"
echo "  - ${FULL_IMAGE_NAME}:latest"
echo "=========================================="
