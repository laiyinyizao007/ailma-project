#!/bin/bash
# AILMA Test Runner Script

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}AILMA Test Runner${NC}"
echo "================================"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo -e "${GREEN}✓${NC} Activating virtual environment..."
source venv/bin/activate

# Run tests
echo -e "${GREEN}✓${NC} Running tests..."
pytest tests/ "$@"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Tests completed!${NC}"
