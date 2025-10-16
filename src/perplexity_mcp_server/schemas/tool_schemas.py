"""
JSON Schema definitions for MCP tools.

Provides schemas for tool validation and documentation generation.
"""

from typing import Dict, Any


def get_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """
    Get JSON schemas for all MCP tools.

    Returns:
        Dictionary mapping tool names to their JSON schemas
    """
    return {
        "search_perplexity": {
            "type": "function",
            "function": {
                "name": "search_perplexity",
                "description": "🧩 Search using Perplexity AI (pro mode) for current, factual, or research-based answers.\n\n**Perfect for:** Technical queries, academic research, fact-checking, deep web insights\n\n**Available Models:**\n• `claude45sonnet` – balanced reasoning and explanation\n• `claude45sonnetthinking` – advanced logical reasoning\n• `gpt5` – deep analytical research\n• `gpt5thinking` – complex reasoning and critical synthesis\n• `sonar` – fast, efficient factual lookups",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search question or topic"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["pro"],
                            "default": "pro",
                            "description": "Search mode: always 'pro'"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "sonar"],
                            "description": "Specific model to use: claude45sonnet, claude45sonnetthinking, gpt5, gpt5thinking, sonar"
                        },
                        "profile": {
                            "type": "string",
                            "enum": [
                                "research", "code_analysis", "troubleshooting", "documentation",
                                "architecture", "security", "performance", "tutorial",
                                "comparison", "trending", "best_practices", "integration",
                                "debugging", "optimization"
                            ],
                            "description": "Enhances result focus - available profiles"
                        },
                        "sources": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["web", "scholar", "social"]
                            },
                            "default": ["web"],
                            "description": "Data origin (web, scholar, or social, default: web)"
                        },
                        "language": {
                            "type": "string",
                            "default": "english",
                            "description": "Response language (default: English)"
                        },
                        "max_results": {
                            "type": "integer",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 20,
                            "description": "Max number of results (default: 5)"
                        },
                        "raw_mode": {
                            "type": "boolean",
                            "default": False,
                            "description": "Return full JSON (true) or clean text answer (false, recommended)"
                        },
                        "search_focus": {
                            "type": "string",
                            "description": "Specific focus area for the search (e.g., 'technical', 'academic', 'news', default: None)"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone for context-aware responses (e.g., 'UTC', 'America/New_York', default: None)"
                        }
                    },
                    "required": ["query", "model", "profile"]
                }
            }
        },
        "chat_with_perplexity": {
            "type": "function",
            "function": {
                "name": "chat_with_perplexity",
                "description": "💬 Chat with Perplexity AI (pro mode) for interactive, context-aware explanations and reasoning.\n\n**Perfect for:** Conversational research, educational guidance, and technical Q&A\n\n**Available Models:**\n• `claude45sonnet` – detailed, balanced conversation\n• `claude45sonnetthinking` – logical and step-by-step discussions\n• `gpt5` – expert reasoning in conversation\n• `gpt5thinking` – advanced analytical discussions\n• `sonar` – fast, concise replies",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "User message or question"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["pro"],
                            "default": "pro",
                            "description": "Chat mode: always 'pro'"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "sonar"],
                            "description": "Specific model to use: claude45sonnet, claude45sonnetthinking, gpt5, gpt5thinking, sonar"
                        },
                        "profile": {
                            "type": "string",
                            "enum": [
                                "research", "code_analysis", "troubleshooting", "documentation",
                                "architecture", "security", "performance", "tutorial",
                                "comparison", "trending", "best_practices", "integration",
                                "debugging", "optimization"
                            ],
                            "description": "Enhances conversation context - available profiles"
                        },
                        "conversation_id": {
                            "type": "string",
                            "description": "Maintain context between turns"
                        },
                        "temperature": {
                            "type": "number",
                            "default": 0.7,
                            "minimum": 0.1,
                            "maximum": 1.0,
                            "description": "Controls creativity (0.1–1.0, default 0.7)"
                        },
                        "raw_mode": {
                            "type": "boolean",
                            "default": False,
                            "description": "Return full JSON (true) or clean text answer (false, recommended)"
                        },
                        "search_focus": {
                            "type": "string",
                            "description": "Specific focus area for the chat (e.g., 'technical', 'academic', 'news', default: None)"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone for context-aware responses (e.g., 'UTC', 'America/New_York', default: None)"
                        }
                    },
                    "required": ["message", "model", "profile"]
                }
            }
        },
        "analyze_file_with_perplexity": {
            "type": "function",
            "function": {
                "name": "analyze_file_with_perplexity",
                "description": "📄 Analyze and interpret file content using Perplexity AI (pro mode) for code, data, or document insights.\n\n**Perfect for:** Code review, document understanding, security checks, and data pattern extraction\n\n**Available Models:**\n• `claude45sonnet` – detailed code and document analysis\n• `claude45sonnetthinking` – logical problem-solving\n• `gpt5` – comprehensive technical analysis\n• `gpt5thinking` – deep reasoning and complex document insight\n• `sonar` – quick analysis and summaries",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_content": {
                            "type": "string",
                            "description": "Raw file content to analyze"
                        },
                        "file_type": {
                            "type": "string",
                            "default": "text",
                            "description": "File format (python, json, txt, etc.)"
                        },
                        "query": {
                            "type": "string",
                            "default": "Analyze this file content",
                            "description": "Specific question or task (e.g., \"summarize,\" \"find bugs,\" etc.)"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["pro"],
                            "default": "pro",
                            "description": "Analysis mode: always 'pro'"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "sonar"],
                            "description": "Specific model to use: claude45sonnet, claude45sonnetthinking, gpt5, gpt5thinking, sonar"
                        },
                        "profile": {
                            "type": "string",
                            "enum": [
                                "research", "code_analysis", "troubleshooting", "documentation",
                                "architecture", "security", "performance", "tutorial",
                                "comparison", "trending", "best_practices", "integration",
                                "debugging", "optimization"
                            ],
                            "description": "Enhances analysis - available profiles"
                        },
                        "raw_mode": {
                            "type": "boolean",
                            "default": False,
                            "description": "Return full JSON (true) or clean text answer (false, recommended)"
                        },
                        "search_focus": {
                            "type": "string",
                            "description": "Specific focus area for the analysis (e.g., 'security', 'performance', 'architecture', default: None)"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone for context-aware responses (e.g., 'UTC', 'America/New_York', default: None)"
                        }
                    },
                    "required": ["file_content", "model", "profile"]
                }
            }
        },
        "get_available_models": {
            "type": "function",
            "function": {
                "name": "get_available_models",
                "description": "🤖 Get list of supported Perplexity models for this MCP tool.\n\n**Available Models:**\n• claude45sonnet – balanced reasoning and explanation\n• claude45sonnetthinking – advanced logical reasoning\n• gpt5 – deep analytical research\n• gpt5thinking – complex reasoning and critical synthesis\n• sonar – fast, efficient factual lookups\n\n**Returns:**\n    Model list with descriptions and use cases",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        "get_search_profiles": {
            "type": "function",
            "function": {
                "name": "get_search_profiles",
                "description": "📋 Get comprehensive list of available search profiles with descriptions and use cases.\n\n**Perfect for:** Profile selection, understanding search enhancements, choosing right approach\n\n**Returns:**\nComplete profile catalog with descriptions, use cases, and examples for coding and tech work",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        "get_perplexity_health": {
            "type": "function",
            "function": {
                "name": "get_perplexity_health",
                "description": "🔍 Check Perplexity API connection health and system status.\n\n**Perfect for:** Connection diagnostics, performance monitoring, troubleshooting, API status verification\n\n**Health Checks Include:**\n• API connection status and latency\n• Model availability and response times\n• Authentication and authorization status\n• Rate limiting and quota information\n• System-wide performance metrics\n\n**Returns:**\nComprehensive health report with connection status, performance metrics, and diagnostic information",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    }


def validate_tool_input(tool_name: str, parameters: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate tool input parameters against schema.

    Args:
        tool_name: Name of the tool
        parameters: Input parameters to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        schemas = get_tool_schemas()

        if tool_name not in schemas:
            return False, f"Unknown tool: {tool_name}"

        schema = schemas[tool_name]["function"]["parameters"]
        required_fields = schema.get("required", [])
        properties = schema.get("properties", {})

        # Check required fields
        for field in required_fields:
            if field not in parameters:
                return False, f"Missing required field: {field}"

        # Check field types and enums
        for field_name, value in parameters.items():
            if field_name in properties:
                field_schema = properties[field_name]

                # Type validation
                field_type = field_schema.get("type")
                if field_type == "string" and not isinstance(value, str):
                    return False, f"Field {field_name} must be a string"
                elif field_type == "number" and not isinstance(value, (int, float)):
                    return False, f"Field {field_name} must be a number"
                elif field_type == "boolean" and not isinstance(value, bool):
                    return False, f"Field {field_name} must be a boolean"
                elif field_type == "array" and not isinstance(value, list):
                    return False, f"Field {field_name} must be an array"

                # Enum validation
                enum_values = field_schema.get("enum")
                if enum_values and value not in enum_values:
                    return False, f"Invalid value for {field_name}: {value}. Must be one of: {enum_values}"

        return True, ""

    except Exception as e:
        return False, f"Validation error: {str(e)}"