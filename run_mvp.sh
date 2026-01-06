#!/bin/bash
# Quick MVP runner script

echo "🚀 AI News Agent MVP"
echo "===================="
echo ""
echo "Running in fast mode (no API key required for testing)..."
echo ""

cd "$(dirname "$0")"

# Use python3 if available, fallback to python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

$PYTHON_CMD main.py --fast --days 3 --no-save
