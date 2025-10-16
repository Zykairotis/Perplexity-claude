#!/bin/bash
# Quick test script for Perplexity API
# Usage: ./tests/quick_test.sh [query]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Perplexity API Quick Test${NC}"
echo -e "${BLUE}================================${NC}\n"

# Check if running from project root
if [ ! -f "src/perplexity_api.py" ]; then
    echo "Error: Please run this script from the project root directory"
    echo "Usage: ./tests/quick_test.sh"
    exit 1
fi

# Get query from argument or use default
QUERY="${1:-What is artificial intelligence?}"

echo -e "${GREEN}Testing query: $QUERY${NC}\n"

# Run the test
python tests/run_api.py --query "$QUERY"

echo -e "\n${GREEN}✓ Test complete!${NC}"
echo -e "\nFor more options, run: python tests/run_api.py --help"
