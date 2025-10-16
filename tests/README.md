# Perplexity API Tests

This directory contains test scripts for the Perplexity API wrapper.

## Quick Start

### Basic Test
Run a simple test with default settings:
```bash
python tests/run_api.py
```

### Custom Query Test
Test with your own query:
```bash
python tests/run_api.py --query "What is quantum computing?"
```

### Streaming Test
Test the streaming functionality:
```bash
python tests/run_api.py --query "Latest AI developments" --streaming
```

### Run All Tests
Execute comprehensive test suite:
```bash
python tests/run_api.py --test-all
```

## Advanced Usage

### With Custom Mode
```bash
python tests/run_api.py --query "Explain machine learning" --mode pro
```

### With Specific Model
```bash
python tests/run_api.py --query "How does AI work?" --mode pro --model sonar
```

### With Cookies File
```bash
python tests/run_api.py --cookies-file tests/cookies.json --test-all
```

### Quiet Mode (Less Verbose)
```bash
python tests/run_api.py --quiet --test-all
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--query` | `-q` | Custom query to test |
| `--mode` | `-m` | Search mode (auto, pro, reasoning, deep research) |
| `--model` | | Model to use (sonar, claude45sonnet, gpt5, etc.) |
| `--streaming` | `-s` | Use streaming search |
| `--test-all` | `-a` | Run all tests |
| `--quiet` | | Reduce output verbosity |
| `--cookies-file` | | Path to JSON file containing cookies |

## Available Modes

- **auto**: Automatic mode selection
- **pro**: Pro mode with advanced models
- **reasoning**: Reasoning mode for complex queries
- **deep research**: Deep research mode

## Available Models (Pro Mode)

- `sonar` - Sonar model
- `claude45sonnet` - Claude 4.5 Sonnet
- `claude45sonnetthinking` - Claude 4.5 Sonnet with thinking
- `gpt5` - GPT-5
- `gpt5thinking` - GPT-5 with thinking
- `grok-2` - Grok 2

## Search Profiles

The API supports various search profiles for enhanced results:
- `research` - Detailed research
- `code_analysis` - Code review and analysis
- `troubleshooting` - Step-by-step problem solving
- `documentation` - Comprehensive documentation
- `architecture` - Design patterns and scalability
- `security` - Security assessment
- `performance` - Performance optimization

## Setting Up Cookies

1. Copy the template:
   ```bash
   cp tests/cookies.example.json tests/cookies.json
   ```

2. Edit `cookies.json` with your actual cookie values

3. Use with tests:
   ```bash
   python tests/run_api.py --cookies-file tests/cookies.json
   ```

## Test Coverage

The test suite covers:

1. **Basic Search** - Simple search functionality
2. **Pro Search** - Pro mode with specific models
3. **Streaming Search** - Real-time streaming responses
4. **Profile Search** - Profile-enhanced queries
5. **Different Sources** - Scholar, web, and social sources
6. **Session Info** - API session information
7. **Raw Response** - Unprocessed API responses

## Example Output

```
ℹ️  Testing basic search...
✅ Query: What is artificial intelligence?
✅ Answer length: 1234 chars
✅ Number of sources: 5
✅ Mode: auto

================================================================================
ANSWER:
================================================================================
Artificial intelligence (AI) refers to the simulation of human intelligence...
================================================================================
```

## Troubleshooting

### Import Errors
Make sure you're running from the project root:
```bash
cd /home/mewtwo/Zykairotis/Perplexity-claude
python tests/run_api.py
```

### Module Not Found
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Errors
- Check your internet connection
- Verify cookies are valid (if using authentication)
- Check rate limits

## Development

To add new tests:
1. Open `tests/run_api.py`
2. Add a new test method to the `PerplexityAPITester` class
3. Follow the pattern of existing tests
4. Add the test to the `test_all()` method

## Notes

- Tests include built-in rate limiting (1 second between tests)
- Streaming tests show real-time progress
- All tests automatically clean up resources
- Use `--quiet` for CI/CD environments
