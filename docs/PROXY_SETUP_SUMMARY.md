# Perplexity Proxy Server - Setup & Usage Summary

## Overview

This document summarizes the setup and configuration of the Perplexity Proxy Server that provides OpenAI-compatible API endpoints for Perplexity AI functionality.

## System Architecture

```
Client Applications
        ↓
🌐 Proxy Server (Port 4000) - OpenAI-compatible API
        ↓
📡 Main Perplexity Server (Port 9522) - Core functionality
        ↓
🔍 Perplexity AI Services
```

## Quick Start

### 1. Start the Main Perplexity Server
```bash
# Terminal 1: Start the main server
uv run server.py
# This runs on port 9522
```

### 2. Start the Proxy Server
```bash
# Terminal 2: Start the OpenAI-compatible proxy
uv run s2.py
# This runs on port 4000
```

### 3. Test the Setup
```bash
# Test models endpoint
curl http://localhost:4000/v1/models

# Test chat completion
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "pro-sonar",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

## Available Endpoints

### OpenAI-Compatible Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/v1/models` | GET | List available models | ✅ Working |
| `/v1/chat/completions` | POST | Chat completion requests | ✅ Working |
| `/v1/completions` | POST | Text completion requests | ✅ Working |

### Double-Slash URL Support
The proxy now handles URLs with double slashes (common with some clients):
- `//v1/models` → works
- `//v1/chat/completions` → works

### Debug & Utility Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/health` | GET | Health check for both servers | ✅ Working |
| `/debug/config` | GET | Show current configuration | ✅ Working |
| `/api/tags` | GET | Ollama-style model listing | ✅ Working |
| `/docs` | GET | Interactive API documentation | ✅ Working |

## Available Models

- `pro-sonar` - Perplexity Pro with web search
- `pro-claude37sonnetthinking` - Claude 3.7 Sonnet with reasoning
- `pro-grok4` - Grok-4 model

## Fixes Applied

### 1. Missing `/v1/models` Endpoint
**Problem**: Clients expecting OpenAI API were getting 404 errors when requesting available models.

**Solution**: Added proper `/v1/models` endpoint that returns OpenAI-compatible model list.

### 2. Double-Slash URL Handling
**Problem**: Some clients were sending requests with double slashes (`//v1/models`), causing 404 errors.

**Solutions Applied**:
- Added URL normalization middleware
- Added duplicate route handlers for double-slash URLs
- Added request logging for debugging

### 3. Server Connectivity
**Problem**: Proxy couldn't connect to main Perplexity server.

**Solution**: Ensured both servers are running:
- Main server on port 9522 (`server.py`)
- Proxy server on port 4000 (`s2.py`)

### 4. Missing Dependencies
**Problem**: FastAPI middleware imports were incorrect.

**Solution**: Fixed import to use `starlette.middleware.base.BaseHTTPMiddleware`.

## Testing

### Automated Testing
Use the provided test script:
```bash
python3 test_endpoints.py
```

### Manual Testing
```bash
# Health check
curl http://localhost:4000/health

# List models
curl http://localhost:4000/v1/models

# Chat completion
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "pro-sonar",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
    "max_tokens": 100
  }'

# Test double-slash URLs
curl http://localhost:4000//v1/models
```

## Troubleshooting

### Common Issues

#### 1. 404 Errors on `/v1/models`
**Cause**: Missing endpoint or server not running.
**Solution**: Ensure proxy server (`s2.py`) is running on port 4000.

#### 2. Connection Refused or Timeout
**Cause**: Main Perplexity server not running.
**Solution**: Start main server first: `uv run server.py`

#### 3. 422 Unprocessable Entity
**Cause**: Malformed request or invalid parameters.
**Solution**: Check request format matches OpenAI API specification.

#### 4. Import Errors
**Cause**: Missing dependencies.
**Solution**: Install requirements: `pip install -r requirements.txt`

### Server Status Check

```bash
# Check if main server is running (port 9522)
curl http://localhost:9522/api/health

# Check if proxy server is running (port 4000)
curl http://localhost:4000/health

# Check processes
ps aux | grep -E "(server\.py|s2\.py)"
```

### Logs and Debugging

- Proxy server logs include request/response debugging
- Use `/debug/config` endpoint to check configuration
- Check `nohup.out` or server logs for detailed error messages

## Integration Examples

### Using with OpenAI Python Client
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="dummy-key"  # Not validated currently
)

response = client.chat.completions.create(
    model="pro-sonar",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Using with curl
```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-key" \
  -d '{
    "model": "pro-sonar",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

## Configuration

### Environment Variables (Optional)
The system uses these defaults, which can be customized:
- `DEFAULT_LANGUAGE`: "en-US"
- `DEFAULT_INCOGNITO`: false
- `DEFAULT_RAW_RESPONSE`: false
- `DEFAULT_SOURCES`: "web"

### Server Ports
- Main server: 9522 (configured in `server.py`)
- Proxy server: 4000 (configured in `s2.py`)

## Notes

- The proxy provides non-streaming responses only
- API key validation is not currently implemented
- Both servers must be running for full functionality
- The system is compatible with most OpenAI API clients
- Request logging is enabled for debugging purposes

## Next Steps

1. **Authentication**: Implement proper API key validation if needed
2. **Streaming**: Add support for streaming responses
3. **Rate Limiting**: Implement rate limiting for production use
4. **Monitoring**: Add metrics and monitoring endpoints
5. **Docker**: Use provided Docker setup for production deployment

---

*Last updated: 2025-01-27*
*Status: ✅ Fully Functional*