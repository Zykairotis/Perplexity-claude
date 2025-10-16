"""
Resource manager for handling MCP resources.

Manages registration and access to different resource providers.
"""

import logging
from typing import Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ResourceManager:
    """Manages MCP resources and their providers."""

    def __init__(self):
        self.providers = {}
        self.uri_schemes = {}

    def register_provider(self, uri_pattern: str, provider):
        """
        Register a resource provider for a URI pattern.

        Args:
            uri_pattern: URI pattern (e.g., "perplexity://models")
            provider: Provider instance
        """
        self.providers[uri_pattern] = provider

        # Extract scheme for pattern matching
        parsed = urlparse(uri_pattern)
        scheme = parsed.scheme
        if scheme not in self.uri_schemes:
            self.uri_schemes[scheme] = []
        self.uri_schemes[scheme].append(uri_pattern)

        logger.info(f"Registered resource provider for: {uri_pattern}")

    def get_provider(self, uri: str) -> Optional[Any]:
        """
        Get the appropriate provider for a URI.

        Args:
            uri: Resource URI

        Returns:
            Provider instance or None if not found
        """
        # Direct match first
        if uri in self.providers:
            return self.providers[uri]

        # Pattern matching
        parsed = urlparse(uri)
        scheme = parsed.scheme

        if scheme in self.uri_schemes:
            for pattern in self.uri_schemes[scheme]:
                # Simple pattern matching - can be enhanced
                if uri.startswith(pattern):
                    return self.providers[pattern]

        logger.warning(f"No provider found for URI: {uri}")
        return None

    async def read_resource(self, uri: str) -> str:
        """
        Read a resource by URI.

        Args:
            uri: Resource URI

        Returns:
            Resource content as string

        Raises:
            ValueError: If provider not found
            Exception: If reading fails
        """
        provider = self.get_provider(uri)
        if not provider:
            raise ValueError(f"No provider found for URI: {uri}")

        try:
            return await provider.read(uri)
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            raise

    def list_resources(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available resources.

        Returns:
            Dictionary of resource information
        """
        resources = {}
        for uri_pattern, provider in self.providers.items():
            try:
                resource_info = provider.get_info()
                resources[uri_pattern] = resource_info
            except Exception as e:
                logger.error(f"Error getting info for {uri_pattern}: {e}")
                resources[uri_pattern] = {
                    "error": str(e),
                    "uri": uri_pattern
                }

        return resources

    def supports_subscription(self, uri: str) -> bool:
        """
        Check if a resource supports subscriptions.

        Args:
            uri: Resource URI

        Returns:
            True if subscription is supported
        """
        provider = self.get_provider(uri)
        if not provider:
            return False

        return hasattr(provider, 'supports_subscription') and provider.supports_subscription()

    async def subscribe_to_resource(self, uri: str):
        """
        Subscribe to resource updates (if supported).

        Args:
            uri: Resource URI

        Returns:
            Async iterator for resource updates
        """
        provider = self.get_provider(uri)
        if not provider:
            raise ValueError(f"No provider found for URI: {uri}")

        if not self.supports_subscription(uri):
            raise ValueError(f"Resource {uri} does not support subscriptions")

        return provider.subscribe()


# Global resource manager instance
_resource_manager = None


def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance."""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager