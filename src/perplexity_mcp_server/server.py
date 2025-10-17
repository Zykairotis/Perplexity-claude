#!/usr/bin/env python3
"""
Perplexity MCP Server - Main Entry Point

A modular Model Context Protocol server that provides access to Perplexity AI
search capabilities with proper separation of concerns and maintainable architecture.
"""

import json
import logging
import sys
import os
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Import server components
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)  # Add MCP server directory
sys.path.insert(0, os.path.dirname(current_dir))  # Add src directory

from perplexity_mcp_server.config.settings import load_config, ServerConfig
from perplexity_mcp_server.tools import (
    search_perplexity,
    chat_with_perplexity,
    analyze_file_with_perplexity,
    get_available_models,
    get_search_profiles,
    get_perplexity_health,
    create_perplexity_space,
    list_perplexity_spaces
)
from perplexity_mcp_server.resources import get_resource_manager, get_search_context, get_session_history
from perplexity_mcp_server.resources.providers import (
    ModelsResourceProvider,
    HealthResourceProvider,
    ConfigurationResourceProvider,
    ProfilesResourceProvider,
    SpacesResourceProvider
)
from perplexity_mcp_server.utils.perplexity_client import get_perplexity_api
from perplexity_mcp_server.prompts import (
    search_workshop,
    consultation_session,
    file_analysis_deep_dive,
    research_assistant,
    list_server_assets
)


