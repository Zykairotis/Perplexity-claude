# Perplexity Search Profiles Feature Guide

## Overview

The new profile feature enhances search effectiveness for coding and tech-related work by appending specific instructions to search queries. Each profile is designed to optimize the search for a particular type of task or use case.

## Available Profiles

| Profile | Description | Best For |
|---------|-------------|-----------|
| `research` | Deep research with multiple sources and detailed information | Academic research, comprehensive analysis |
| `code_analysis` | Detailed code analysis with logic explanations and improvements | Code review, understanding algorithms |
| `troubleshooting` | Step-by-step troubleshooting with solutions and prevention | Debugging, fixing technical issues |
| `documentation` | Comprehensive documentation with examples and guidelines | Writing technical docs, API references |
| `architecture` | Architectural analysis with design patterns and scalability | System design, technical architecture |
| `security` | Security evaluation with vulnerability identification | Security audits, vulnerability assessment |
| `performance` | Performance analysis with optimization recommendations | Performance tuning, optimization |
| `tutorial` | Step-by-step tutorials with examples and exercises | Learning new technologies, creating guides |
| `comparison` | Detailed comparisons with pros/cons and recommendations | Technology selection, tool comparison |
| `trending` | Latest trends and emerging technologies | Staying current, technology trends |
| `best_practices` | Industry best practices and coding standards | Professional development, standards |
| `integration` | Integration guidance with compatibility considerations | API integration, system integration |
| `debugging` | Systematic debugging with tools and techniques | Finding and fixing bugs |
| `optimization` | Specific optimizations with measurable improvements | Code optimization, performance tuning |

## Usage Examples

### MCP Tools

```python
# Using search_perplexity with profile
result = await mcp.search_perplexity(
    query="React hooks optimization",
    profile="code_analysis",
    mode="pro",
    model="claude 3.7 sonnet"
)

# Using chat_with_perplexity with profile
result = await mcp.chat_with_perplexity(
    message="How do I fix Docker connection issues?",
    profile="troubleshooting",
    mode="auto"
)

# Using file analysis with profile
result = await mcp.analyze_file_with_perplexity(
    file_content="def fibonacci(n): ...",
    file_type="python",
    query="Explain this implementation and suggest improvements",
    profile="code_analysis"
)

# Get available profiles
profiles = await mcp.get_search_profiles()
```

### API Usage

```python
# Using PerplexityAPI directly
from perplexity_api import PerplexityAPI
from perplexity_profiles import SearchProfile

api = PerplexityAPI()

result = await api.search(
    query="microservices architecture patterns",
    profile=SearchProfile.ARCHITECTURE,
    mode="pro"
)
```

### HTTP API

```bash
# REST API call with profile
curl -X POST "http://localhost:9522/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "blockchain technology trends",
    "profile": "trending",
    "mode": "pro",
    "sources": ["web", "scholar"]
  }'

# Get available profiles
curl "http://localhost:9522/api/profiles"
```

## Profile Enhancements

### Research Profile Example

**Original Query:** "machine learning algorithms"

**Enhanced Query:** "machine learning algorithms. do a detailed research on this and provide me with most recent information about this be very detailed about it also make sure u are reffering to multiple sources like this"

### Code Analysis Profile Example

**Original Query:** "React hooks implementation"

**Enhanced Query:** "React hooks implementation. analyze this code in detail, explain the logic, identify potential issues, suggest improvements, and provide best practices for this type of implementation"

### Troubleshooting Profile Example

**Original Query:** "database connection timeout"

**Enhanced Query:** "database connection timeout. help me troubleshoot this issue step by step, identify common causes, provide solutions, and include preventative measures for similar problems"

## Integration Points

The profile feature is integrated at multiple layers:

1. **Core Layer**: `perplexity_profiles.py` - Profile definitions and utilities
2. **API Wrapper Layer**: `perplexity_api.py` - Profile parameter in search methods
3. **MCP Layer**: `simple_perplexity_mcp.py` - Profile support in all tools
4. **Server Layer**: `server.py` - HTTP API endpoints with profile support

## Error Handling

Invalid profiles are validated and provide helpful error messages with available options:

```json
{
  "error": "Invalid profile 'invalid_profile'. Available profiles: ['research', 'code_analysis', 'troubleshooting', ...]"
}
```

## Best Practices

1. **Choose the right profile** for your specific use case
2. **Combine with appropriate modes** (pro for complex analysis, auto for general queries)
3. **Use with specific models** for best results (e.g., Claude for code analysis)
4. **Test different profiles** to find the most effective one for your needs

## Implementation Details

The profile system works by:

1. **Validating** the provided profile name
2. **Retrieving** the profile-specific instruction template
3. **Appending** the instruction to the original query
4. **Passing** the enhanced query to the underlying search engine

This approach ensures compatibility with existing code while adding powerful query enhancement capabilities.