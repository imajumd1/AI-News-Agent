#!/bin/bash
# Setup script for AI News Agent MVP

echo "🚀 Setting up AI News Agent MVP"
echo "================================"
echo ""

cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✓ pip found"
echo ""

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Run MVP (no API key needed):"
    echo "     python3 main.py --fast"
    echo ""
    echo "  2. Or with AI summaries (requires API key):"
    echo "     export OPENAI_API_KEY=your_key_here"
    echo "     python3 main.py"
    echo ""
else
    echo ""
    echo "❌ Setup failed. Please check the error messages above."
    exit 1
fi
