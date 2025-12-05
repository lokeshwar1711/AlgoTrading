#!/bin/bash
# Trading System Launcher for Bash
# Run with: bash start.sh

# Set UTF-8 encoding
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Change to script directory
cd "$(dirname "$0")"

echo "======================================================================"
echo "                  ALGORITHMIC TRADING SYSTEM"
echo "======================================================================"
echo ""

# Check if venv exists
if [ -f "venv/Scripts/python.exe" ]; then
    PYTHON_CMD="venv/Scripts/python.exe"
    echo "✓ Using virtual environment"
elif [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
    echo "✓ Using virtual environment"
else
    PYTHON_CMD="python"
    echo "⚠ Virtual environment not found, using system Python"
fi

echo ""

# Run the launcher
$PYTHON_CMD start.py

echo ""
echo "Press Enter to exit..."
read
