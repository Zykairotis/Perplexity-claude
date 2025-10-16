"""
Resource providers for different types of MCP resources.

Implements specific providers for models, health status, etc.
"""

import logging
import json
from typing import Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseResourceProvider(ABC):
    """Base class for resource providers."""

    @abstractmethod
    async def read(self, uri: str) -> str:
        """Read resource content."""
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Get resource information."""
        pass

    @property
    def supports_subscription(self) -> bool:
        """Whether this provider supports subscriptions."""
        return False


class ModelsResourceProvider(BaseResourceProvider):
    """Provider for available Perplexity models information."""

    def __init__(self):
        self.models_data = {
            "claude45sonnet": {
                "description": "Balanced reasoning and explanation",
                "use_case": "General purpose analysis and explanation"
            },
            "claude45sonnetthinking": {
                "description": "Advanced logical reasoning",
                "use_case": "Complex logical problems and step-by-step analysis"
            },
            "gpt5": {
                "description": "Deep analytical research",
                "use_case": "Comprehensive research and detailed analysis"
            },
            "gpt5thinking": {
                "description": "Complex reasoning and critical synthesis",
                "use_case": "Advanced analytical thinking and problem-solving"
            },
            "sonar": {
                "description": "Fast, efficient factual lookups",
                "use_case": "Quick factual answers and simple queries"
            }
        }

    async def read(self, uri: str) -> str:
        """Read models information."""
        response = {
            "models": self.models_data,
            "mode": "pro",
            "required_profile": True,
            "required_sources": ["web", "scholar", "social"]
        }

        return json.dumps(response, indent=2)

    def get_info(self) -> Dict[str, Any]:
        """Get models resource information."""
        return {
            "uri": "perplexity://models",
            "name": "Perplexity Models",
            "description": "Available Perplexity AI models with descriptions and use cases",
            "mime_type": "application/json"
        }


class HealthResourceProvider(BaseResourceProvider):
    """Provider for Perplexity API health status."""

    def __init__(self):
        self.last_check = None
        self.last_status = None

    async def read(self, uri: str) -> str:
        """Read current health status."""
        try:
            # Import here to avoid circular dependencies
            from utils.perplexity_client import get_perplexity_api
            from perplexity_api import SearchMode, SearchSource

            api = get_perplexity_api()
            client = await api.get_client()

            # Try a simple test search
            result = await client.search(
                query="test",
                mode=SearchMode.AUTO,
                sources=[SearchSource.WEB],
                language="english"
            )

            response = {
                "status": "healthy",
                "connection": "connected",
                "api_working": True,
                "test_result": {
                    "query": result.query,
                    "answer_length": len(result.answer) if result.answer else 0,
                    "mode": result.mode,
                    "timestamp": result.timestamp
                },
                "last_check": self.last_check
            }

            self.last_status = response

        except Exception as e:
            response = {
                "status": "unhealthy",
                "connection": "disconnected",
                "api_working": False,
                "error": str(e),
                "last_check": self.last_check
            }

            self.last_status = response

        import time
        self.last_check = time.time()

        return json.dumps(response, indent=2, default=str)

    def get_info(self) -> Dict[str, Any]:
        """Get health resource information."""
        return {
            "uri": "perplexity://health",
            "name": "Perplexity API Health",
            "description": "Perplexity API connection health and system status",
            "mime_type": "application/json"
        }


class ConfigurationResourceProvider(BaseResourceProvider):
    """Provider for server configuration information."""

    def __init__(self, config=None):
        self.config = config or {}

    async def read(self, uri: str) -> str:
        """Read configuration information."""
        config_info = {
            "server_name": self.config.get("name", "perplexity"),
            "version": self.config.get("version", "1.0.0"),
            "log_level": self.config.get("log_level", "INFO"),
            "default_mode": self.config.get("default_mode", "pro"),
            "default_sources": self.config.get("default_sources", ["web"]),
            "required_model": self.config.get("required_model", True),
            "required_profile": self.config.get("required_profile", True),
            "max_results_default": self.config.get("max_results_default", 5),
            "max_file_size": self.config.get("max_file_size", 10485760)
        }

        return json.dumps(config_info, indent=2)

    def get_info(self) -> Dict[str, Any]:
        """Get configuration resource information."""
        return {
            "uri": "perplexity://config",
            "name": "Server Configuration",
            "description": "Current server configuration and settings",
            "mime_type": "application/json"
        }


class ProfilesResourceProvider(BaseResourceProvider):
    """Provider for search profiles information."""

    async def read(self, uri: str) -> str:
        """Read profiles information."""
        from utils.profile_validator import list_available_profiles

        profiles = list_available_profiles()

        response = {
            "profiles": profiles,
            "usage": "Add the profile parameter to any search function to enhance query effectiveness",
            "examples": {
                "research": "search_perplexity(query='blockchain technology', profile='research')",
                "code_analysis": "search_perplexity(query='React hooks optimization', profile='code_analysis')",
                "troubleshooting": "search_perplexity(query='Docker connection issues', profile='troubleshooting')"
            },
            "integration": "Profiles work with search_perplexity, chat_with_perplexity, and analyze_file_with_perplexity"
        }

        return json.dumps(response, indent=2)

    def get_info(self) -> Dict[str, Any]:
        """Get profiles resource information."""
        return {
            "uri": "perplexity://profiles",
            "name": "Search Profiles",
            "description": "Available search profiles with descriptions and use cases",
            "mime_type": "application/json"
        }