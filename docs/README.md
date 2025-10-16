# 🔍 Perplexity AI Unofficial API

A comprehensive Python wrapper for the Perplexity AI API with streaming support, OpenAI-compatible endpoints, conversation continuity, file uploads, and a modern web interface.

## ✨ Features

- 🚀 **Multiple API Interfaces** - OpenAI-compatible endpoints (`s2.py`), high-level Python API (`perplexity_api.py`), and low-level client (`perplexity_fixed.py`)
- 💬 **Chat Completions** - Full OpenAI-compatible chat completions API with streaming support
- 📡 **Streaming Support** - Real-time response streaming with Server-Sent Events (SSE)
- 💬 **Conversation Continuity** - Automatic conversation context management and follow-up queries
- 📁 **File Uploads** - Support for document analysis with proper S3 upload integration
- 🌐 **Web Interface** - Modern FastAPI web server with interactive UI
- 🔧 **Multiple Sources** - Web, Scholar, Social, Edgar (SEC filings)
- 🎯 **All Models** - Support for all Perplexity models (GPT-4o, Claude, Gemini, Grok, O3, R1, etc.)
- 📊 **Token Counting** - Built-in token counting and usage tracking
- 🔗 **WebSocket Support** - Real-time WebSocket connections for interactive sessions
- 🖥️ **CLI Interface** - Command-line interface for quick searches
- 🛠️ **Developer Tools** - Health checks, session info, diagnostics, and debugging utilities

## 🚀 Quick Start

## Webhook MCP Server Tools

### Available MCP Tools

1. **`call_webhook`** - Make HTTP requests to external APIs
   ```python
   {
     "url": "https://api.example.com/data",
     "method": "POST",
     "auth_type": "bearer",
     "auth_credentials": {"token": "your-token"},
     "body": {"key": "value"}
   }
   ```

2. **`analyze_with_perplexity`** - AI-powered data analysis  
   ```python
   {
     "response_data": {"user": "data"},
     "analysis_query": "What insights can you provide?",
     "perplexity_mode": "auto",
     "sources": ["web"]
   }
   ```

3. **`webhook_and_analyze`** - Combined webhook + analysis workflow
   ```python
   {
     "url": "https://api.github.com/zen",
     "method": "GET", 
     "analysis_query": "Analyze this response",
     "perplexity_mode": "auto"
   }
   ```

### Available MCP Resources

- **`webhook://config`** - Server configuration and settings
- **`webhook://stats`** - Usage statistics and performance metrics  
- **`webhook://health`** - Server health status and diagnostics

## Installation

```bash
git clone https://github.com/yourusername/perplexity-unofficial
cd perplexity-unofficial
pip install -r requirements.txt
```

### Start the Web Server

```bash
python src/server.py
```

The server will automatically find a free port (default: 52399) and provide:
- **Web Interface**: http://localhost:52399
- **API Documentation**: http://localhost:52399/docs
- **Health Check**: http://localhost:52399/health

## 📖 Usage

### 1. OpenAI-Compatible API (s2.py)

Use familiar OpenAI SDK patterns with Perplexity's power:

```python
import asyncio
from s2 import chat_completions, completions

async def main():
    # Chat completions (recommended)
    request = {
        "model": "auto",
        "messages": [
            {"role": "user", "content": "What is quantum computing?"}
        ],
        "stream": True,
        "sources": ["web", "scholar"]
    }
    
    async for chunk in chat_completions(request):
        if chunk.get("choices", [{}])[0].get("delta", {}).get("content"):
            print(chunk["choices"][0]["delta"]["content"], end="")
    
    # Text completions
    result = await completions({
        "model": "auto",
        "prompt": "Explain machine learning in simple terms",
        "max_tokens": 500
    })
    print(result["choices"][0]["text"])

asyncio.run(main())
```

### 2. High-Level Python API (perplexity_api.py)

Object-oriented interface with structured responses:

