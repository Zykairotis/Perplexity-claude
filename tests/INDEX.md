# Test Suite Index

## 📁 File Structure

```
tests/
│
├── 🚀 Quick Start
│   ├── GETTING_STARTED.md       ← Start here!
│   ├── setup_and_test.sh        ← Automated setup
│   └── quick_test.sh            ← Quick testing
│
├── 📖 Documentation
│   ├── README.md                ← Complete guide
│   ├── EXAMPLES.md              ← Code examples
│   ├── CHECKLIST.md             ← Setup verification
│   └── INDEX.md                 ← This file
│
├── 🧪 Test Scripts
│   └── run_api.py               ← Main test script
│
├── ⚙️ Configuration
│   ├── cookies.example.json     ← Cookie template
│   └── __init__.py              ← Package init
│
```

## 🎯 Where to Start

### New User?
👉 **Start with:** `GETTING_STARTED.md`

### Want Quick Test?
👉 **Run:** `./tests/quick_test.sh` or `python tests/run_api.py`

### Need Examples?
👉 **Read:** `EXAMPLES.md`

### Want Full Details?
👉 **Read:** `README.md`

### Setting Up?
👉 **Run:** `./tests/setup_and_test.sh`

## 📚 Document Guide

### GETTING_STARTED.md
- **Purpose:** Quick start guide for new users
- **Contains:** 
  - 3-step quick start
  - Basic usage examples
  - Common use cases
  - Troubleshooting
- **Best for:** First-time users

### README.md
- **Purpose:** Complete documentation
- **Contains:**
  - Detailed usage instructions
  - All command-line options
  - Configuration guide
  - Test coverage details
- **Best for:** Comprehensive reference

### EXAMPLES.md
- **Purpose:** Practical code examples
- **Contains:**
  - Copy-paste examples
  - Shell script examples
  - Programmatic usage
  - Integration patterns
- **Best for:** Learning by example

### CHECKLIST.md
- **Purpose:** Setup verification
- **Contains:**
  - File checklist
  - Feature list
  - Testing workflow
  - Configuration steps
- **Best for:** Verifying setup

## 🛠️ Script Guide

### run_api.py
- **Main test script**
- **Usage:** `python tests/run_api.py [options]`
- **Features:**
  - Custom queries
  - Multiple modes
  - Streaming support
  - Complete test suite
- **Examples:**
  ```bash
  python tests/run_api.py --query "What is AI?"
  python tests/run_api.py --test-all
  python tests/run_api.py --streaming
  ```

### quick_test.sh
- **Quick test helper**
- **Usage:** `./tests/quick_test.sh [query]`
- **Features:**
  - One-command testing
  - Optional custom query
  - Color output
- **Examples:**
  ```bash
  ./tests/quick_test.sh
  ./tests/quick_test.sh "Explain quantum computing"
  ```

### setup_and_test.sh
- **Setup automation**
- **Usage:** `./tests/setup_and_test.sh`
- **Features:**
  - Dependency installation
  - Import verification
  - Test execution
  - Status reporting
- **Run once to set everything up**

## ⚡ Quick Commands

| Task | Command |
|------|---------|
| First-time setup | `./tests/setup_and_test.sh` |
| Quick test | `./tests/quick_test.sh` |
| Basic test | `python tests/run_api.py` |
| Custom query | `python tests/run_api.py -q "query"` |
| Streaming | `python tests/run_api.py -s` |
| All tests | `python tests/run_api.py -a` |
| Help | `python tests/run_api.py --help` |

## 🎓 Learning Path

### Level 1: Beginner
1. Read `GETTING_STARTED.md`
2. Run `./tests/setup_and_test.sh`
3. Try `python tests/run_api.py`

### Level 2: Intermediate
1. Read `EXAMPLES.md`
2. Try different modes and models
3. Test streaming functionality

### Level 3: Advanced
1. Read `README.md` completely
2. Run `python tests/run_api.py --test-all`
3. Integrate into your application

## 🔍 Find What You Need

### "I want to..."

#### ...run my first test
→ `python tests/run_api.py`

#### ...test with my own query
→ `python tests/run_api.py --query "your query"`

#### ...see streaming results
→ `python tests/run_api.py --streaming`

#### ...use a specific model
→ `python tests/run_api.py --mode pro --model sonar`

#### ...run all tests
→ `python tests/run_api.py --test-all`

#### ...set up authentication
→ Edit `cookies.example.json` → save as `cookies.json`

#### ...integrate into my code
→ See `EXAMPLES.md` section "Programmatic Usage"

#### ...troubleshoot issues
→ See `GETTING_STARTED.md` section "Troubleshooting"

## 📊 Test Coverage

The test suite covers:

✅ **Basic Search** - Simple queries  
✅ **Pro Search** - Advanced models  
✅ **Streaming** - Real-time responses  
✅ **Profiles** - Enhanced queries  
✅ **Sources** - Different data sources  
✅ **Session Info** - API status  
✅ **Raw Response** - Unprocessed data  

## 🎨 Output Modes

### Verbose (default)
- Detailed progress
- Full answers
- Source information
- Test summaries

### Quiet (`--quiet`)
- Minimal output
- Results only
- Good for scripts/CI

### Streaming (`--streaming`)
- Real-time updates
- Progressive results
- Step-by-step progress

## 🔗 Quick Links

- **Main Script:** `run_api.py`
- **Getting Started:** `GETTING_STARTED.md`
- **Examples:** `EXAMPLES.md`
- **Full Docs:** `README.md`
- **Checklist:** `CHECKLIST.md`

## 💡 Tips

1. **First time?** Read `GETTING_STARTED.md`
2. **Need examples?** Check `EXAMPLES.md`
3. **Want details?** Read `README.md`
4. **Stuck?** See troubleshooting sections
5. **Quick test?** Use `./tests/quick_test.sh`

---

**Current Status:** ✅ All test files ready to use!

**Next Step:** Choose your starting point above and begin testing! 🚀
