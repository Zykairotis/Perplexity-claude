"""
File analysis tool for Perplexity AI integration.

Provides file content analysis capabilities using Perplexity AI.
"""

import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP

from .base import (
    validate_model, validate_mode,
    format_response, create_error_response
)
from utils.perplexity_client import get_perplexity_api
from utils.profile_validator import validate_profile

logger = logging.getLogger(__name__)


async def analyze_file_with_perplexity(
    file_content: str,
    file_type: str = "text",
    query: str = "Analyze this file content",
    mode: str = "pro",
    model: str = "claude45sonnet",
    profile: str = "code_analysis",
    raw_mode: bool = False,
    prompt_source: Optional[str] = None,
    query_source: Optional[str] = None,
    should_ask_for_mcp_tool_confirmation: Optional[bool] = False,
    search_focus: Optional[str] = None,
    timezone: Optional[str] = None,
    space: Optional[str] = None
) -> str:
    """
    📄 Analyze and interpret file content using Perplexity AI (pro mode) for code, data, or document insights.

    **Perfect for:** Code review, document understanding, security checks, and data pattern extraction

    **Available Models:**
    • `claude45sonnet` – detailed code and document analysis
    • `claude45sonnetthinking` – logical problem-solving
    • `gpt5` – comprehensive technical analysis
    • `gpt5thinking` – deep reasoning and complex document insight
    • `sonar` – quick analysis and summaries

    **Required Args:**
        file_content: Raw file content to analyze
        file_type: File format (python, json, txt, etc.)
        query: Specific question or task (e.g., "summarize," "find bugs," etc.)
        mode: Always "pro"
        model: One of the models listed above
        profile: Enhances analysis - available profiles:
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
        prompt_source: Source of the prompt for context tracking (default: None)
        query_source: Source of the query for analytics tracking (default: None)
        should_ask_for_mcp_tool_confirmation: Whether to ask for confirmation before executing MCP tools (default: False)
        search_focus: Specific focus area for the analysis (e.g., 'security', 'performance', 'architecture', default: None)
        timezone: Timezone for context-aware responses (e.g., 'UTC', 'America/New_York', default: None)
        space: Space name or UUID to analyze within a specific Perplexity collection (default: None)

    Returns:
        Clean text analysis (default) or structured report with insights and metadata.
    """
    try:
        logger.info(f"Analyzing file with Perplexity: {query}")

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

        # Get API client
        client_manager = get_perplexity_api()
        api = await client_manager.get_client()

        # Convert modes to enums
        from perplexity_api import SearchMode, SearchSource
        mode_mapping = {
            "auto": SearchMode.AUTO,
            "pro": SearchMode.PRO,
            "reasoning": SearchMode.REASONING,
            "deep research": SearchMode.DEEP_RESEARCH
        }

        search_mode = mode_mapping.get(mode, SearchMode.AUTO)

        # Create analysis prompt
        analysis_prompt = f"""
        File Type: {file_type}
        Analysis Request: {query}

        File Content:
        {file_content}

        Please provide a comprehensive analysis of this file content based on the request.
        """

        # Perform analysis
        result = await api.search(
            query=analysis_prompt,
            mode=search_mode,
            sources=[SearchSource.WEB],
            language="english",
            model=model,
            profile=search_profile,
            prompt_source=prompt_source,
            query_source=query_source,
            should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
            search_focus=search_focus,
            timezone=timezone,
            space=space
        )

        # Format response
        if raw_mode:
            response_data = {
                "file_type": file_type,
                "analysis_request": query,
                "analysis": result.answer,
                "mode": result.mode,
                "model": result.model,
                "model_used": model,
                "timestamp": result.timestamp,
                "sources": result.sources or [],
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
        logger.error(f"File analysis error: {e}")
        return create_error_response(f"Error analyzing file: {str(e)}", raw_mode)