```python
import asyncio
from perplexity_api import PerplexityAPI, SearchMode, ProModel, SearchSource

async def main():
    api = PerplexityAPI()
    
    # Basic search with structured result
    result = await api.search(
        "What are the latest developments in AI?",
        mode=SearchMode.PRO,
        model=ProModel.GPT_4O,
        sources=[SearchSource.WEB, SearchSource.SCHOLAR]
    )
    
    print(f"Answer: {result.answer}")
    print(f"Sources: {len(result.sources)} found")
    print(f"Related queries: {result.related_queries}")
    
    # Streaming search
    async for chunk in api.search_stream("Explain quantum physics"):
        if chunk.step_type == "FINAL":
            print(f"Final answer: {chunk.content}")
    
    # File upload search
    with open("document.pdf", "rb") as f:
        result = await api.search(
            "Analyze this document",
            files={"document.pdf": f.read()}
        )
    
    await api.close()

asyncio.run(main())
```

### 3. Web Interface

1. Open http://localhost:52399 in your browser
2. Enter your question in the search box
3. Select sources (Web, Scholar, Social, Edgar)
4. Choose mode and model (Auto, Pro, Reasoning, Deep Research)
5. Upload files by clicking "Choose Files"
6. Click "Stream with Files" for real-time responses
7. Use "Continue Previous Chat" for follow-up questions

### 4. REST API Endpoints

#### Chat Completions (OpenAI-Compatible)
```bash
curl -X POST "http://localhost:52399/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true,
    "sources": ["web"]
  }'
```

#### Search with Files
```bash
curl -X POST "http://localhost:52399/api/search/files/stream" \
  -F "query=Analyze this document" \
  -F "mode=pro" \
  -F "model_preference=gpt-4o" \
  -F "sources=web,scholar" \
  -F "files=@document.pdf"
```

#### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:52399/ws/search');
ws.send(JSON.stringify({
    query: "What is machine learning?",
    mode: "auto",
    sources: ["web"]
}));
```

### 5. Low-Level Client (perplexity_fixed.py)

Direct client for maximum control:

```python
import asyncio
from perplexity_fixed import Client

async def main():
    client = await Client()
    
    # Non-streaming search
    result = await client.search(
        query="What is artificial intelligence?",
        mode="pro",
        model="gpt-4o",
        sources=["web", "scholar"]
    )
    
    # Streaming search
    async for chunk in client.search_stream("Latest tech news"):
        print(chunk)
    
    await client.session.close()

