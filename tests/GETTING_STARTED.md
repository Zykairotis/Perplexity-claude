# Getting Started with Perplexity API Tests

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Your First Test
```bash
python tests/run_api.py
```

### 3. Try a Custom Query
```bash
python tests/run_api.py --query "What is machine learning?"
```

That's it! 🎉

---

## 📦 What's Included

The test folder contains everything you need:

```
tests/
├── run_api.py                 # Main test script ⭐
├── README.md                  # Detailed documentation
├── EXAMPLES.md                # Copy-paste examples
├── GETTING_STARTED.md         # This file
├── CHECKLIST.md               # Setup verification
├── quick_test.sh             # Quick test script
├── setup_and_test.sh         # Setup + verification
├── cookies.example.json       # Cookie template
└── __init__.py               # Package file
```

---

## 🎯 Common Use Cases

### Just Want to Test a Query?
```bash
python tests/run_api.py --query "Your question here"
```

### Want to See Streaming in Action?
```bash
python tests/run_api.py --streaming --query "Latest AI news"
```

### Want to Run All Tests?
```bash
python tests/run_api.py --test-all
```

### Want Less Output?
```bash
python tests/run_api.py --quiet --query "Quick test"
```

---

## 🛠️ Setup (Detailed)

### Option 1: Automatic Setup (Recommended)
```bash
./tests/setup_and_test.sh
```
This script will:
- Check Python version
- Install dependencies
- Verify imports
- Run a test

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify installation
python -c "import sys; sys.path.insert(0, 'src'); from perplexity_api import PerplexityAPI; print('✓ Ready!')"

# 3. Run a test
python tests/run_api.py
```

---

## 📖 Usage Examples

### Basic Examples

```bash
# Default test
python tests/run_api.py

# Custom query
python tests/run_api.py --query "Explain quantum computing"

# Streaming mode
python tests/run_api.py --streaming

# All tests
python tests/run_api.py --test-all

# Quiet mode
python tests/run_api.py --quiet
```

### Advanced Examples

```bash
# Pro mode with specific model
python tests/run_api.py --mode pro --model sonar --query "What is AI?"

# Reasoning mode
python tests/run_api.py --mode reasoning --query "Solve this problem..."

# With cookies
python tests/run_api.py --cookies-file tests/cookies.json --test-all
```

### Shell Script Examples

```bash
# Quick test (uses default query)
./tests/quick_test.sh

# Quick test with custom query
./tests/quick_test.sh "What is Python?"

# Setup and run verification
./tests/setup_and_test.sh
```

---

## 🎨 Available Options

| Option | Description | Example |
|--------|-------------|---------|
| `--query` or `-q` | Custom search query | `--query "What is AI?"` |
| `--mode` or `-m` | Search mode | `--mode pro` |
| `--model` | Specific model | `--model sonar` |
| `--streaming` or `-s` | Enable streaming | `--streaming` |
| `--test-all` or `-a` | Run all tests | `--test-all` |
| `--quiet` | Reduce verbosity | `--quiet` |
| `--cookies-file` | Cookie file path | `--cookies-file cookies.json` |
| `--help` | Show help | `--help` |

---

## 🎭 Available Modes

- **auto** - Automatic mode selection (default)
- **pro** - Pro mode with advanced models
- **reasoning** - Reasoning mode for complex queries
- **deep research** - Deep research mode

---

## 🤖 Available Models

### Pro Mode Models
- `sonar` - Fast and efficient
- `claude45sonnet` - Claude 4.5 Sonnet
- `claude45sonnetthinking` - Claude with reasoning
- `gpt5` - GPT-5
- `gpt5thinking` - GPT-5 with reasoning
- `grok-2` - Grok 2

### Reasoning Mode Models
- `r1` - Reasoning model
- `o3-mini` - O3 Mini

---

## 🔧 Configuration

### Optional: Cookie Authentication

1. **Create cookie file:**
   ```bash
   cp tests/cookies.example.json tests/cookies.json
   ```

2. **Edit with your values:**
   ```json
   {
     "pplx.visitor-id": "your-visitor-id",
     "pplx.session-id": "your-session-id"
   }
   ```

3. **Use in tests:**
   ```bash
   python tests/run_api.py --cookies-file tests/cookies.json
   ```

---

## 📊 Understanding Output

### Successful Test Output
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
```

### Test Summary
```
================================================================================
TEST SUMMARY
================================================================================
Basic Search: PASS
Pro Search: PASS
Streaming Search: PASS
...
================================================================================
Total Tests: 7
Passed: 7
Failed: 0
================================================================================
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### "Permission denied" (shell script)
**Solution:**
```bash
chmod +x tests/quick_test.sh tests/setup_and_test.sh
```

### Import errors
**Solution:** Make sure you're in the project root:
```bash
cd /home/mewtwo/Zykairotis/Perplexity-claude
python tests/run_api.py
```

### API timeouts
- Check your internet connection
- Try with a simpler query
- Verify Perplexity service status

---

## 📚 Learn More

- **Detailed Usage:** See `tests/README.md`
- **Code Examples:** See `tests/EXAMPLES.md`
- **Setup Checklist:** See `tests/CHECKLIST.md`
- **Help:** Run `python tests/run_api.py --help`

---

## ✅ Quick Verification

Run this to verify everything is working:

```bash
# Method 1: Use the setup script
./tests/setup_and_test.sh

# Method 2: Manual verification
python tests/run_api.py --query "Test query"
```

If you see a response, you're all set! ✅

---

## 🎯 Next Steps

Now that you have the test setup working:

1. ✅ Try different modes and models
2. ✅ Test streaming functionality
3. ✅ Run the full test suite
4. ✅ Integrate the API into your application
5. ✅ Read the full documentation

---

## 💡 Pro Tips

- Use `--quiet` for cleaner output
- Use `--streaming` to see real-time results
- Use `--test-all` to verify all features
- Create a `cookies.json` for authenticated requests
- Check `EXAMPLES.md` for copy-paste code snippets

---

## 🆘 Need Help?

1. Check `tests/README.md` for detailed documentation
2. Look at `tests/EXAMPLES.md` for code examples
3. Run `python tests/run_api.py --help` for options
4. Review `tests/CHECKLIST.md` for setup verification

---

**Ready to start?** Run: `python tests/run_api.py` 🚀
