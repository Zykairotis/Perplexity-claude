"""
JSON Schema definitions for MCP tools.

Provides validation schemas for tool inputs and outputs.
"""

import json
from typing import Dict, Any


def get_tool_schemas() -> Dict[str, Dict[str, Any]]:
    """
    Get JSON schemas for all tools.

    Returns:
        Dictionary mapping tool names to their JSON schemas
    """
    return {
        "search_perplexity": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query or question"
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
                    "description": "Specific model to use"
                },
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["web", "scholar", "social"]
                    },
                    "default": ["web"],
                    "description": "Sources: web, scholar, social"
                },
                "language": {
                    "type": "string",
                    "default": "english",
                    "description": "Response language"
                },
                "max_results": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20,
                    "description": "Maximum number of search results"
                },
                "profile": {
                    "type": "string",
                    "enum": [
                        "research", "code_analysis", "troubleshooting", "documentation",
                        "architecture", "security", "performance", "tutorial",
                        "comparison", "trending", "best_practices", "integration",
                        "debugging", "optimization"
                    ],
                    "description": "Search profile for enhancing results"
                },
                "raw_mode": {
                    "type": "boolean",
                    "default": False,
                    "description": "Return full JSON response or clean text"
                },
                "search_focus": {
                    "type": "string",
                    "description": "Specific focus area for the search"
                },
                "timezone": {
                    "type": "string",
                    "description": "Timezone for context-aware responses"
                }
            },
            "required": ["query", "model", "profile"]
        },

        "chat_with_perplexity": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message or question"
                },
                "conversation_id": {
                    "type": "string",
                    "description": "Conversation ID for continuity"
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
                    "description": "Specific model to use"
                },
                "temperature": {
                    "type": "number",
                    "default": 0.7,
                    "minimum": 0.1,
                    "maximum": 1.0,
                    "description": "Temperature for response generation"
                },
                "profile": {
                    "type": "string",
                    "enum": [
                        "research", "code_analysis", "troubleshooting", "documentation",
                        "architecture", "security", "performance", "tutorial",
                        "comparison", "trending", "best_practices", "integration",
                        "debugging", "optimization"
                    ],
                    "description": "Search profile for enhancing conversation"
                },
                "raw_mode": {
                    "type": "boolean",
                    "default": False,
                    "description": "Return full JSON response or clean text"
                },
                "search_focus": {
                    "type": "string",
                    "description": "Specific focus area for the chat"
                },
                "timezone": {
                    "type": "string",
                    "description": "Timezone for context-aware responses"
                }
            },
            "required": ["message", "model", "profile"]
        },

        "analyze_file_with_perplexity": {
            "type": "object",
            "properties": {
                "file_content": {
                    "type": "string",
                    "description": "Content of the file to analyze"
                },
                "file_type": {
                    "type": "string",
                    "default": "text",
                    "description": "Type of file: text, pdf, image, etc."
                },
                "query": {
                    "type": "string",
                    "default": "Analyze this file content",
                    "description": "What to analyze about the file"
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
                    "description": "Specific model to use"
                },
                "profile": {
                    "type": "string",
                    "enum": [
                        "research", "code_analysis", "troubleshooting", "documentation",
                        "architecture", "security", "performance", "tutorial",
                        "comparison", "trending", "best_practices", "integration",
                        "debugging", "optimization"
                    ],
                    "description": "Search profile for enhancing analysis"
                },
                "raw_mode": {
                    "type": "boolean",
                    "default": False,
                    "description": "Return full JSON response or clean text"
                },
                "search_focus": {
                    "type": "string",
                    "description": "Specific focus area for the analysis"
                },
                "timezone": {
                    "type": "string",
                    "description": "Timezone for context-aware responses"
                }
            },
            "required": ["file_content", "model", "profile"]
        }
    }


def validate_request_data(tool_name: str, data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate request data against tool schema.

    Args:
        tool_name: Name of the tool
        data: Request data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        schemas = get_tool_schemas()

        if tool_name not in schemas:
            return False, f"Unknown tool: {tool_name}"

        schema = schemas[tool_name]

        # Basic required field validation
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in data or data[field] is None:
                return False, f"Missing required field: {field}"

        # Enum validation
        properties = schema.get("properties", {})
        for field_name, field_schema in properties.items():
            if field_name in data and data[field_name] is not None:
                enum_values = field_schema.get("enum")
                if enum_values and data[field_name] not in enum_values:
                    return False, f"Invalid value for {field_name}: {data[field_name]}. Must be one of: {enum_values}"

        return True, ""

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def get_resource_schemas() -> Dict[str, Dict[str, Any]]:
    """
    Get JSON schemas for all resources.

    Returns:
        Dictionary mapping resource names to their JSON schemas
    """
    return {
        "perplexity://models": {
            "type": "object",
            "description": "Available Perplexity models with descriptions",
            "properties": {
                "models": {
                    "type": "object",
                    "description": "Model descriptions"
                },
                "mode": {
                    "type": "string",
                    "description": "Default mode"
                },
                "required_profile": {
                    "type": "boolean",
                    "description": "Whether profile is required"
                }
            }
        },
        "perplexity://health": {
            "type": "object",
            "description": "Perplexity API health status",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Health status"
                },
                "connection": {
                    "type": "string",
                    "description": "Connection status"
                },
                "api_working": {
                    "type": "boolean",
                    "description": "Whether API is working"
                },
                "test_result": {
                    "type": "object",
                    "description": "Test result details"
                }
            }
        }
    }