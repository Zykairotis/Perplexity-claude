# Windsurf Integration Guide

This guide shows how to integrate the Perplexity MCP Server with Windsurf IDE for enhanced AI-powered search and analysis capabilities.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Install MCP server dependencies
pip install -r requirements.txt

# Install Windsurf MCP client dependencies
pip install mcp-client
```

### 2. Configure Windsurf

Create or update your Windsurf MCP configuration file:

**Location:** `~/.windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": ["-m", "src.perplexity_mcp_server.server"],
      "cwd": "/path/to/your/Perplexity-claude/project",
      "env": {
        "PERPLEXITY_MCP_LOG_LEVEL": "INFO",
        "PERPLEXITY_MCP_DEFAULT_MODE": "pro"
      }
    }
  }
}
```

### 3. Restart Windsurf

After configuring, restart Windsurf to load the MCP server.

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PERPLEXITY_MCP_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `PERPLEXITY_MCP_PERPLEXITY_TIMEOUT` | `120` | API timeout in seconds |
| `PERPLEXITY_MCP_DEFAULT_MODE` | `pro` | Default search mode |
| `PERPLEXITY_MCP_DEFAULT_SOURCES` | `["web"]` | Default search sources |
| `PERPLEXITY_MCP_REQUIRED_MODEL` | `true` | Whether model parameter is required |
| `PERPLEXITY_MCP_REQUIRED_PROFILE` | `true` | Whether profile parameter is required |

### Advanced Configuration

For more control, create a configuration file:

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
  "max_file_size": 10485760,
  "validation": {
    "strict_mode": true,
    "sanitize_inputs": true
  }
}
```

Then reference it in your MCP config:

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": ["-m", "src.perplexity_mcp_server.server", "--config", "/path/to/config.json"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

## 🛠️ Available Tools in Windsurf

Once integrated, you'll have access to these tools in Windsurf:

### Core Search Tools

1. **`search_perplexity`** - Main search functionality
   ```
   Search for current information on any topic
   ```

2. **`chat_with_perplexity`** - Conversational AI
   ```
   Have interactive conversations with AI assistance
   ```

3. **`analyze_file_with_perplexity`** - File analysis
   ```
   Analyze code, documents, and data files
   ```

### Utility Tools

4. **`get_available_models`** - View available AI models
5. **`get_search_profiles`** - View search profiles
6. **`get_perplexity_health`** - Check API status

## 📋 Search Profiles

Choose from 14 specialized search profiles:

- **`research`** - Academic research with multiple sources
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

## 💡 Usage Examples in Windsurf

### Example 1: Research a Technical Topic

In Windsurf, you can now ask:
```
Research the latest developments in quantum computing using the search_perplexity tool with research profile and claude45sonnet model
```

### Example 2: Code Analysis

Select code and ask:
```
Analyze this Python code for bugs and security issues using analyze_file_with_perplexity with code_analysis profile
```

### Example 3: Troubleshooting

```
Help me troubleshoot Docker connection issues using search_perplexity with troubleshooting profile
```

### Example 4: Learning

```
Explain machine learning concepts step by step using chat_with_perplexity with tutorial profile
```

## 🔗 Available Resources

Access these resources directly in Windsurf:

- **`perplexity://models`** - Available models information
- **`perplexity://health`** - API health status
- **`perplexity://config`** - Server configuration
- **`perplexity://profiles`** - Search profiles information

## 🐳 Docker Integration

For Docker-based development:

```bash
# Build the image
docker build -t perplexity-mcp .

# Run with Windsurf configuration
docker run -v $(pwd)/cookies.json:/app/cookies.json \
           -v $(pwd)/src:/app/src \
           perplexity-mcp
```

Update your Windsurf config for Docker:

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "docker",
      "args": ["run", "-v", "/path/to/project:/app", "perplexity-mcp"],
      "cwd": "/app"
    }
  }
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   Ensure the working directory (cwd) is set correctly in your MCP config
   ```

2. **Cookie Authentication**
   ```
   Make sure cookies.json exists and is accessible
   Check file permissions
   ```

3. **Connection Issues**
   ```
   Use get_perplexity_health tool to check API status
   Verify Perplexity API credentials
   ```

4. **Model Not Available**
   ```
   Use get_available_models tool to see current models
   Check Perplexity subscription status
   ```

### Debug Mode

Enable debug logging:

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": ["-m", "src.perplexity_mcp_server.server", "--log-level", "DEBUG"],
      "cwd": "/path/to/project"
    }
  }
}
```

## 📚 Advanced Usage

### Custom Search Profiles

Create custom prompt templates by modifying:
- `src/perplexity_mcp_server/prompts/templates.py`
- `src/perplexity_mcp_server/prompts/manager.py`

### Adding New Tools

1. Create tool function in `src/perplexity_mcp_server/tools/`
2. Add validation in `src/perplexity_mcp_server/data/schemas.py`
3. Register in `src/perplexity_mcp_server/server.py`

### Performance Optimization

- Configure appropriate timeout values
- Use caching for repeated queries
- Monitor API usage and limits

## 🔄 Integration with Other IDEs

The same MCP server can be used with other MCP-compatible IDEs:

- **Cursor** - Similar configuration in `.cursor/mcp_config.json`
- **Claude Desktop** - Configuration in `claude_desktop_config.json`
- **Codeium** - MCP configuration in settings

## 📞 Support

For issues with Windsurf integration:

1. Check Windsurf documentation for MCP setup
2. Verify MCP server is running correctly
3. Test with simple search queries first
4. Check logs for error messages

## 🚀 Next Steps

1. Configure Windsurf with your Perplexity credentials
2. Test basic search functionality
3. Explore different search profiles
4. Integrate with your development workflow
5. Customize configuration for your needs

Enjoy enhanced AI-powered search and analysis in Windsurf! 🎉