# Perplexity CLI Chat Tool

A simple, lightweight command-line interface for getting answers from your Perplexity API server. Ask questions, get AI-powered responses - no complexity, no history management, just straightforward AI search.

## 🚀 Features

- **Simple Interface**: Just ask questions and get answers
- **Multiple Modes**: Auto, Pro, Reasoning, Deep Research, and Deep Lab
- **Model Selection**: Choose specific models within each mode
- **Source Control**: Search web, academic papers, social media, or SEC filings
- **Streaming Responses**: Real-time response streaming with live markdown rendering
- **Interactive & Single-Shot**: Both chat mode and one-off queries
- **No Configuration Files**: Everything via command line arguments
- **Rich Terminal UI**: Beautiful formatting with syntax highlighting

## 📦 Installation

1. **Install Dependencies**:
   ```bash
   pip install rich httpx prompt_toolkit
   ```
   
   Or if using UV (recommended):
   ```bash
   uv pip install rich httpx prompt_toolkit
   ```

2. **Make the launcher executable**:
   ```bash
   chmod +x chat
   ```

3. **Start your Perplexity API server**:
   ```bash
   python3 s2.py  # This runs on port 4000
   ```

## 🎯 Quick Start

### Interactive Chat Mode
```bash
# Start interactive chat with default settings (auto mode, web source)
./chat

# Start with Pro mode and GPT-4o
./chat --mode pro --model gpt-4o

# Use multiple sources
./chat --sources web,scholar,social
```

### Single Message Mode
```bash
# Quick question with auto mode
./chat "What is quantum computing?"

# Use Pro mode with specific model
./chat --mode pro --model gpt-4o "Explain machine learning"

# Search academic sources
./chat --sources scholar "Latest AI research"

# Use reasoning mode
./chat --mode reasoning "Solve this logic puzzle: ..."
```

## 🛠️ Usage

### Command Line Options

```bash
./chat [OPTIONS] [MESSAGE]

Options:
  --mode <mode>        Search mode (auto, pro, reasoning, deep research, deep lab)
  --model <model>      Specific model to use (must be compatible with mode)
  --sources <list>     Comma-separated sources (web,scholar,social,edgar)
  --base-url <url>     Server URL (default: http://localhost:4000)
  --no-stream          Disable streaming responses
  --help               Show help
```

### Available Modes and Models

| Mode | Available Models |
|------|------------------|
| **auto** | auto |
| **pro** | gpt-4o, gpt-4.5, claude 3.7 sonnet, claude, gemini 2.0 flash, grok-2, grok4, sonar, pplx_pro, o3, experimental |
| **reasoning** | pplx_reasoning, r1, o3-mini, claude 3.7 sonnet |
| **deep research** | pplx_alpha |
| **deep lab** | pplx_beta |

### Available Sources

- **web** - General web search (default)
- **scholar** - Academic papers and research
- **social** - Social media content and discussions  
- **edgar** - SEC filings and financial data

## 📝 Examples

### Basic Usage
```bash
# Simple question
./chat "What's the weather like today?"

# Interactive mode
./chat
Ask: Hello, what can you help me with?
# AI responds with streaming text...

Ask: Tell me about Python programming
# AI responds...

# Ctrl+D to exit
```

### Using Different Modes
```bash
# Auto mode (free, fast)
./chat "Quick question about cats"

# Pro mode with advanced models
./chat --mode pro --model gpt-4o "Complex analysis of market trends"

# Reasoning mode for complex problems
./chat --mode reasoning "Solve this step by step: If a train..."

# Deep research mode
./chat --mode "deep research" "Comprehensive analysis of climate change"
```

### Using Different Sources
```bash
# Academic research
./chat --sources scholar "Latest developments in quantum computing"

# Social media insights
./chat --sources social "What are people saying about the new iPhone?"

# Financial data
./chat --sources edgar "Apple's latest quarterly earnings"

# Multiple sources
./chat --sources web,scholar,social "AI impact on education"
```

### Model-Specific Queries
```bash
# Use Claude for creative writing
./chat --mode pro --model "claude 3.7 sonnet" "Write a short story about robots"

# Use GPT-4o for coding
./chat --mode pro --model gpt-4o "Write a Python function to sort a list"

# Use Grok for casual conversation
./chat --mode pro --model grok-2 "What's the funniest thing about programming?"
```

## ⚙️ Configuration

### Server Configuration
By default, the CLI connects to `http://localhost:4000`. You can change this:

```bash
# Different port
./chat --base-url http://localhost:8080 "Hello"

# Remote server
./chat --base-url https://your-perplexity-server.com "Hello"
```

### Response Types
```bash
# Streaming responses (default) - see text appear in real-time
./chat "Tell me about space exploration"

# Non-streaming responses - wait for complete answer
./chat --no-stream "What is machine learning?"
```

## 🎨 Interactive Mode Features

When you run `./chat` without a message, you enter interactive mode:

- **Simple Prompt**: Just type your questions at the "Ask:" prompt
- **Keyboard Shortcuts**: 
  - `Ctrl+C` to cancel current input
  - `Ctrl+D` to exit
  - Arrow keys to navigate input history
- **Live Streaming**: Watch responses appear in real-time
- **Markdown Rendering**: Code blocks, formatting, and links are beautifully displayed

## 🐛 Troubleshooting

### Server Connection Issues
```bash
# Check if server is running
curl http://localhost:4000/health

# Start the server
python3 s2.py

# Check server logs
tail -f server.log
```

### Dependencies Issues
```bash
# Install missing dependencies
pip install rich httpx prompt_toolkit

# Or with UV
uv pip install rich httpx prompt_toolkit

# Check if dependencies are available
python3 -c "import rich, httpx, prompt_toolkit; print('All good!')"
```

### Mode/Model Issues
```bash
# Check available modes
./chat --help

# Use default auto mode if unsure
./chat "test message"

# Verify model is compatible with mode
./chat --mode pro --help
```

## 💡 Tips

1. **Start Simple**: Use auto mode for most questions
2. **Use Pro Mode**: For complex queries that need advanced AI models  
3. **Choose Sources**: Scholar for research, social for trends, edgar for finance
4. **Streaming**: Keep streaming enabled for better UX
5. **Interactive Mode**: Great for extended conversations
6. **Single Shot**: Perfect for quick questions in scripts

## 🔧 Integration

### In Scripts
```bash
#!/bin/bash
# Get AI answer in a script
ANSWER=$(./chat --no-stream "What is $1?")
echo "AI says: $ANSWER"
```

### With Other Tools
```bash
# Pipe to other commands
./chat "Explain Docker" | grep -i container

# Save output
./chat "Write a Python script" > ai_script.py
```

## 🚀 Performance

- **Auto Mode**: Fast, free responses
- **Pro Mode**: Higher quality but may use credits
- **Streaming**: Better perceived performance
- **Local Server**: Minimal latency when server is local

---

**Simple. Fast. Powerful.**

Get AI-powered answers from Perplexity without the complexity. Just ask and receive.

For more information about the underlying API server, see the main project documentation.