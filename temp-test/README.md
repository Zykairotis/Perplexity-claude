# Perplexity API Test Scripts

This folder contains test scripts for both Perplexity API modules.

## Files

- `test_perplexity_api.py` - Tests for the high-level API wrapper
- `test_perplexity_fixed.py` - Tests for the low-level client
- `requirements.txt` - Required dependencies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the `src/` folder with the original modules is available (this test expects to be run from the temp-test folder).

## Running Tests

### Test the API Wrapper
```bash
python test_perplexity_api.py
```

### Test the Fixed Client
```bash
python test_perplexity_fixed.py
```

## Test Coverage

### perplexity_api.py Tests
- ✅ API initialization
- ✅ Basic search (auto mode)
- ✅ Search with sources
- ✅ Pro mode search
- ✅ Streaming search
- ✅ Convenience functions
- ✅ Error handling
- ✅ Search profiles

### perplexity_fixed.py Tests
- ✅ Client initialization
- ✅ Different search modes (auto, pro, reasoning)
- ✅ Various sources (web, scholar, social)
- ✅ Streaming functionality
- ✅ File upload capability
- ✅ Error handling
- ✅ Follow-up queries

## Notes

- Tests run without authentication cookies, so some features may be limited
- Pro mode and reasoning mode tests may fail without proper authentication
- File upload tests use temporary files that are automatically cleaned up
- All tests include error handling to catch and report issues gracefully

## Authentication (Optional)

To test with full functionality, you can provide Perplexity cookies:

1. Get your cookies from browser dev tools (pplx.visitor-id, pplx.session-id, etc.)
2. Modify the test scripts to include your cookies
3. Re-run the tests for full functionality

## Troubleshooting

- If you get import errors, ensure the `src/` directory is in the correct location
- If tests fail with network errors, check your internet connection
- Some features may be rate-limited without proper authentication