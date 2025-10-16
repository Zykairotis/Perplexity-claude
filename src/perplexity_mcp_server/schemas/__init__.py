"""
JSON Schema definitions for MCP server.

Provides schemas for validation and documentation.
"""

from .tool_schemas import get_tool_schemas, validate_tool_input
from .resource_schemas import get_resource_schemas

__all__ = [
    "get_tool_schemas",
    "validate_tool_input",
    "get_resource_schemas"
]