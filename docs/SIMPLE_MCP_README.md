# Simple Perplexity MCP Server

A clean, straightforward MCP server that provides direct access to Perplexity AI models.

## Features

- **Direct Perplexity Access**: No webhook complexity - direct model access
- **Multiple Search Modes**: auto, pro, reasoning, deep research
- **File Analysis**: Analyze file content with Perplexity AI
- **Chat Interface**: Conversational AI with continuity
- **Health Checks**: Monitor API status
- **Model Discovery**: List available models and capabilities

## Available Tools

### 1. `search_perplexity`
Search using Perplexity AI with various modes and models.

**Parameters:**
- `query` (required): The search query or question
- `mode`: Search mode (auto, pro, reasoning, deep research)
- `model`: Specific model (sonar, gpt-4o, claude 3.7 sonnet, etc.)
- `sources`: Sources to search (web, scholar, social)
- `language`: Response language
- `max_results`: Maximum number of results
- `stream`: Whether to stream the response

### 2. `chat_with_perplexity`
Chat with Perplexity AI with conversation continuity.

**Parameters:**
- `message` (required): The message or question
- `conversation_id`: Conversation ID for continuity
- `mode`: Chat mode (auto, pro, reasoning)
- `model`: Specific model to use
- `temperature`: Temperature for response generation
- `stream`: Whether to stream the response

### 3. `analyze_file_with_perplexity`
Analyze file content using Perplexity AI.

**Parameters:**
- `file_content` (required): Content of the file to analyze
- `file_type`: Type of file (text, pdf, image, etc.)
- `query` (required): What to analyze about the file
- `mode`: Analysis mode (auto, pro, deep research)
- `model`: Specific model to use

### 4. `get_available_models`
Get list of available Perplexity models and their capabilities.

### 5. `get_perplexity_health`
Check the health status of Perplexity API connection.

## Available Resources

- `perplexity://models` - Available models and capabilities
- `perplexity://health` - API health status

## Usage Examples

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "/home/mewtwo/Zykairotis/Perplexity-Unofficial-main/.venv/bin/python",
      "args": ["/home/mewtwo/Zykairotis/Perplexity-Unofficial-main/simple_perplexity_mcp.py"]
    }
  }
}
```

### Tool Usage Examples

#### Basic Search
```python
result = await session.call_tool("search_perplexity", {
    "query": "What is quantum computing?",
    "mode": "pro",
    "model": "sonar"
})
```

#### Chat with Continuity
```python
result = await session.call_tool("chat_with_perplexity", {
    "message": "Can you explain that in simpler terms?",
    "conversation_id": "conv_123",
    "mode": "pro"
})
```

#### File Analysis
```python
result = await session.call_tool("analyze_file_with_perplexity", {
    "file_content": "Your file content here...",
    "file_type": "text",
    "query": "Summarize the key points",
    "mode": "deep research"
})
```

#### Get Available Models
```python
result = await session.call_tool("get_available_models", {})
```

#### Check Health
```python
result = await session.call_tool("get_perplexity_health", {})
```

## Available Models

### Pro Mode Models
- `sonar` - Fast, efficient model
- `gpt-4.5` - Advanced GPT-4.5
- `gpt-4o` - GPT-4 Optimized
- `claude 3.7 sonnet` - Claude 3.7 Sonnet
- `gemini 2.0 flash` - Gemini 2.0 Flash
- `grok-2` - Grok 2

### Reasoning Mode Models
- `r1` - Advanced reasoning
- `o3-mini` - Efficient reasoning
- `claude 3.7 sonnet` - Claude reasoning

### Deep Research Models
- `pplx_alpha` - Comprehensive research
- `pplx_beta` - Experimental features

## Search Sources
- `web` - General web sources
- `scholar` - Academic and research papers
- `social` - Social media and forums

## Installation

1. Install dependencies:
```bash
pip install fastmcp mcp pydantic
```

2. Run the server:
```bash
python src/simple_perplexity_mcp.py
```

## Configuration

The server automatically uses the existing Perplexity API configuration from your project. No additional setup required.

## Why This Instead of the Webhook Version?

- **Simpler**: Direct model access, no webhook complexity
- **Faster**: No HTTP round trips
- **More Reliable**: Direct API calls
- **Better Integration**: Designed specifically for Perplexity models
- **Cleaner**: Focused tool set for AI agent use cases