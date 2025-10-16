# Perplexity MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with Perplexity AI, enabling advanced AI-powered search and question-answering capabilities through standardized protocols.

## 🌟 Features

- **MCP Server Integration**: Full Model Context Protocol support for Claude Desktop and other MCP clients
- **Perplexity AI Integration**: Direct access to Perplexity's powerful search and AI capabilities
- **Profile Management**: Support for multiple user profiles with different configurations
- **LiteLLM Proxy**: Built-in proxy server for unified LLM access
- **CLI Chat Interface**: Interactive command-line chat interface
- **Webhook Support**: HTTP webhook endpoints for external integrations
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Cookie-based Authentication**: Secure session management using browser cookies
- **Async/Await Support**: High-performance asynchronous architecture

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Perplexity-claude.git
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
```json
{
  "session_cookie": "your_session_cookie_here",
  "other_cookies": "as_needed"
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Perplexity API Configuration
PERPLEXITY_API_KEY=your_api_key_here

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
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

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

#### `perplexity_search`
Performs a search query using Perplexity AI.

```json
{
  "query": "What is quantum computing?",
  "profile": "default"
}
```

#### `perplexity_ask`
Ask a question and get an AI-generated answer.

```json
{
  "question": "Explain machine learning in simple terms",
  "context": "optional context"
}
```

### REST API Endpoints

- `POST /api/search` - Perform a search
- `POST /api/ask` - Ask a question
- `GET /api/profiles` - List available profiles
- `POST /api/webhook` - Webhook endpoint

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

---

**Note**: This project is not officially affiliated with Perplexity AI or Anthropic.