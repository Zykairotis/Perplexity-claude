# Perplexity MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with Perplexity AI, enabling advanced AI-powered search and question-answering capabilities through standardized protocols.

## 🌟 Features

### **🤖 Core AI Integration**
- **Perplexity AI Integration**: Direct access to Perplexity's powerful search and AI capabilities
- **Experimental Model Support**: Updated to use Perplexity's latest "experimental" model (formerly Sonar) with "copilot" mode
- **Multi-Model Support**: Access to Claude 4.5 Sonnet, GPT-5, Grok-4, Gemini 2.0 Flash, and more
- **Multiple Search Modes**: Auto, Pro, Reasoning, Deep Research, and Deep Lab modes

### **🔧 Advanced Features**

#### **📚 Profile System**
Enhanced search profiles for specialized use cases:
- **Research**: Detailed research with multiple sources
- **Code Analysis**: Code review, logic analysis, improvements
- **Troubleshooting**: Step-by-step issue resolution
- **Documentation**: Comprehensive setup and usage docs
- **Architecture**: Design patterns and scalability
- **Security**: Vulnerability assessment and best practices
- **Performance**: Bottlenecks and optimization strategies
- **Tutorial**: Step-by-step learning with examples
- **Comparison**: Detailed alternatives analysis
- **Trending**: Latest developments and emerging tech
- **Best Practices**: Industry standards and guidelines
- **Integration**: System compatibility and API patterns
- **Debugging**: Systematic debugging techniques
- **Optimization**: Specific performance improvements

#### **🏢 Space Management**
Create and manage Perplexity collections/spaces:
- **Space Creation**: Create dedicated knowledge bases
- **Auto-save Configuration**: Automatic space UUID management
- **Access Control**: Private, team, and public space options
- **Custom Instructions**: Define AI behavior within spaces
- **Content Storage**: Historical chats, documents, web links
- **Thread Management**: Track conversations and file uploads

#### **🔌 Webhook Integration**
Advanced external system integration:
- **HTTP Client**: Call external webhooks with authentication
- **Multiple Auth Methods**: Bearer, Basic, API Key authentication
- **Retry Logic**: Configurable retry with exponential backoff
- **Response Analysis**: AI-powered webhook response analysis
- **SSRF Protection**: Security validation for external calls
- **Combined Operations**: Webhook + AI analysis in single workflow

#### **📡 Streaming & Real-time**
Multiple streaming options for real-time responses:
- **Server-Sent Events (SSE)**: HTTP-based streaming for file uploads
- **WebSocket Streaming**: Real-time bidirectional communication
- **File Upload Streaming**: Stream responses while analyzing files
- **Progress Tracking**: Real-time status updates and completion notifications

#### **📁 File Analysis**
Advanced file processing capabilities:
- **Multi-format Support**: Text, PDF, image, code files
- **Code Analysis**: Bug detection, optimization suggestions
- **Document Understanding**: Extract insights from various file types
- **Bulk Processing**: Analyze multiple files simultaneously
- **Custom Queries**: Tailored analysis requests

### **🌐 Interface Options**
- **MCP Server Integration**: Full Model Context Protocol support for Claude Desktop
- **LiteLLM Proxy**: OpenAI-compatible API endpoints
- **CLI Chat Interface**: Interactive command-line tool with rich formatting
- **Web Interface**: Full-featured web UI at http://localhost:9522
- **REST API**: Comprehensive HTTP API with all features

### **🛠️ Development & Deployment**
- **Docker Support**: Multi-service containerized deployment
- **Cookie-based Authentication**: Secure session management
- **Async/Await Architecture**: High-performance asynchronous operations
- **Environment Configuration**: Flexible configuration via environment variables
- **Health Monitoring**: Built-in health checks and diagnostics

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Zykairotis/Perplexity-claude.git
cd Perplexity-claude
```

2. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .example.env .env
# Edit .env with your configuration
```

5. **Set up authentication**

Extract your Perplexity cookies and save them to `cookies.json`:

### 🍪 How to Get Cookies

