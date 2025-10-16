#!/bin/bash
# Setup and test script for Perplexity API
# This script installs dependencies and runs a verification test

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Perplexity API Setup & Test${NC}"
echo -e "${BLUE}================================${NC}\n"

# Check if running from project root
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    echo "Usage: ./tests/setup_and_test.sh"
    exit 1
fi

# Step 1: Check Python version
echo -e "${YELLOW}[1/4] Checking Python version...${NC}"
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}\n"

# Step 2: Install dependencies
echo -e "${YELLOW}[2/4] Installing dependencies...${NC}"
if pip install -r requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Dependencies installed${NC}\n"
else
    echo -e "${YELLOW}⚠ Some dependencies may have failed. Continuing...${NC}\n"
fi

# Step 3: Verify imports
echo -e "${YELLOW}[3/4] Verifying imports...${NC}"
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from perplexity_api import PerplexityAPI
    print('✓ Imports successful')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"
echo ""

# Step 4: Run test
echo -e "${YELLOW}[4/4] Running verification test...${NC}"
echo -e "${BLUE}This may take a few seconds...${NC}\n"

python tests/run_api.py --query "Hello, this is a test"

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}\n"

echo -e "Next steps:"
echo -e "  • Run basic test: ${BLUE}python tests/run_api.py${NC}"
echo -e "  • Run all tests: ${BLUE}python tests/run_api.py --test-all${NC}"
echo -e "  • Quick test: ${BLUE}./tests/quick_test.sh${NC}"
echo -e "  • Help: ${BLUE}python tests/run_api.py --help${NC}\n"
