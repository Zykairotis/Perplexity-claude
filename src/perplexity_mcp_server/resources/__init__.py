"""
Resource management for Perplexity MCP server.

Handles MCP resources for models, health status, search context, and session history.
"""

from .manager import ResourceManager, get_resource_manager
from .providers import (
    ModelsResourceProvider,
    HealthResourceProvider,
    SpacesResourceProvider
)
from .search_context_resource import (
    get_search_context,
    get_search_analytics,
    get_trending_queries
)
from .session_history_resource import (
    get_session_history,
    get_session_details,
    get_history_summary,
    get_session_analytics
)
from .spaces_resource import (
    get_configured_spaces,
    get_space_info,
    get_spaces_summary
)

__all__ = [
    "ResourceManager",
    "get_resource_manager",
    "ModelsResourceProvider",
    "HealthResourceProvider",
    "SpacesResourceProvider",
    "get_search_context",
    "get_search_analytics",
    "get_trending_queries",
    "get_session_history",
    "get_session_details",
    "get_history_summary",
    "get_session_analytics",
    "get_configured_spaces",
    "get_space_info",
    "get_spaces_summary"
]