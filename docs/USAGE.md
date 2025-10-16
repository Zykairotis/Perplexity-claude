# Perplexity AI CLI - Usage Guide

A powerful command-line interface for Perplexity AI with real-time streaming search results.

## 🚀 Installation

1. **Install dependencies:**
   ```bash
   uv pip install click rich curl-cffi
   ```

2. **Make CLI executable:**
   ```bash
   chmod +x perplexity_cli.py
   ```

## 📋 Commands Overview

```bash
python perplexity_cli.py --help
```

### Available Commands:
- `search` - Perform a search query
- `interactive` - Start interactive mode
- `init` - Initialize cookies configuration file

## 🔍 Basic Search

### Simple Search
```bash
python perplexity_cli.py search "What is artificial intelligence?"
```

### Search with Streaming (Default)
```bash
python perplexity_cli.py search "Latest developments in quantum computing"
```

### Non-Streaming Search
```bash
python perplexity_cli.py search "Python programming basics" --no-stream
```

## ⚙️ Advanced Options

### Search Modes
```bash
# Auto mode (default)
python perplexity_cli.py search "What is blockchain?" --mode auto

# Pro mode with specific model
python perplexity_cli.py search "Explain machine learning" --mode pro --model sonar

# Reasoning mode
python perplexity_cli.py search "Solve this math problem: 2x + 5 = 15" --mode reasoning --model r1

# Deep research mode
python perplexity_cli.py search "Climate change impact analysis" --mode "deep research"
```

### Available Models by Mode:
- **Auto**: None (uses default)
- **Pro**: `sonar`, `gpt-4.5`, `gpt-4o`, `claude 3.7 sonnet`, `gemini 2.0 flash`, `grok-2`
- **Reasoning**: `r1`, `o3-mini`, `claude 3.7 sonnet`
- **Deep Research**: None (uses default)

### Search Sources
```bash
# Web search (default)
python perplexity_cli.py search "Latest news" --sources web

# Academic search
python perplexity_cli.py search "Research on AI ethics" --sources scholar

# Social media search
python perplexity_cli.py search "Public opinion on climate change" --sources social

# Multiple sources
python perplexity_cli.py search "COVID-19 research" --sources web --sources scholar
```

## 🍪 Cookie Configuration

### Method 1: Use Default Cookies (Built-in)
The CLI comes with default cookies that work for basic searches.

### Method 2: Create Custom Cookies File
```bash
# Generate cookies template
python perplexity_cli.py init --output my_cookies.json

# Use custom cookies
python perplexity_cli.py search "Your query" --cookies-file my_cookies.json
```

### Method 3: Update Default Cookies
Edit the `DEFAULT_COOKIES` dictionary in `perplexity_cli.py` with your browser cookies.

## 🎯 Interactive Mode

Start an interactive session for multiple queries:

```bash
python perplexity_cli.py interactive
```

In interactive mode:
- Type your queries and press Enter
- Type `quit`, `exit`, or `q` to exit
- Use Ctrl+C to interrupt

Example session:
```
Perplexity AI Interactive Mode
Type your queries or 'quit' to exit

❯ What is the weather today?
[Streaming search results...]

❯ Explain quantum physics
[Streaming search results...]

❯ quit
Goodbye!
```

## 📊 Output Formats

### Streaming Mode (Default)
- Real-time updates with progress indicators
- Live answer generation
- Source citations as they're found
- Rich formatting with colors and panels

### Non-Streaming Mode
- Complete results after search finishes
- Formatted answer in a panel
- Sources displayed in a table
- Faster for simple queries

## 🛠️ Examples

### 1. Quick Question
```bash
python perplexity_cli.py search "What time is it in Tokyo?"
```

### 2. Research Query
```bash
python perplexity_cli.py search "Latest breakthroughs in renewable energy 2025" \
  --mode pro --model "claude 3.7 sonnet" --sources web --sources scholar
```

### 3. Code Help
```bash
python perplexity_cli.py search "How to implement binary search in Python" \
  --mode pro --model sonar
```

### 4. Academic Research
```bash
python perplexity_cli.py search "Machine learning applications in healthcare" \
  --sources scholar --mode "deep research"
```

### 5. Current Events
```bash
python perplexity_cli.py search "Latest tech news today" \
  --sources web --sources social
```

## 🎨 CLI Features

### Rich Output
- **Colors**: Different colors for status, answers, and sources
- **Progress**: Real-time search progress indicators
- **Panels**: Organized display with borders and titles
- **Tables**: Clean source listings with columns
- **Markdown**: Formatted answers with proper styling

### Streaming Display
- **Live Updates**: See search progress in real-time
- **Status Indicators**: 🔍 Searching, 🌐 Web Search, 📄 Sources Found, ✅ Completed
- **Dynamic Content**: Answer builds up as it's generated
- **Source Integration**: Sources appear as they're discovered

## 🔧 Troubleshooting

### Common Issues

1. **"No module named 'click'"**
   ```bash
   uv pip install click rich
   ```

2. **"Permission denied"**
   ```bash
   chmod +x perplexity_cli.py
   ```

3. **Cookie errors**
   - Update cookies in the script or use `--cookies-file`
   - Get fresh cookies from your browser

4. **Rate limiting**
   - Wait a few minutes between requests
   - Use different cookie sessions

### Getting Fresh Cookies

1. Open browser and go to https://perplexity.ai
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Copy relevant cookie values
5. Update the `DEFAULT_COOKIES` in the script

## 📝 Tips & Best Practices

### For Better Results:
- Use specific, well-formed questions
- Choose appropriate search modes for your query type
- Use academic sources for research queries
- Use pro mode with specific models for complex questions

### Performance Tips:
- Use `--no-stream` for faster simple queries
- Use streaming mode for complex research
- Interactive mode is great for exploratory research

### Cookie Management:
- Keep cookies updated for best performance
- Use separate cookie files for different accounts
- Don't share cookie files (they contain authentication data)

## 🚀 Advanced Usage

### Batch Processing
```bash
# Create a script for multiple queries
echo "What is AI?" | python perplexity_cli.py search
echo "Explain blockchain" | python perplexity_cli.py search --mode pro
```

### Integration with Other Tools
```bash
# Pipe output to file
python perplexity_cli.py search "Python tutorial" --no-stream > result.txt

# Use with grep
python perplexity_cli.py search "Linux commands" --no-stream | grep -i "file"
```

### Custom Aliases
Add to your `.bashrc` or `.zshrc`:
```bash
alias pplx="python /path/to/perplexity_cli.py search"
alias pplxi="python /path/to/perplexity_cli.py interactive"

# Usage:
pplx "What is the weather?"
pplxi  # Start interactive mode
```

## 📚 Examples by Use Case

### Student Research
```bash
python perplexity_cli.py search "Causes of World War 1" \
  --mode "deep research" --sources scholar --sources web
```

### Developer Help
```bash
python perplexity_cli.py search "React hooks best practices" \
  --mode pro --model sonar
```

### Current Events
```bash
python perplexity_cli.py search "Latest news in technology" \
  --sources web --sources social
```

### Academic Writing
```bash
python perplexity_cli.py search "Peer-reviewed studies on climate change" \
  --sources scholar --mode "deep research"
```

### Quick Facts
```bash
python perplexity_cli.py search "Population of Japan 2025" --no-stream
```

---

## 🆘 Need Help?

- Run `python perplexity_cli.py --help` for command overview
- Run `python perplexity_cli.py search --help` for search options
- Check the troubleshooting section above
- Update your cookies if you get authentication errors

Happy searching! 🎉