# Test Setup Checklist

## ✅ Files Created

### Main Test Files
- [x] `tests/run_api.py` - Main test script with comprehensive test suite
- [x] `tests/__init__.py` - Package initialization
- [x] `tests/README.md` - Detailed documentation
- [x] `tests/EXAMPLES.md` - Quick examples and usage patterns
- [x] `tests/CHECKLIST.md` - This file
- [x] `tests/quick_test.sh` - Quick test shell script
- [x] `tests/cookies.example.json` - Cookie template

## 🚀 Quick Start

### Option 1: Basic Test
```bash
python tests/run_api.py
```

### Option 2: Using Shell Script
```bash
./tests/quick_test.sh
```

### Option 3: Custom Query
```bash
python tests/run_api.py --query "Your question here"
```

### Option 4: Full Test Suite
```bash
python tests/run_api.py --test-all
```

## 📋 Test Coverage

The test suite includes:

- ✅ **Basic Search** - Simple search functionality
- ✅ **Pro Search** - Pro mode with specific models  
- ✅ **Streaming Search** - Real-time streaming responses
- ✅ **Profile Search** - Profile-enhanced queries
- ✅ **Different Sources** - Scholar, web, and social sources
- ✅ **Session Info** - API session information
- ✅ **Raw Response** - Unprocessed API responses

## 🛠️ Features

### Command Line Interface
- ✅ Custom queries via `--query`
- ✅ Mode selection (`auto`, `pro`, `reasoning`)
- ✅ Model selection (Sonar, Claude, GPT-5, etc.)
- ✅ Streaming support via `--streaming`
- ✅ Comprehensive test suite via `--test-all`
- ✅ Quiet mode via `--quiet`
- ✅ Cookie authentication support

### Test Class Features
- ✅ Verbose/quiet output modes
- ✅ Test result tracking
- ✅ Automatic resource cleanup
- ✅ Error handling and reporting
- ✅ Summary statistics

## 📖 Documentation

- ✅ **README.md** - Complete usage guide
- ✅ **EXAMPLES.md** - Copy-paste examples
- ✅ **CHECKLIST.md** - This setup guide
- ✅ Inline code documentation
- ✅ Help text (`--help`)

## 🧪 Testing Workflow

### 1. Installation Check
```bash
# Ensure dependencies are installed
pip install -r requirements.txt
```

### 2. Basic Functionality Test
```bash
# Run a simple test to verify setup
python tests/run_api.py
```

### 3. Feature Testing
```bash
# Test streaming
python tests/run_api.py --streaming

# Test different modes
python tests/run_api.py --mode pro --model sonar

# Test with profile
python tests/run_api.py --query "How to build REST API?"
```

### 4. Comprehensive Testing
```bash
# Run all tests
python tests/run_api.py --test-all
```

## 🔧 Configuration

### Optional: Set Up Cookies
```bash
# 1. Copy the template
cp tests/cookies.example.json tests/cookies.json

# 2. Edit with your values
# Edit tests/cookies.json

# 3. Use in tests
python tests/run_api.py --cookies-file tests/cookies.json
```

## 📊 Expected Output

### Successful Test Output Example
```
ℹ️  Testing basic search...
✅ Query: What is artificial intelligence?
✅ Answer length: 1234 chars
✅ Number of sources: 5
✅ Mode: auto

================================================================================
ANSWER:
================================================================================
Artificial intelligence (AI) refers to...
================================================================================

================================================================================
TEST SUMMARY
================================================================================
Basic Search: PASS
================================================================================
Total Tests: 1
Passed: 1
Failed: 0
================================================================================
```

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| Permission denied (shell script) | Run `chmod +x tests/quick_test.sh` |
| Import errors | Run from project root directory |
| API timeout | Check internet connection |
| Rate limiting | Tests include built-in delays |

## 🎯 Next Steps

1. ✅ Verify installation: `python tests/run_api.py`
2. ⬜ Try custom queries: `python tests/run_api.py --query "Your question"`
3. ⬜ Test streaming: `python tests/run_api.py --streaming`
4. ⬜ Run full suite: `python tests/run_api.py --test-all`
5. ⬜ Integrate into your application

## 📝 Notes

- All tests automatically handle resource cleanup
- Streaming tests show real-time progress
- Built-in rate limiting (1 second between tests)
- Comprehensive error handling
- Supports both synchronous and streaming modes

## 🤝 Contributing

To add new tests:
1. Open `tests/run_api.py`
2. Add method to `PerplexityAPITester` class
3. Follow existing test patterns
4. Add to `test_all()` method if appropriate

## 📚 Additional Resources

- See `tests/README.md` for detailed usage
- See `tests/EXAMPLES.md` for code examples
- Run `python tests/run_api.py --help` for CLI options

---

**Status**: ✅ All test infrastructure ready to use!
