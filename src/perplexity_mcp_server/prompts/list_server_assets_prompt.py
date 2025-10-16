"""List server assets prompt implementation for comprehensive capability overview."""

from mcp.server.fastmcp.prompts import base
from typing import List, Optional


async def list_server_assets(asset_type: str = "all", detail_level: str = "comprehensive") -> str:
    """Comprehensive overview of all available MCP server capabilities and assets."""

    try:
        # Define asset categories
        asset_categories = {
            "tools": {
                "search_perplexity": {
                    "description": "Advanced search with Perplexity AI",
                    "parameters": ["query", "mode", "model", "profile", "sources", "language"],
                    "profiles": ["research", "code_analysis", "troubleshooting", "documentation",
                               "architecture", "security", "performance", "tutorial", "comparison",
                               "trending", "best_practices", "integration", "debugging", "optimization"],
                    "use_cases": ["Research", "Information gathering", "Fact-checking", "Trend analysis"]
                },
                "chat_with_perplexity": {
                    "description": "Interactive conversation with Perplexity AI",
                    "parameters": ["message", "mode", "model", "profile", "conversation_id", "temperature"],
                    "profiles": ["same as search_perplexity"],
                    "use_cases": ["Learning", "Problem-solving", "Brainstorming", "Guidance"]
                },
                "analyze_file_with_perplexity": {
                    "description": "AI-powered file analysis and interpretation",
                    "parameters": ["file_content", "file_type", "query", "mode", "model", "profile"],
                    "profiles": ["code_analysis", "documentation", "security", "performance", "debugging"],
                    "use_cases": ["Code review", "Document analysis", "Security assessment", "Data analysis"]
                },
                "get_available_models": {
                    "description": "List available Perplexity AI models",
                    "parameters": [],
                    "profiles": [],
                    "use_cases": ["Model selection", "Capability assessment"]
                },
                "get_search_profiles": {
                    "description": "List available search profiles with descriptions",
                    "parameters": [],
                    "profiles": [],
                    "use_cases": ["Profile selection", "Strategy planning"]
                },
                "get_perplexity_health": {
                    "description": "Check Perplexity API connection and system status",
                    "parameters": [],
                    "profiles": [],
                    "use_cases": ["System monitoring", "Troubleshooting", "Performance assessment"]
                }
            },
            "resources": {
                "perplexity://models": {
                    "description": "Available AI models and their capabilities",
                    "content": "Model information, capabilities, usage recommendations"
                },
                "perplexity://health": {
                    "description": "System health and performance metrics",
                    "content": "API status, latency, performance indicators"
                },
                "perplexity://config": {
                    "description": "Current server configuration",
                    "content": "Settings, timeouts, model configurations"
                },
                "perplexity://profiles": {
                    "description": "Search profile definitions and usage",
                    "content": "Profile descriptions, use cases, best practices"
                }
            },
            "prompts": {
                "search_workshop": {
                    "description": "Guided search session with expert methodology",
                    "parameters": ["query", "profile", "context"],
                    "benefits": ["Structured search approach", "Query optimization", "Result analysis guidance"]
                },
                "consultation_session": {
                    "description": "Expert consultation for specific topics",
                    "parameters": ["topic", "expertise_area", "session_type"],
                    "benefits": ["Expert guidance", "Structured problem-solving", "Actionable recommendations"]
                },
                "file_analysis_deep_dive": {
                    "description": "Comprehensive file analysis with expert review",
                    "parameters": ["file_type", "analysis_depth", "focus_areas"],
                    "benefits": ["Thorough code review", "Quality assessment", "Improvement recommendations"]
                },
                "research_assistant": {
                    "description": "Systematic research guidance and methodology",
                    "parameters": ["research_topic", "research_type", "output_format"],
                    "benefits": ["Structured research", "Quality sources", "Comprehensive analysis"]
                },
                "list_server_assets": {
                    "description": "Complete overview of server capabilities",
                    "parameters": ["asset_type", "detail_level"],
                    "benefits": ["Capability discovery", "Usage guidance", "Asset exploration"]
                }
            }
        }

        detail_levels = {
            "summary": "High-level overview with key capabilities",
            "detailed": "Comprehensive information with parameters and use cases",
            "comprehensive": "Complete documentation with examples and best practices"
        }

        detail_desc = detail_levels.get(detail_level, detail_levels["comprehensive"])

        prompt = f"""📋 **Perplexity MCP Server - Complete Asset Overview**

**Asset Type:** {asset_type.title()}
**Detail Level:** {detail_level.title()}

**🎯 Server Information:**
- **Name:** Perplexity MCP Server
- **Version:** 1.0.0
- **Purpose:** Advanced search and AI capabilities through Perplexity AI
- **Integration:** Model Context Protocol (MCP) compatible

**📊 Overview Scope:**
{detail_desc}

"""

        if asset_type in ["all", "tools"]:
            prompt += """## 🔧 Available Tools\n\n"""

            for tool_name, tool_info in asset_categories["tools"].items():
                prompt += f"### 🛠️ `{tool_name}`\n"
                prompt += f"**Description:** {tool_info['description']}\n\n"

                if detail_level in ["detailed", "comprehensive"]:
                    if tool_info['parameters']:
                        prompt += f"**Parameters:** {', '.join(tool_info['parameters'])}\n"

                    if tool_info['profiles']:
                        if isinstance(tool_info['profiles'], list):
                            prompt += f"**Profiles:** {', '.join(tool_info['profiles'])}\n"
                        else:
                            prompt += f"**Profiles:** {tool_info['profiles']}\n"

                if detail_level == "comprehensive":
                    prompt += f"**Use Cases:**\n"
                    for use_case in tool_info['use_cases']:
                        prompt += f"- {use_case}\n"

                    # Add usage examples for key tools
                    if tool_name == "search_perplexity":
                        prompt += f"""
**Example Usage:**
```python
result = await search_perplexity(
    query="React hooks optimization techniques",
    profile="code_analysis",
    mode="pro",
    model="claude45sonnet"
)
```
"""
                    elif tool_name == "chat_with_perplexity":
                        prompt += f"""
**Example Usage:**
```python
result = await chat_with_perplexity(
    message="How do I optimize database queries?",
    profile="performance",
    conversation_id="session_123"
)
```
"""
                    elif tool_name == "analyze_file_with_perplexity":
                        prompt += f"""
**Example Usage:**
```python
result = await analyze_file_with_perplexity(
    file_content=code_content,
    file_type="python",
    query="Review this code for security vulnerabilities",
    profile="security"
)
```
"""

                prompt += "\n"

        if asset_type in ["all", "resources"]:
            prompt += """## 📚 Available Resources\n\n"""

            for resource_name, resource_info in asset_categories["resources"].items():
                prompt += f"### 📖 `{resource_name}`\n"
                prompt += f"**Description:** {resource_info['description']}\n"

                if detail_level in ["detailed", "comprehensive"]:
                    prompt += f"**Content:** {resource_info['content']}\n"

                if detail_level == "comprehensive":
                    prompt += f"""
**Access Method:**
```python
# Via MCP resource handler
resource_data = await mcp.read_resource("{resource_name}")

# Via corresponding tool (if available)
tool_data = await resource_{resource_name.replace('://', '_').replace(':', '_')}()
```
"""

                prompt += "\n"

        if asset_type in ["all", "prompts"]:
            prompt += """## 💡 Available Prompts\n\n"""

            for prompt_name, prompt_info in asset_categories["prompts"].items():
                prompt += f"### 🎯 `{prompt_name}`\n"
                prompt += f"**Description:** {prompt_info['description']}\n"

                if detail_level in ["detailed", "comprehensive"]:
                    if prompt_info['parameters']:
                        prompt += f"**Parameters:** {', '.join(prompt_info['parameters'])}\n"

                if detail_level == "comprehensive":
                    prompt += f"**Benefits:**\n"
                    for benefit in prompt_info['benefits']:
                        prompt += f"- {benefit}\n"

                    prompt += f"""
**Usage Example:**
```python
# Generate the prompt
prompt_text = await {prompt_name}(
    {', '.join([f'{param}="value"' for param in prompt_info['parameters'][:2]])}
)

# Use with chat or search tools
result = await chat_with_perplexity(
    message=prompt_text,
    profile="research"
)
```
"""

                prompt += "\n"

        # Add integration examples for comprehensive view
        if detail_level == "comprehensive":
            prompt += """## 🔗 Integration Examples\n\n

### Complete Research Workflow
```python
# 1. Start with research assistant
research_prompt = await research_assistant(
    research_topic="microservices architecture patterns",
    research_type="comprehensive",
    output_format="structured"
)

# 2. Conduct initial search
search_results = await search_perplexity(
    query="microservices design patterns best practices",
    profile="architecture",
    mode="pro"
)

# 3. Analyze specific documentation
file_analysis = await analyze_file_with_perplexity(
    file_content=architecture_doc,
    file_type="markdown",
    query="Evaluate this microservices architecture",
    profile="architecture"
)

# 4. Follow-up with expert consultation
consultation = await consultation_session(
    topic="microservices implementation challenges",
    expertise_area="technical",
    session_type="problem_solving"
)
```

### Code Review Workflow
```python
# 1. Deep file analysis
analysis_prompt = await file_analysis_deep_dive(
    file_type="python",
    analysis_depth="comprehensive",
    focus_areas="security"
)

# 2. Execute analysis
code_review = await analyze_file_with_perplexity(
    file_content=python_code,
    file_type="python",
    query=analysis_prompt,
    profile="security"
)

# 3. Follow-up discussion
follow_up = await chat_with_perplexity(
    message="Based on the security analysis, what are the top 3 priorities?",
    profile="security"
)
```

"""

        # Add usage recommendations
        prompt += """## 🎯 Usage Recommendations\n\n

**Getting Started:**
1. **Explore Capabilities:** Use this asset overview to understand available tools
2. **Check System Health:** Run `get_perplexity_health()` to verify connectivity
3. **Select Models:** Use `get_available_models()` to choose appropriate AI models
4. **Review Profiles:** Use `get_search_profiles()` to understand search strategies

**Best Practices:**
- **Choose Right Profiles:** Match profiles to your specific use cases
- **Monitor Performance:** Regularly check system health and API status
- **Combine Tools:** Use multiple tools together for comprehensive analysis
- **Provide Context:** Include relevant context in your queries for better results

**Troubleshooting:**
- **Connectivity Issues:** Check `perplexity://health` resource
- **Model Problems:** Verify model availability and capabilities
- **Search Quality:** Experiment with different profiles and parameters
- **Performance:** Monitor response times and adjust complexity as needed

"""

        prompt += f"""
**🚀 Ready to Explore!**

This Perplexity MCP server provides {len(asset_categories['tools'])} tools, {len(asset_categories['resources'])} resources, and {len(asset_categories['prompts'])} specialized prompts for comprehensive AI-powered search and analysis capabilities.

**Next Steps:**
1. Choose a tool or prompt that matches your needs
2. Check system health and model availability
3. Start with your specific use case or research question
4. Use the comprehensive search and analysis capabilities

For specific guidance on any asset, refer to the detailed documentation above or use the individual prompt generators for targeted assistance.
"""

        return prompt

    except Exception as e:
        return f"Error generating server assets overview: {str(e)}"