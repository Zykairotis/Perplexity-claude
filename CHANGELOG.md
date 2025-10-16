# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- More LLM provider integrations
- Caching for improved performance
- Web UI dashboard
- Streaming response support
- Rate limiting and quotas

## [0.1.0] - 2024-01-XX

### Added
- Initial release of Perplexity MCP Server
- Full Model Context Protocol (MCP) server implementation
- Perplexity AI integration with search and query capabilities
- Profile management system for multiple user configurations
- CLI chat interface with rich formatting
- FastAPI-based REST API server
- LiteLLM proxy support for unified LLM access
- Webhook support for external integrations
- Docker and Docker Compose support for containerized deployment
- Cookie-based authentication system
- Async/await architecture for high performance
- Comprehensive test suite with pytest
- Example usage scripts and documentation

### Security
- Cookie-based authentication for Perplexity sessions
- Environment variable configuration for sensitive data
- `.gitignore` configured to exclude sensitive files
- Docker security with non-root user

### Documentation
- README with installation and usage instructions
- Profile feature guide (PROFILE_FEATURE_GUIDE.md)
- Windsurf IDE integration guide (WINDSURF_INTEGRATION.md)
- Publishing guide for distribution
- API documentation via FastAPI automatic docs

### Infrastructure
- GitHub Actions workflows (planned)
- PyPI package structure with pyproject.toml
- Docker Hub compatible Dockerfile
- Requirements.txt for dependency management

---

## Version History

[Unreleased]: https://github.com/yourusername/Perplexity-claude/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/Perplexity-claude/releases/tag/v0.1.0