#!/bin/bash
# Quick test script for Git Bash
# Usage: bash test_kite.sh

cd "$(dirname "$0")"

echo "======================================================================"
echo "Testing Kite API Connection..."
echo "======================================================================"

# Set UTF-8 encoding
export PYTHONIOENCODING=utf-8

# Use the virtual environment Python
if [ -f "venv/Scripts/python.exe" ]; then
    PYTHON="venv/Scripts/python.exe"
else
    PYTHON="python"
fi

echo "Using Python: $PYTHON"
echo ""

# Run the test
$PYTHON test_kite_api.py
