"""
Search tool for Perplexity AI integration.

Provides search functionality using Perplexity AI's models with profile enhancement.
"""

import logging
from typing import List, Optional
from mcp.server.fastmcp import FastMCP

from .base import (
    validate_model, validate_mode, validate_sources,
    format_response, create_error_response
)
from utils.perplexity_client import get_perplexity_api
from utils.profile_validator import validate_profile

logger = logging.getLogger(__name__)


async def search_perplexity(
    query: str,
    mode: str = "pro",
    model: str = "claude45sonnet",
    sources: List[str] = ["web"],
    language: str = "english",
    max_results: int = 5,
    stream: bool = False,
    profile: str = "research",
    raw_mode: bool = False,
    prompt_source: Optional[str] = None,
    query_source: Optional[str] = None,
    should_ask_for_mcp_tool_confirmation: Optional[bool] = False,
    search_focus: Optional[str] = None,
    timezone: Optional[str] = None
) -> str:
    """
    🧩 Search using Perplexity AI (pro mode) for current, factual, or research-based answers.

    **Perfect for:** Technical queries, academic research, fact-checking, deep web insights

    **Available Models:**
    • `claude45sonnet` – balanced reasoning and explanation
    • `claude45sonnetthinking` – advanced logical reasoning
    • `gpt5` – deep analytical research
    • `gpt5thinking` – complex reasoning and critical synthesis
    • `sonar` – fast, efficient factual lookups

    **Required Args:**
        query: The search question or topic
        mode: Always "pro"
        model: One of the models listed above
        profile: Enhances result focus - available profiles:
            • research - detailed research with multiple sources
            • code_analysis - code review, logic analysis, improvements
            • troubleshooting - step-by-step issue resolution
            • documentation - comprehensive setup and usage docs
            • architecture - design patterns and scalability
            • security - vulnerability assessment and best practices
            • performance - bottlenecks and optimization strategies
            • tutorial - step-by-step learning with examples
            • comparison - detailed alternatives analysis
            • trending - latest developments and emerging tech
            • best_practices - industry standards and guidelines
            • integration - system compatibility and API patterns
            • debugging - systematic debugging techniques
            • optimization - specific performance improvements

    **Optional Args:**
        sources: Data origin (web, scholar, or social, default: web)
        language: Response language (default: English)
        max_results: Max number of results (default: 5)
        stream: Whether to stream the response (default: false)
        raw_mode: Return full JSON (true) or clean text answer (false, recommended)
        prompt_source: Source of the prompt for context tracking (default: None)
        query_source: Source of the query for analytics tracking (default: None)
        should_ask_for_mcp_tool_confirmation: Whether to ask for confirmation before executing MCP tools (default: False)
        search_focus: Specific focus area for the search (e.g., 'technical', 'academic', 'news', default: None)
        timezone: Timezone for context-aware responses (e.g., 'UTC', 'America/New_York', default: None)

    Returns:
        Clean text/markdown answer (default) or full JSON response with sources and metadata.
    """
    try:
        logger.info(f"Searching Perplexity: {query}")

        # Validate required parameters
        mode_validation = validate_mode(mode)
        if not mode_validation.is_valid:
            return create_error_response(mode_validation.error_message, raw_mode)

        model_validation = validate_model(model)
        if not model_validation.is_valid:
            return create_error_response(model_validation.error_message, raw_mode)

        # Validate profile (required)
        if not profile:
            from utils.profile_validator import list_available_profiles
            available_profiles = list(list_available_profiles().keys())
            return create_error_response(
                f"Profile is required. Available profiles: {available_profiles}",
                raw_mode
            )

        search_profile = validate_profile(profile)
        if search_profile is None:
            from utils.profile_validator import list_available_profiles
            available_profiles = list(list_available_profiles().keys())
            return create_error_response(
                f"Invalid profile '{profile}'. Available profiles: {available_profiles}",
                raw_mode
            )

        # Validate sources
        sources_validation = validate_sources(sources)
        if not sources_validation.is_valid:
            return create_error_response(sources_validation.error_message, raw_mode)

        # Get API client
        client_manager = get_perplexity_api()
        api = await client_manager.get_client()

        # Convert sources to enum format
        from perplexity_api import SearchSource
        source_mapping = {
            "web": SearchSource.WEB,
            "scholar": SearchSource.SCHOLAR,
            "social": SearchSource.SOCIAL
        }

        search_sources = []
        for source in sources_validation.normalized_data["sources"]:
            search_sources.append(source_mapping[source])

        # Convert mode to enum
        from perplexity_api import SearchMode
        mode_mapping = {
            "auto": SearchMode.AUTO,
            "pro": SearchMode.PRO,
            "reasoning": SearchMode.REASONING,
            "deep research": SearchMode.DEEP_RESEARCH
        }

        search_mode = mode_mapping.get(mode, SearchMode.AUTO)

        # Perform search with profile
        result = await api.search(
            query=query,
            mode=search_mode,
            sources=search_sources,
            language=language,
            model=model,
            profile=search_profile,
            prompt_source=prompt_source,
            query_source=query_source,
            should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
            search_focus=search_focus,
            timezone=timezone
        )

        # Format response
        if raw_mode:
            response_data = {
                "query": result.query,
                "answer": result.answer,
                "mode": result.mode,
                "model": result.model,
                "model_used": model,
                "language": result.language,
                "sources": result.sources[:max_results] if result.sources else [],
                "timestamp": result.timestamp,
                "related_queries": result.related_queries or [],
                "profile": search_profile.value if search_profile else None,
                "sources_count": len(result.sources) if result.sources else 0,
                "prompt_source": prompt_source,
                "query_source": query_source,
                "should_ask_for_mcp_tool_confirmation": should_ask_for_mcp_tool_confirmation,
                "search_focus": search_focus,
                "timezone": timezone
            }
            return format_response(response_data, raw_mode=True)
        else:
            return format_response(result.answer, raw_mode=False)

    except Exception as e:
        logger.error(f"Search error: {e}")
        return create_error_response(f"Error performing search: {str(e)}", raw_mode)