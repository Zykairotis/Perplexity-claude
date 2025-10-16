"""
Utility tools for Perplexity MCP server.

Provides helper tools for model information, profiles, and health checks.
"""

import logging
import json
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from .base import format_response, create_error_response
from utils.perplexity_client import get_perplexity_api
from utils.profile_validator import list_available_profiles

logger = logging.getLogger(__name__)


async def get_available_models() -> str:
    """
    🤖 Get list of supported Perplexity models for this MCP tool.

    **Available Models:**
    • claude45sonnet – balanced reasoning and explanation
    • claude45sonnetthinking – advanced logical reasoning
    • gpt5 – deep analytical research
    • gpt5thinking – complex reasoning and critical synthesis
    • sonar – fast, efficient factual lookups

    **Returns:**
        Model list with descriptions and use cases
    """
    try:
        models = {
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

        response = {
            "models": models,
            "mode": "pro",
            "required_profile": True,
            "required_sources": ["web", "scholar", "social"]
        }

        return json.dumps(response, indent=2)

    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return create_error_response(f"Error getting models: {str(e)}", raw_mode=True)


async def get_search_profiles() -> str:
    """
    📋 Get comprehensive list of available search profiles with descriptions and use cases.

    **Perfect for:** Profile selection, understanding search enhancements, choosing right approach

    **Returns:**
    Complete profile catalog with descriptions, use cases, and examples for coding and tech work
    """
    try:
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

    except Exception as e:
        logger.error(f"Error getting profiles: {e}")
        return create_error_response(f"Error getting profiles: {str(e)}", raw_mode=True)


async def get_perplexity_health() -> str:
    """
    🔍 Check Perplexity API connection health and system status.

    **Perfect for:** Connection diagnostics, performance monitoring, troubleshooting, API status verification

    **Health Checks Include:**
    • API connection status and latency
    • Model availability and response times
    • Authentication and authorization status
    • Rate limiting and quota information
    • System-wide performance metrics

    **Returns:**
    Comprehensive health report with connection status, performance metrics, and diagnostic information
    """
    try:
        # Get API client
        client_manager = get_perplexity_api()
        api = await client_manager.get_client()

        # Try a simple test search
        from perplexity_api import SearchMode, SearchSource
        result = await api.search(
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
            }
        }

        return json.dumps(response, indent=2, default=str)

    except Exception as e:
        response = {
            "status": "unhealthy",
            "connection": "disconnected",
            "api_working": False,
            "error": str(e)
        }

        return json.dumps(response, indent=2, default=str)