asyncio.run(main())
```

## 🔧 Configuration

### Available Modes
- **auto** - Automatic mode (free, fast)
- **pro** - Pro mode with advanced models (requires credits)
- **reasoning** - Reasoning mode for complex problems (requires credits)
- **deep research** - Deep research mode (requires credits)
- **deep lab** - Experimental deep lab mode (requires credits)

### Available Models

#### Pro Mode Models
- `gpt-4o` - GPT-4 Omni (recommended)
- `gpt-4.5` - GPT-4.5
- `claude 3.7 sonnet` - Claude 3.7 Sonnet
- `claude` - Claude (latest)
- `gemini 2.0 flash` - Gemini 2.0 Flash
- `grok-2` - Grok-2
- `grok4` - Grok-4
- `sonar` - Sonar (Perplexity's model)
- `pplx_pro` - PPLX Pro
- `o3` - OpenAI O3
- `experimental` - Latest experimental model

#### Reasoning Mode Models
- `pplx_reasoning` - PPLX Reasoning (default)
- `r1` - R1 Reasoning
- `o3-mini` - O3 Mini
- `claude 3.7 sonnet` - Claude 3.7 Sonnet (Thinking)

#### Research Mode Models
- `pplx_alpha` - Deep Research Alpha
- `pplx_beta` - Deep Lab Beta

### Available Sources
- **web** - General web search (default)
- **scholar** - Academic papers and research
- **social** - Social media content and discussions
- **edgar** - SEC filings and financial data

## 🌐 API Endpoints

### Core Endpoints
- `GET /` - Interactive web interface
- `GET /api` - API information and status
- `POST /api/search` - Non-streaming search
- `POST /api/search/files` - Search with file uploads
- `POST /api/search/files/stream` - Streaming search with files
- `GET /ws/search` - WebSocket search connection

### OpenAI-Compatible Endpoints
- `POST /v1/chat/completions` - Chat completions (streaming & non-streaming)
- `POST /v1/completions` - Text completions
- `GET /v1/models` - Available models list

### Utility Endpoints
- `GET /health` - Health check
- `GET /session` - Session information
- `GET /api/modes` - Available modes and models
- `GET /docs` - OpenAPI documentation

### Request Parameters

#### Common Parameters
- `query` / `prompt` (required) - Your search query or prompt
- `model` (optional) - Specific model to use
- `sources` (optional) - Array of sources to search
- `stream` (optional) - Enable streaming responses
- `max_tokens` (optional) - Maximum response tokens
- `temperature` (optional) - Response creativity (0.0-1.0)

#### File Upload Parameters
- `files` - File uploads (multipart/form-data)
- `mode` - Search mode (auto, pro, reasoning, etc.)
- `model_preference` - Preferred model for the mode
- `continue_chat` - Continue previous conversation
- `incognito` - Use incognito mode

## 📁 File Structure

```
perplexity-unofficial/
├── s2.py                   # OpenAI-compatible API endpoints
├── server.py               # FastAPI web server and REST API
├── perplexity_api.py       # High-level Python API wrapper
├── perplexity_fixed.py     # Low-level client implementation
├── requirements.txt        # Python dependencies
├── static/                 # Web interface assets
├── templates/              # HTML templates
└── README.md              # This documentation
```

### Core Components

#### s2.py - OpenAI-Compatible API
- `count_tokens()` - Token counting utility
- `parse_model()` - Model parsing and validation
- `format_messages_as_query()` - Message formatting
- `call_perplexity()` - Core API calling function
- `chat_completions()` - Chat completions endpoint
- `completions()` - Text completions endpoint
- Classes: `MessageRole`, `ToolCall`, `ChatMessage`, `Function`, `Tool`, `ResponseFormat`, `CompletionRequest`, `ChatCompletionRequest`

#### server.py - Web Server
- `home()` - Web interface handler
- `api_search*()` - Various search endpoints
- `websocket_search()` - WebSocket handler
- `health_check()` - Health monitoring
- `session_info()` - Session management
- `get_modes()` - Available modes/models

#### perplexity_api.py - High-Level API
- `PerplexityAPI` - Main API class
- `SearchResult` - Structured search results
- `StreamChunk` - Streaming response chunks
- Enums: `SearchMode`, `SearchSource`, `ProModel`, `ReasoningModel`
- Convenience functions: `quick_search()`, `search_with_sources()`, `raw_search()`

#### perplexity_fixed.py - Core Client
- `Client` - Async client with session management
- `AsyncMixin` - Async initialization helper
- File upload handling with S3 integration
- Cookie-based authentication support

## 🌟 Advanced Features

### Conversation Continuity
The system automatically manages conversation context:
```python
# First message
result1 = await api.search("Hello, what's your name?")

# Follow-up (context automatically maintained)
result2 = await api.search("What did I just ask you?", follow_up={
    'backend_uuid': result1.backend_uuid,
    'read_write_token': result1.raw_response.get('read_write_token')
})
```

### File Upload with Analysis
Support for various file types with proper handling:
```python
# Upload and analyze documents
with open("research_paper.pdf", "rb") as f:
    result = await api.search(
        "Summarize the key findings in this paper",
        files={"research_paper.pdf": f.read()},
        mode=SearchMode.PRO,
        sources=[SearchSource.SCHOLAR]
    )
```

### Token Usage Tracking
Built-in token counting and usage monitoring:
```python
from s2 import count_tokens

# Count tokens in your prompt
token_count = count_tokens("Your prompt here")
print(f"Prompt uses {token_count} tokens")