#### Perplexity (to use your own account)
* Open [Perplexity.ai](https://perplexity.ai/) and login.
* Click `F12` or `Ctrl + Shift + I` to open inspector.
* Go to the "Network" tab in the inspector.
* Refresh the page, right-click the first request, hover on "Copy" and click "Copy as cURL (bash)".
* Now go to the [CurlConverter](https://curlconverter.com/python/) and paste your code here. The cookies dictionary will appear, copy and use it in your codes.

#### Emailnator (for account generating)
* Open [Emailnator](https://emailnator.com/) and verify you're human.
* Click `F12` or `Ctrl + Shift + I` to open inspector.
* Go to the "Network" tab in the inspector.
* Refresh the page, right-click the first request, hover on "Copy" and click "Copy as cURL (bash)".
* Now go to the [CurlConverter](https://curlconverter.com/python/) and paste your code here. The cookies dictionary will appear, copy and use it in your codes.
* Cookies for Emailnator are temporary, you need to renew them continuously.

**Save cookies to `cookies.json`:**
```json
{
  "cookies": {
    "pplx.visitor-id": "your-visitor-id",
    "pplx.session-id": "your-session-id",
    "next-auth.csrf-token": "your-csrf-token",
    "__Secure-next-auth.session-token": "your-session-token",
    "pplx.search-models-v4": "{\"research\":\"pplx_alpha\",\"search\":\"experimental\",\"studio\":\"pplx_beta\"}"
  }
}
```

**⚠️ Important Notes:**
- Never commit `cookies.json` to version control
- Cookies expire and need to be refreshed periodically
- The `pplx.search-models-v4` setting controls which models are available to your account

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000

# MCP Server Settings
MCP_SERVER_NAME=perplexity-mcp
MCP_SERVER_VERSION=0.1.0

# LiteLLM Configuration (optional)
LITELLM_PROXY_PORT=4000
```

## 💻 Usage

### 1. Running the MCP Server

Start the main MCP server:

```bash
python -m src.perplexity_mcp_server.server
```

Or use the modular version:

```bash
python src/perplexity_mcp_main.py
```

### 2. CLI Chat Interface

Launch the interactive chat interface:

```bash
python src/chat_cli.py
```

### 3. Using with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": [
        "-m",
        "src.perplexity_mcp_server.server"
      ],
      "cwd": "/path/to/Perplexity-claude"
    }
  }
}
```

### 4. Using the API Server

Start the FastAPI server:

```bash
python src/server.py
```

Access the API at `http://localhost:8000` and view documentation at `http://localhost:8000/docs`.

### 5. LiteLLM Proxy

Run the LiteLLM proxy for unified LLM access:

```bash
python src/litellm_proxy.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart with latest changes
docker-compose down && docker-compose up -d --build
```

**📝 Note:** If you have a `cookies.json` file, the Docker setup will automatically mount it. Make sure it's in the project root directory.

### Using Docker Directly

```bash
# Build image
docker build -t perplexity-mcp .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/cookies.json:/app/cookies.json:ro \
  --name perplexity-mcp \
  perplexity-mcp
```

## 📚 API Documentation

### MCP Tools

The server exposes the following MCP tools:

#### `search_perplexity`
Performs enhanced search queries using Perplexity AI with profile support.

```json
{
  "query": "What is quantum computing?",
  "mode": "pro",
  "model": "experimental",
  "profile": "research",
  "sources": ["web"],
  "language": "english",
  "max_results": 5,
  "raw_mode": false,
  "search_focus": "technical"
}
```

**Required Parameters:**
- `query`: The search question or topic
- `mode`: Always "pro"
- `model`: One of "claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "experimental"
- `profile`: Enhanced search profile ("research", "code_analysis", "troubleshooting", etc.)

#### `chat_with_perplexity`
Interactive conversational AI with context awareness.

```json
{
  "message": "Explain machine learning in simple terms",
  "mode": "pro",
  "model": "claude45sonnet",
  "profile": "research",
  "conversation_id": "optional-conversation-id",
  "temperature": 0.7
}
```

#### `analyze_file_with_perplexity`
Analyze file content with AI-powered insights.

```json
{
  "file_content": "def hello(): print('Hello World')",
  "file_type": "python",
  "query": "Find bugs and suggest improvements",
  "mode": "pro",
  "model": "claude45sonnet",
  "profile": "code_analysis"
}
```

#### `get_available_models`
List all supported Perplexity models with descriptions.

#### `get_search_profiles`
Get comprehensive list of available search profiles with use cases.

#### `get_perplexity_health`
Check API connection status and performance metrics.

### REST API Endpoints

- `POST /api/search` - Perform a search with full parameters
- `POST /api/search/files` - File upload search with multipart form data
- `POST /api/search/files/stream` - Server-Sent Events streaming search
- `GET /api/health` - Health check and system status
- `GET /api/session` - Session information and status
- `GET /api/modes` - Get available search modes and models
- `GET /api/profiles` - List available search profiles
- `POST /api/spaces/create` - Create new Perplexity space/collection
- `GET /api/spaces` - List available spaces
- `GET /` - Web interface (HTML)

### 🤖 Available Models

#### Pro Mode Models (use with `mode: "pro"`)
- `experimental` - Fast, efficient factual lookups (formerly Sonar)
- `claude45sonnet` - Balanced reasoning and explanation
- `claude45sonnetthinking` - Advanced logical reasoning
- `gpt5` - Deep analytical research
- `gpt5thinking` - Complex reasoning and critical synthesis
- `gpt-4.5` - GPT-4.5 with enhanced capabilities
- `gpt-4o` - GPT-4o multimodal model
- `claude 3.7 sonnet` - Claude 3.7 Sonnet
- `gemini 2.0 flash` - Fast multimodal responses

#### Other Modes
- **Reasoning Mode**: `r1`, `o3-mini`, `claude 3.7 sonnet`
- **Deep Research**: `pplx_alpha`
- **Deep Lab**: `pplx_beta`

#### Example Usage

**1. Direct API Usage (Port 9522)**
```bash
# Basic search with experimental model
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is artificial intelligence?",
    "mode": "pro",
    "model_preference": "experimental",
    "sources": ["web"],
    "language": "english"
  }'

# File upload search
curl -X POST http://localhost:9522/api/search/files \
  -F "query=Analyze this code" \
  -F "files=@example.py" \
  -F "mode=pro" \
  -F "model_preference=claude45sonnet"

# Streaming search (Server-Sent Events)
curl -X POST http://localhost:9522/api/search/files/stream \
  -F "query=Explain quantum computing" \
  -F "mode=pro" \
  -F "model_preference=experimental"
```

**2. LiteLLM Proxy Usage (Port 4000)**
```bash
# OpenAI-style completions
curl -X POST http://localhost:4000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "pro-experimental",
    "prompt": "What is machine learning?"
  }'

# OpenAI-style chat completions
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "pro-claude45sonnet",
    "prompt": "Explain blockchain technology"
  }'

# Model format: {mode}-{model}
# Examples: pro-experimental, pro-claude45sonnet, pro-gpt5, pro-gpt5thinking
```

**3. MCP Client Usage (Claude Desktop)**
```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": ["-m", "src.perplexity_mcp_server.server"],
      "cwd": "/path/to/Perplexity-claude"
    }
  }
}
```

**4. Health Check and Model Info**
```bash
# Check API health
curl http://localhost:9522/api/health

# Get available models and modes
curl http://localhost:9522/api/modes

# Get available profiles
curl http://localhost:9522/api/profiles
```

## 🔧 Detailed Feature Usage

### **📚 Using Search Profiles**

Enhance your searches with specialized profiles:

```bash
# Code Analysis Profile
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Optimize this React component",
    "mode": "pro",
    "model_preference": "claude45sonnet",
    "profile": "code_analysis"
  }'

# Security Assessment Profile
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Check authentication implementation",
    "mode": "pro",
    "model_preference": "experimental",
    "profile": "security"
  }'

# Research Profile (most detailed)
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Latest developments in quantum computing",
    "mode": "pro",
    "model_preference": "claude45sonnetthinking",
    "profile": "research"
  }'
```

### **🏢 Managing Spaces**

Create dedicated knowledge bases:

```bash
# Create a trading analysis space
curl -X POST http://localhost:9522/api/spaces/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Trading Analysis",
    "description": "Space for market analysis and trading strategies",
    "emoji": "📊",
    "instructions": "You are a financial analyst providing data-driven insights",
    "access": 1,
    "auto_save": true
  }'

# List configured spaces
curl http://localhost:9522/api/spaces

# Use space in search (if space is configured)
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze recent market trends",
    "mode": "pro",
    "model_preference": "experimental",
    "space": "trading-analysis"
  }'
```

### **📁 File Upload & Analysis**

Analyze files with AI:

```bash
# Single file analysis
curl -X POST http://localhost:9522/api/search/files \
  -F "query=Find bugs and suggest improvements" \
  -F "files=@src/main.py" \
  -F "mode=pro" \
  -F "model_preference=claude45sonnet" \
  -F "profile=code_analysis"

# Multiple files
curl -X POST http://localhost:9522/api/search/files \
  -F "query=Compare implementations and find the best approach" \
  -F "files=@src/app.py" \
  -F "files=@src/utils.py" \
  -F "files=@docs/api.md" \
  -F "mode=pro" \
  -F "model_preference=experimental"
```

### **📡 Streaming Responses**

Real-time streaming for long queries:

```bash
# Server-Sent Events streaming
curl -X POST http://localhost:9522/api/search/files/stream \
  -F "query=Explain blockchain technology in detail" \
  -F "mode=pro" \
  -F "model_preference=claude45sonnetthinking" \
  --no-buffer

# WebSocket streaming (use client library)
# Endpoint: ws://localhost:9522/ws/search
# Send JSON: {"query": "Your question", "mode": "pro", "model_preference": "experimental"}
```

### **🔌 Webhook Integration**

Automate external service workflows:

```bash
# Via MCP (Claude Desktop)
# Call webhook and analyze response
webhook_and_analyze(
  url="https://api.example.com/data",
  method="POST",
  body={"query": "market_data"},
  analysis_query="Analyze this market data for trading opportunities",
  perplexity_mode="pro"
)

# Via Webhook MCP Server (Port 8000)
curl -X POST http://localhost:8000/call_webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.github.com/repos",
    "method": "GET",
    "auth_type": "bearer",
    "auth_credentials": {"token": "your-token"}
  }'
```

### **💻 CLI Interface**

Interactive chat with rich formatting:

```bash
# Start CLI chat
python src/chat_cli.py

# Available commands in CLI:
# /models - Show available models
# /profiles - Show search profiles
# /help - Show help
# /quit - Exit

# Usage examples in CLI:
> What are the latest trends in AI?
> /profile research How does quantum computing work?
> /model claude45sonnet Analyze this code: print("Hello")
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_perplexity_api.py

# Run with coverage
pytest --cov=src tests/
```

## 📁 Project Structure

```
Perplexity-claude/
├── src/
│   ├── perplexity_mcp_server/    # Main MCP server implementation
│   ├── chat_cli.py               # CLI chat interface
│   ├── server.py                 # FastAPI server
│   ├── perplexity_api.py         # Perplexity API client
│   ├── litellm_proxy.py          # LiteLLM proxy server
│   └── perplexity_profiles.py    # Profile management
├── tests/                        # Test files
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # This file
```

## 🔐 Security Considerations

- **Never commit `cookies.json`** - This file contains sensitive authentication data
- **Use environment variables** for secrets and API keys
- **Restrict file permissions** on sensitive configuration files
- **Use HTTPS** in production deployments
- **Regularly rotate** authentication credentials

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (if available)
pre-commit install

# Run tests before committing
pytest
```

## 📖 Additional Documentation

- [Profile Feature Guide](PROFILE_FEATURE_GUIDE.md) - Detailed guide on using profiles
- [Windsurf Integration](WINDSURF_INTEGRATION.md) - Integration with Windsurf IDE

## 🐛 Troubleshooting

### Common Issues

**Issue: "Module not found" errors**
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

**Issue: "Authentication failed"**
- Verify your `cookies.json` file is correctly formatted
- Ensure cookies are not expired
- Re-extract cookies from your browser
- Check that `pplx.search-models-v4` cookie includes the models you want to use

**Issue: "Model not found" errors**
- The `sonar` model has been renamed to `experimental`
- Update your code to use `experimental` instead of `sonar`
- Check your `pplx.search-models-v4` cookie setting to ensure the model is available

**Issue: Docker containers can't find cookies**
- Make sure `cookies.json` is in the project root directory
- Copy cookies to running container: `docker cp cookies.json perplexity-claude-perplexity-server-1:/app/`
- Restart containers with: `docker-compose down && docker-compose up -d --build`

**Issue: "Port already in use"**
```bash
# Find and kill process using the port
lsof -ti:8000 | xargs kill -9
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for the Model Context Protocol
- [Perplexity AI](https://www.perplexity.ai/) for their powerful search capabilities
- The open-source community for various dependencies

## 📞 Support

- Open an issue for bug reports or feature requests
- Check existing issues before creating a new one
- For security issues, please email directly (do not create public issues)

## 🗺️ Roadmap

- [ ] Add more LLM provider integrations
- [ ] Implement caching for improved performance
- [ ] Add more comprehensive test coverage
- [ ] Create web UI dashboard
- [ ] Add support for streaming responses
- [ ] Implement rate limiting and quotas

## 📝 Changelog

### Recent Updates
- **🚀 Model Update**: Sonar model renamed to `experimental` with `copilot` mode support
- **🍪 Enhanced Cookie Guide**: Added detailed step-by-step instructions for extracting cookies from Perplexity.ai and Emailnator
- **🐳 Docker Improvements**: Better cookie mounting and container management
- **📚 Documentation**: Updated model listings, API endpoints, and troubleshooting guides
- **🔧 Security**: Added important notes about cookie management and model availability

### Previous Updates
- Added space/collection management functionality
- Implemented streaming support with WebSocket and SSE
- Enhanced profile system with multiple search contexts
- Added webhook integration for external API calls
- Improved Docker containerization and deployment options

---

**Note**: This project is not officially affiliated with Perplexity AI or Anthropic.