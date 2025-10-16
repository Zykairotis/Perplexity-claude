"""
JSON Schema definitions for MCP resources.

Provides schemas for resource validation and documentation.
"""

from typing import Dict, Any


def get_resource_schemas() -> Dict[str, Dict[str, Any]]:
    """
    Get JSON schemas for all MCP resources.

    Returns:
        Dictionary mapping resource URIs to their JSON schemas
    """
    return {
        "perplexity://models": {
            "type": "object",
            "description": "Available Perplexity models with descriptions and use cases",
            "properties": {
                "models": {
                    "type": "object",
                    "description": "Dictionary of model information",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Model description"
                            },
                            "use_case": {
                                "type": "string",
                                "description": "Recommended use case"
                            }
                        },
                        "required": ["description", "use_case"]
                    }
                },
                "mode": {
                    "type": "string",
                    "description": "Default search mode"
                },
                "required_profile": {
                    "type": "boolean",
                    "description": "Whether profile parameter is required"
                },
                "required_sources": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Required search sources"
                }
            },
            "required": ["models", "mode", "required_profile", "required_sources"]
        },

        "perplexity://health": {
            "type": "object",
            "description": "Perplexity API connection health and system status",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["healthy", "unhealthy"],
                    "description": "Overall health status"
                },
                "connection": {
                    "type": "string",
                    "enum": ["connected", "disconnected"],
                    "description": "Connection status"
                },
                "api_working": {
                    "type": "boolean",
                    "description": "Whether API is working correctly"
                },
                "test_result": {
                    "type": "object",
                    "description": "Results of health test",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Test query used"
                        },
                        "answer_length": {
                            "type": "integer",
                            "description": "Length of test answer"
                        },
                        "mode": {
                            "type": "string",
                            "description": "Mode used for test"
                        },
                        "timestamp": {
                            "type": "number",
                            "description": "Test timestamp"
                        }
                    }
                },
                "last_check": {
                    "type": "number",
                    "description": "Timestamp of last health check"
                },
                "error": {
                    "type": "string",
                    "description": "Error message if unhealthy"
                }
            },
            "required": ["status", "connection", "api_working"]
        },

        "perplexity://config": {
            "type": "object",
            "description": "Current server configuration and settings",
            "properties": {
                "server_name": {
                    "type": "string",
                    "description": "Server name"
                },
                "version": {
                    "type": "string",
                    "description": "Server version"
                },
                "log_level": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR"],
                    "description": "Current log level"
                },
                "default_mode": {
                    "type": "string",
                    "description": "Default search mode"
                },
                "default_sources": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Default search sources"
                },
                "required_model": {
                    "type": "boolean",
                    "description": "Whether model parameter is required"
                },
                "required_profile": {
                    "type": "boolean",
                    "description": "Whether profile parameter is required"
                },
                "max_results_default": {
                    "type": "integer",
                    "description": "Default maximum number of results"
                },
                "max_file_size": {
                    "type": "integer",
                    "description": "Maximum file size in bytes"
                }
            },
            "required": ["server_name", "version", "log_level"]
        },

        "perplexity://profiles": {
            "type": "object",
            "description": "Available search profiles with descriptions and use cases",
            "properties": {
                "profiles": {
                    "type": "object",
                    "description": "Dictionary of profile information",
                    "additionalProperties": {
                        "type": "string",
                        "description": "Profile description"
                    }
                },
                "usage": {
                    "type": "string",
                    "description": "Usage instructions for profiles"
                },
                "examples": {
                    "type": "object",
                    "description": "Usage examples for different profiles",
                    "additionalProperties": {
                        "type": "string",
                        "description": "Example usage"
                    }
                },
                "integration": {
                    "type": "string",
                    "description": "Integration information"
                }
            },
            "required": ["profiles", "usage", "examples", "integration"]
        }
    }