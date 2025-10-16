# Quick Examples

## Basic Usage

### 1. Simple Test
```bash
python tests/run_api.py
```

### 2. Custom Query
```bash
python tests/run_api.py --query "What is machine learning?"
```

### 3. Streaming Mode
```bash
python tests/run_api.py --streaming --query "Latest AI news"
```

### 4. Complete Test Suite
```bash
python tests/run_api.py --test-all
```

## Advanced Examples

### Pro Mode with Claude
```bash
python tests/run_api.py \
  --query "Explain quantum entanglement" \
  --mode pro \
  --model claude45sonnet
```

### Pro Mode with GPT-5
```bash
python tests/run_api.py \
  --query "How does neural network training work?" \
  --mode pro \
  --model gpt5
```

### Reasoning Mode
```bash
python tests/run_api.py \
  --query "Solve this logic puzzle: If A is true and B is false..." \
  --mode reasoning \
  --model r1
```

### With Cookies
```bash
# First, set up your cookies
cp tests/cookies.example.json tests/cookies.json
# Edit cookies.json with your actual values
# Then run:
python tests/run_api.py \
  --cookies-file tests/cookies.json \
  --test-all
```

## Programmatic Usage

You can also use the tester in your own Python scripts:

```python
import asyncio
from tests.run_api import PerplexityAPITester

async def custom_test():
    tester = PerplexityAPITester(verbose=True)
    
    try:
        # Run a basic search
        result = await tester.test_basic_search("What is AI?")
        
        # Run streaming search
        await tester.test_streaming_search("Latest tech news")
        
        # Run all tests
        await tester.test_all()
        
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(custom_test())
```

## Using the API Directly

```python
import asyncio
import sys
sys.path.insert(0, 'src')

from perplexity_api import PerplexityAPI, SearchMode, ProModel

async def main():
    api = PerplexityAPI()
    
    try:
        # Basic search
        result = await api.search("What is Python?")
        print(result.answer)
        
        # Pro search with model
        result = await api.search(
            "Explain async programming",
            mode=SearchMode.PRO,
            model=ProModel.CLAUDE_45_SONNET
        )
        print(result.answer)
        
        # Streaming search
        async for chunk in api.search_stream("Latest AI developments"):
            if chunk.step_type == "FINAL":
                print("Search complete!")
        
    finally:
        await api.close()

asyncio.run(main())
```

## Testing Different Features

### 1. Test Different Models
```bash
# Test with Sonar
python tests/run_api.py --mode pro --model sonar --query "What is AI?"

# Test with Claude
python tests/run_api.py --mode pro --model claude45sonnet --query "What is AI?"

# Test with GPT-5
python tests/run_api.py --mode pro --model gpt5 --query "What is AI?"
```

### 2. Test Streaming vs Non-Streaming
```bash
# Non-streaming
python tests/run_api.py --query "Explain quantum computing"

# Streaming
python tests/run_api.py --streaming --query "Explain quantum computing"
```

### 3. Test With Quiet Mode (for CI/CD)
```bash
python tests/run_api.py --quiet --test-all
```

## Performance Testing

```bash
# Time the execution
time python tests/run_api.py --query "Quick test"

# Run multiple queries
for query in "AI" "ML" "DL" "NLP"; do
  echo "Testing: $query"
  python tests/run_api.py --quiet --query "What is $query?"
  sleep 1
done
```

## Debugging

### Enable verbose output
```bash
python tests/run_api.py --query "Debug test"
# Verbose is on by default
```

### Get raw API response
Modify the test to use `raw_response=True`:
```python
await tester.test_raw_response("Your query")
```

### Check session info
```bash
python -c "
import asyncio
import sys
sys.path.insert(0, 'src')
from perplexity_api import PerplexityAPI

async def check():
    api = PerplexityAPI()
    info = await api.get_session_info()
    print(info)
    await api.close()

asyncio.run(check())
"
```

## Integration Examples

### Use in a Shell Script
```bash
#!/bin/bash
# ask_ai.sh

QUERY="$1"
if [ -z "$QUERY" ]; then
    echo "Usage: ./ask_ai.sh 'your question'"
    exit 1
fi

python tests/run_api.py --quiet --query "$QUERY"
```

### Use with JSON Output
Create a wrapper that outputs JSON for easy parsing:
```python
import asyncio
import json
import sys
sys.path.insert(0, 'src')

from perplexity_api import PerplexityAPI

async def main():
    api = PerplexityAPI()
    try:
        result = await api.search(sys.argv[1] if len(sys.argv) > 1 else "Test")
        print(json.dumps(result.to_dict(), indent=2))
    finally:
        await api.close()

asyncio.run(main())
```

## Common Issues and Solutions

### Issue: ModuleNotFoundError
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: Rate limiting
```bash
# Solution: Add delays between requests
python tests/run_api.py --test-all
# The script already has 1-second delays built in
```

### Issue: Timeout errors
```python
# Solution: Increase timeout in code
result = await api.search(query, timeout=120.0)  # 2 minutes
```

## Next Steps

1. ✅ Run basic test to ensure everything works
2. ✅ Try different modes and models
3. ✅ Test streaming functionality
4. ✅ Run complete test suite
5. ✅ Integrate into your application

For more information, see `tests/README.md`
