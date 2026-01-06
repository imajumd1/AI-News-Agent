#!/bin/bash
# Start the web server

echo "🚀 Starting AI News Agent Web Server"
echo "====================================="
echo ""
echo "Server will be available at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"

# Use python3 if available, fallback to python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

$PYTHON_CMD app.py
