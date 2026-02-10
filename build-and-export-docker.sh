#!/bin/bash
# Docker kullanarak image build ve export (Mac için)
# Air-gapped ortam için image build ve export

set -e

echo "🔨 Building images for x86_64 architecture with Docker..."

# Backend image build
echo "📦 Building backend..."
docker build --platform linux/amd64 \
  -t thy500-backend:latest \
  -f backend/Dockerfile \
  ./backend

# Frontend image build
echo "📦 Building frontend..."
docker build --platform linux/amd64 \
  -t thy500-frontend:latest \
  -f frontend/Dockerfile \
  ./frontend

# MongoDB pull
echo "📦 Pulling MongoDB..."
docker pull --platform linux/amd64 mongo:7

# Image'leri listele
echo "✅ Built images:"
docker images | grep -E "(thy500|mongo)"

# TAR dosyasına export
echo "💾 Exporting images to TAR file..."
docker save -o thy500-images.tar \
  thy500-backend:latest \
  thy500-frontend:latest \
  mongo:7

# TAR dosyası boyutunu göster
echo "📊 TAR file size:"
ls -lh thy500-images.tar

echo ""
echo "✅ Export complete! thy500-images.tar ready for transfer."
echo ""
echo "📋 Next steps:"
echo "1. Transfer thy500-images.tar to customer environment"
echo "2. Transfer docker-compose.yml to customer environment"
echo "3. Transfer .env file (if exists) to customer environment"
echo "4. Run load-and-deploy.sh on customer side"
