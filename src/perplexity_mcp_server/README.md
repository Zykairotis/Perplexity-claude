# Perplexity MCP Server

A modular Model Context Protocol (MCP) server that provides access to Perplexity AI search capabilities with proper separation of concerns and maintainable architecture.

## 🏗️ Architecture

This server follows MCP best practices with a clean modular structure:

```
perplexity_mcp_server/
├── __init__.py              # Package initialization
├── server.py                # Main server entry point
├── config/                  # Configuration management
│   ├── __init__.py
│   └── settings.py          # Server settings and validation
├── tools/                   # MCP tools (6 total)
│   ├── __init__.py
│   ├── base.py              # Base tool classes and validation
│   ├── search.py            # Search functionality
│   ├── chat.py              # Chat/conversational AI
│   ├── file_analysis.py     # File content analysis
│   └── utils.py             # Utility tools (models, profiles, health)
├── resources/               # MCP resources (4 total)
│   ├── __init__.py
│   ├── manager.py           # Resource manager
│   └── providers.py         # Resource providers
├── prompts/                 # Prompt templates and management
│   ├── __init__.py
│   ├── manager.py           # Prompt manager
│   └── templates.py         # Pre-defined templates
├── data/                    # Data models and validation
│   ├── __init__.py
│   ├── models.py            # Pydantic data models
│   └── schemas.py           # JSON schemas
├── schemas/                 # Schema definitions
│   ├── __init__.py
│   ├── tool_schemas.py      # Tool schemas
│   └── resource_schemas.py  # Resource schemas
└── utils/                   # Utility modules
    ├── __init__.py
    ├── perplexity_client.py # Perplexity API client
    └── profile_validator.py # Profile validation
```

## 🛠️ Available Tools

### Core Search Tools
1. **`search_perplexity`** - Main search functionality with profile enhancement
2. **`chat_with_perplexity`** - Conversational AI interactions
3. **`analyze_file_with_perplexity`** - File content analysis

### Utility Tools
4. **`get_available_models`** - List available AI models
5. **`get_search_profiles`** - List available search profiles
6. **`get_perplexity_health`** - Check API health status

## 📊 Available Resources

1. **`perplexity://models`** - Available models information
2. **`perplexity://health`** - API health status
3. **`perplexity://config`** - Server configuration
4. **`perplexity://profiles`** - Search profiles information

## 🔧 Configuration

The server can be configured through:
- Environment variables (prefix: `PERPLEXITY_MCP_`)
- Configuration file (JSON)
- Command line arguments

### Environment Variables
- `PERPLEXITY_MCP_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `PERPLEXITY_MCP_PERPLEXITY_TIMEOUT` - API timeout in seconds (default: 120)
- `PERPLEXITY_MCP_DEFAULT_MODE` - Default search mode (default: "pro")
- `PERPLEXITY_MCP_DEFAULT_SOURCES` - Default sources (default: ["web"])

### Configuration File
```json
{
    "name": "perplexity",
    "version": "1.0.0",
    "log_level": "INFO",
    "perplexity_timeout": 120,
    "default_mode": "pro",
    "default_sources": ["web"],
    "required_model": true,
    "required_profile": true,
    "max_results_default": 5,
    "max_file_size": 10485760
}
```

## 🚀 Usage

### Running the Server
```bash
# Use default configuration (run from project root)
python -m src.perplexity_mcp_server.server

# Use custom configuration
python -m src.perplexity_mcp_server.server --config config.json

# Override log level
python -m src.perplexity_mcp_server.server --log-level DEBUG
```

### MCP Integration
Add to your MCP client configuration:

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

### Windsurf Integration
See [WINDSURF_INTEGRATION.md](../../../WINDSURF_INTEGRATION.md) for detailed Windsurf setup instructions.

## 🔍 Search Profiles

The server includes 14 search profiles for optimized queries:

- **`research`** - Detailed research with multiple sources
- **`code_analysis`** - Code review and analysis
- **`troubleshooting`** - Step-by-step problem solving
- **`documentation`** - Comprehensive documentation
- **`architecture`** - Design patterns and scalability
- **`security`** - Vulnerability assessment
- **`performance`** - Optimization strategies
- **`tutorial`** - Step-by-step learning
- **`comparison`** - Detailed comparisons
- **`trending`** - Latest developments
- **`best_practices`** - Industry standards
- **`integration`** - System compatibility
- **`debugging`** - Systematic debugging
- **`optimization`** - Performance improvements

## 🤖 Available Models

- **`claude45sonnet`** - Balanced reasoning and explanation
- **`claude45sonnetthinking`** - Advanced logical reasoning
- **`gpt5`** - Deep analytical research
- **`gpt5thinking`** - Complex reasoning and synthesis
- **`sonar`** - Fast, efficient factual lookups

## 📝 Example Tool Usage

```python
# Search with research profile
result = await search_perplexity(
    query="quantum computing applications",
    model="claude45sonnet",
    profile="research",
    sources=["web", "scholar"]
)

# Analyze Python code
analysis = await analyze_file_with_perplexity(
    file_content="def fibonacci(n): ...",
    file_type="python",
    query="Find bugs and suggest improvements",
    model="claude45sonnet",
    profile="code_analysis"
)

# Chat with AI
response = await chat_with_perplexity(
    message="Explain machine learning concepts",
    model="gpt5",
    profile="tutorial"
)
```

## 🧪 Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Lint code
python -m flake8 perplexity_mcp_server/
```

### Adding New Tools
1. Create tool function in `tools/` directory
2. Add validation in `data/schemas.py`
3. Register in `server.py`
4. Add tests in `tests/`

### Adding New Resources
1. Create provider class in `resources/providers.py`
2. Register in `server.py`
3. Add schema in `schemas/resource_schemas.py`

## 🔒 Security

- Input validation on all tool parameters
- Secure cookie handling for Perplexity API
- Rate limiting through Perplexity API
- No credential exposure in logs

## 📊 Monitoring

- Structured logging with configurable levels
- Health check endpoint
- Performance metrics through logs
- Error tracking and reporting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Perplexity AI](https://www.perplexity.ai/)
- [FastMCP](https://github.com/jlowin/fastmcp)