class PerplexityMCPServer:
    """Main Perplexity MCP Server class."""

    def __init__(self, config: Optional[ServerConfig] = None):
        """
        Initialize the MCP server.

        Args:
            config: Optional server configuration
        """
        self.config = config or load_config()
        self.mcp = FastMCP(self.config.name)
        self.resource_manager = get_resource_manager()
        self.logger = self._setup_logging()

        self._setup_tools()
        self._setup_resources()
        self._setup_prompts()

    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def _setup_tools(self):
        """Register all MCP tools."""
        self.logger.info("Registering MCP tools...")

        # Register search tool
        self.mcp.tool()(
            search_perplexity
        )

        # Register chat tool
        self.mcp.tool()(
            chat_with_perplexity
        )

        # Register file analysis tool
        self.mcp.tool()(
            analyze_file_with_perplexity
        )

        # Register utility tools
        self.mcp.tool()(
            get_available_models
        )

        self.mcp.tool()(
            get_search_profiles
        )

        self.mcp.tool()(
            get_perplexity_health
        )

        # Register space management tools
        self.mcp.tool()(
            create_perplexity_space
        )

        self.mcp.tool()(
            list_perplexity_spaces
        )

        self.logger.info(f"Registered 8 tools")

    def _setup_resources(self):
        """Register all MCP resources."""
        self.logger.info("Registering MCP resources...")

        # Register resource providers
        models_provider = ModelsResourceProvider()
        health_provider = HealthResourceProvider()
        config_provider = ConfigurationResourceProvider(self.config.model_dump())
        profiles_provider = ProfilesResourceProvider()

        self.resource_manager.register_provider("perplexity://models", models_provider)
        self.resource_manager.register_provider("perplexity://health", health_provider)
        self.resource_manager.register_provider("perplexity://config", config_provider)
        self.resource_manager.register_provider("perplexity://profiles", profiles_provider)

        # Register resources with MCP
        self.mcp.resource("perplexity://models")(self._get_models_resource)
        self.mcp.resource("perplexity://health")(self._get_health_resource)
        self.mcp.resource("perplexity://config")(self._get_config_resource)
        self.mcp.resource("perplexity://profiles")(self._get_profiles_resource)
        self.mcp.resource("perplexity://spaces")(self._get_spaces_resource)

        # Register new dynamic resources
        self.mcp.resource("perplexity://search/context")(self._get_search_context_resource)
        self.mcp.resource("perplexity://search/analytics")(self._get_search_analytics_resource)
        self.mcp.resource("perplexity://search/trending")(self._get_trending_queries_resource)
        self.mcp.resource("perplexity://session/history")(self._get_session_history_resource)
        self.mcp.resource("perplexity://session/analytics")(self._get_session_analytics_resource)

        self.logger.info(f"Registered 10 resources")

    def _setup_prompts(self):
        """Register all MCP prompts."""
        self.logger.info("Registering MCP prompts...")

        # Register search workshop prompt
        self.mcp.prompt()(
            search_workshop
        )

        # Register consultation session prompt
        self.mcp.prompt()(
            consultation_session
        )

        # Register file analysis deep dive prompt
        self.mcp.prompt()(
            file_analysis_deep_dive
        )

        # Register research assistant prompt
        self.mcp.prompt()(
            research_assistant
        )

        # Register list server assets prompt
        self.mcp.prompt()(
            list_server_assets
        )

        self.logger.info(f"Registered 5 prompts")

    async def _get_models_resource(self):
        """Resource handler for models."""
        try:
            return await self.resource_manager.read_resource("perplexity://models")
        except Exception as e:
            self.logger.error(f"Error reading models resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_health_resource(self):
        """Resource handler for health."""
        try:
            return await self.resource_manager.read_resource("perplexity://health")
        except Exception as e:
            self.logger.error(f"Error reading health resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_config_resource(self):
        """Resource handler for config."""
        try:
            return await self.resource_manager.read_resource("perplexity://config")
        except Exception as e:
            self.logger.error(f"Error reading config resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_profiles_resource(self):
        """Resource handler for profiles."""
        try:
            return await self.resource_manager.read_resource("perplexity://profiles")
        except Exception as e:
            self.logger.error(f"Error reading profiles resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_spaces_resource(self):
        """Resource handler for spaces."""
        try:
            return await self.resource_manager.read_resource("perplexity://spaces")
        except Exception as e:
            self.logger.error(f"Error reading spaces resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_search_context_resource(self):
        """Resource handler for search context."""
        try:
            return json.dumps(await get_search_context())
        except Exception as e:
            self.logger.error(f"Error reading search context resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_search_analytics_resource(self):
        """Resource handler for search analytics."""
        try:
            from .resources.search_context_resource import get_search_analytics
            return json.dumps(await get_search_analytics())
        except Exception as e:
            self.logger.error(f"Error reading search analytics resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_trending_queries_resource(self):
        """Resource handler for trending queries."""
        try:
            from .resources.search_context_resource import get_trending_queries
            return json.dumps(await get_trending_queries())
        except Exception as e:
            self.logger.error(f"Error reading trending queries resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_session_history_resource(self):
        """Resource handler for session history."""
        try:
            return json.dumps(await get_session_history())
        except Exception as e:
            self.logger.error(f"Error reading session history resource: {e}")
            return json.dumps({"error": str(e)})

    async def _get_session_analytics_resource(self):
        """Resource handler for session analytics."""
        try:
            from .resources.session_history_resource import get_session_analytics
            return json.dumps(await get_session_analytics())
        except Exception as e:
            self.logger.error(f"Error reading session analytics resource: {e}")
            return json.dumps({"error": str(e)})

    def start(self):
        """Start the MCP server."""
        self.logger.info(f"Starting {self.config.name} v{self.config.version}")
        self.logger.info(f"Log level: {self.config.log_level}")
        self.logger.info(f"Perplexity timeout: {self.config.perplexity_timeout}s")

        try:
            # Start the MCP server - FastMCP handles asyncio internally
            self.mcp.run()
        except KeyboardInterrupt:
            self.logger.info("Server interrupted by user")
        except Exception as e:
            self.logger.error(f"Server error: {e}")
            raise

    async def _cleanup(self):
        """Cleanup resources."""
        try:
            api = get_perplexity_api()
            await api.close()
            self.logger.info("Perplexity API client closed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

    def get_server_info(self) -> dict:
        """Get server information."""
        return {
            "name": self.config.name,
            "version": self.config.version,
            "tools": [
                "search_perplexity",
                "chat_with_perplexity",
                "analyze_file_with_perplexity",
                "get_available_models",
                "get_search_profiles",
                "get_perplexity_health",
                "create_perplexity_space",
                "list_perplexity_spaces"
            ],
            "resources": [
                "perplexity://models",
                "perplexity://health",
                "perplexity://config",
                "perplexity://profiles",
                "perplexity://spaces",
                "perplexity://search/context",
                "perplexity://search/analytics",
                "perplexity://search/trending",
                "perplexity://session/history",
                "perplexity://session/analytics"
            ],
            "prompts": [
                "search_workshop",
                "consultation_session",
                "file_analysis_deep_dive",
                "research_assistant",
                "list_server_assets"
            ]
        }


def main():
    """Main entry point."""
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Perplexity MCP Server")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Override log level"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="1.0.0"
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Override log level if provided
    if args.log_level:
        config.log_level = args.log_level

    # Create and start server
    server = PerplexityMCPServer(config)

    try:
        server.start()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()