# Get session info with usage stats
session_info = await api.get_session_info()
print(f"Copilot queries remaining: {session_info['copilot_queries_remaining']}")
```

### WebSocket Real-Time Search
Interactive real-time search with WebSocket:
```javascript
const ws = new WebSocket('ws://localhost:52399/ws/search');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'chunk') {
        console.log('Stream chunk:', data.content);
    } else if (data.type === 'complete') {
        console.log('Search complete:', data.result);
    }
};

ws.send(JSON.stringify({
    query: "What's the weather like today?",
    mode: "auto",
    sources: ["web"]
}));
```

## 🛠️ Development

### Requirements
- Python 3.8+
- curl-cffi (for HTTP requests)
- FastAPI (for web server)
- uvicorn (for ASGI server)
- asyncio (for async operations)
- Other dependencies in `requirements.txt`

### Running in Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start development server with auto-reload
python src/server.py --reload

# Or use uvicorn directly
uvicorn server:app --host 0.0.0.0 --port 52399 --reload
```

### Testing the API
```bash
# Test health endpoint
curl http://localhost:52399/health

# Test session info
curl http://localhost:52399/session

# Test OpenAI-compatible endpoint
curl -X POST http://localhost:52399/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"Hello"}]}'
```

### Environment Variables
```bash
# Optional: Set custom port
export PORT=8080

# Optional: Enable debug mode
export DEBUG=true

# Optional: Set custom host
export HOST=0.0.0.0
```

## 📊 Monitoring and Debugging

### Health Check
Monitor API health and performance:
```bash
curl http://localhost:52399/health
# Returns: {"status": "healthy", "timestamp": "..."}
```

### Session Information
Check account status and usage:
```bash
curl http://localhost:52399/session
# Returns session info, remaining queries, file upload limits
```

### Available Modes and Models
Get current configuration:
```bash
curl http://localhost:52399/api/modes
# Returns all available modes, models, and sources
```

### Debug Mode
Enable raw response debugging:
```python
# Get raw API response for debugging
result = await api.search("test query", raw_response=True)
print(json.dumps(result, indent=2))
```

## ⚠️ Important Notes

- **Unofficial Implementation**: This is a reverse-engineered implementation of the Perplexity AI API
- **Authentication**: Requires valid Perplexity AI session cookies for full functionality
- **Rate Limiting**: Subject to Perplexity's rate limits and usage policies
- **Account Requirements**: Pro features require a Perplexity Pro subscription
- **File Uploads**: Uses official Perplexity S3 upload endpoints
- **Terms of Service**: Please respect Perplexity AI's terms of service

## 🔒 Authentication

### Using Cookies
Extract cookies from your browser session:
```python
cookies = {
    'pplx.visitor-id': 'your-visitor-id',
    'pplx.session-id': 'your-session-id',
    # Add other relevant cookies
}

api = PerplexityAPI(cookies=cookies)
```

### Cookie Extraction
1. Log into Perplexity AI in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Copy relevant cookie values
5. Use them in your API initialization

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Add new features or fix bugs
   - Update documentation
   - Add tests if applicable
4. **Test your changes**
   ```bash
   python -m pytest tests/
   ```
5. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Update README and documentation for new features
- Test all endpoints and functionality
- Ensure backward compatibility when possible

## 📄 License

This project is for educational and research purposes. Please respect Perplexity AI's terms of service and use responsibly.

## 🙏 Acknowledgments

- **Perplexity AI** for their innovative search capabilities
- **FastAPI** for the excellent web framework
- **curl-cffi** for reliable HTTP client functionality
- **The Open Source Community** for inspiration and tools
- **Contributors** who help improve this implementation

## 📚 Additional Resources

- [Perplexity AI Official Site](https://www.perplexity.ai)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [WebSocket API Specification](https://websockets.spec.whatwg.org/)

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

**🐛 Found a bug or have a suggestion? Please open an issue!**

**💡 Want to contribute? We'd love your help - check out our contributing guidelines above!**