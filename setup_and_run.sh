#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Botanica — Setup & Run Script
# Run this from the project root (where manage.py lives)
# ─────────────────────────────────────────────────────────────

set -e

echo ""
echo "🌿 Setting up Botanica..."
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗄️  Running migrations..."
python manage.py migrate

echo ""
echo "🌱 Seeding sample data..."
python manage.py seed_data

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete! Starting server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   Admin:    http://127.0.0.1:8000/admin/"
echo "   Journal:  http://127.0.0.1:8000/blog/"
echo "   Grimoire: http://127.0.0.1:8000/grimoire/"
echo ""
echo "   Login: admin / botanica2024"
echo ""

python manage.py runserver
