#!/bin/bash
# ─────────────────────────────────────────────
#  TalentMind AI  ─  Environment Setup Script
# ─────────────────────────────────────────────

set -e

echo "============================================"
echo "  TalentMind AI  ─  Environment Setup"
echo "============================================"

# Check Python version
echo "[1] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required="3.10"
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "    ✅ Python $python_version found."
else
    echo "    ❌ Python 3.10+ required. Found: $python_version"
    exit 1
fi

# Create virtual environment
echo "[2] Creating virtual environment..."
python3 -m venv venv
echo "    ✅ Virtual environment created."

# Activate virtual environment
echo "[3] Activating virtual environment..."
source venv/bin/activate
echo "    ✅ Virtual environment activated."

# Upgrade pip
echo "[4] Upgrading pip..."
pip install --upgrade pip --quiet
echo "    ✅ pip upgraded."

# Install dependencies
echo "[5] Installing dependencies..."
pip install -r requirements.txt --quiet
echo "    ✅ Dependencies installed."

# Setup .env file
echo "[6] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "    ✅ .env file created from .env.example"
    echo "    ⚠️  Please add your GOOGLE_API_KEY to .env"
else
    echo "    ℹ️  .env file already exists, skipping."
fi

# Create directories
echo "[7] Creating project directories..."
mkdir -p data/uploads data/processed data/reports data/vector_db logs
touch data/uploads/.gitkeep data/processed/.gitkeep
touch data/reports/.gitkeep data/vector_db/.gitkeep
touch logs/.gitkeep
echo "    ✅ Directories created."

# Initialize Git
echo "[8] Initializing Git repository..."
if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "chore: initial project setup - Phase 1"
    echo "    ✅ Git repository initialized."
else
    echo "    ℹ️  Git already initialized, skipping."
fi

# Initialize database
echo "[9] Initializing database..."
python scripts/init_db.py
echo "    ✅ Database initialized."

# Run tests
echo "[10] Running Phase 1 tests..."
python -m pytest tests/unit/test_validators.py -v --tb=short
echo "     ✅ Tests completed."

echo ""
echo "============================================"
echo "  Phase 1 Setup COMPLETE"
echo "============================================"
echo ""
echo "  Next Steps:"
echo "  1. Add GOOGLE_API_KEY to .env"
echo "  2. Run: streamlit run app/main.py"
echo "  3. Open: http://localhost:8501"
echo ""