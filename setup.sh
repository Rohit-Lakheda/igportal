#!/bin/bash

# IG Portal Django Project Setup Script
# This script helps set up the Django project on macOS/Linux

echo "========================================="
echo "IG Portal Django Project Setup"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"
echo "📁 Working directory: $(pwd)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "🔧 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "💡 Tip: If mysqlclient installation fails, install MySQL development libraries:"
    echo "   macOS: brew install mysql-client"
    echo "   Linux: sudo apt-get install default-libmysqlclient-dev build-essential"
    exit 1
fi
echo ""

# Check MySQL connection
echo "🔧 Checking MySQL database configuration..."
echo "💡 Make sure MySQL server is running and database 'ig2026' exists"
echo "   You can create it with: mysql -u root -p -e 'CREATE DATABASE ig2026;'"
echo ""

# Run migrations
echo "🔧 Running database migrations..."
python manage.py migrate
if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed. Please check your database configuration in igportal/settings.py"
    exit 1
fi
echo ""

# Load initial data (optional)
read -p "📦 Do you want to load initial data from fixtures? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Loading initial data..."
    python manage.py loaddata fixtures/initial_data.json
    if [ $? -eq 0 ]; then
        echo "✅ Initial data loaded successfully"
    else
        echo "⚠️  Failed to load initial data (this is optional)"
    fi
    echo ""
fi

# Create superuser
read -p "👤 Do you want to create a superuser now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
    echo ""
fi

# Collect static files
echo "🔧 Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    echo "✅ Static files collected"
else
    echo "⚠️  Static files collection had issues (you can run it manually later)"
fi
echo ""

echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo "Admin panel: http://127.0.0.1:8000/admin/"
echo ""
