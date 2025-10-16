"""
Chat tool for Perplexity AI integration.

Provides conversational access to Perplexity AI with context maintenance.
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


async def chat_with_perplexity(
    message: str,
    conversation_id: Optional[str] = None,
    mode: str = "pro",
    model: str = "claude45sonnet",
    temperature: float = 0.7,
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
    💬 Chat with Perplexity AI (pro mode) for interactive, context-aware explanations and reasoning.

    **Perfect for:** Conversational research, educational guidance, and technical Q&A

    **Available Models:**
    • `claude45sonnet` – detailed, balanced conversation
    • `claude45sonnetthinking` – logical and step-by-step discussions
    • `gpt5` – expert reasoning in conversation
    • `gpt5thinking` – advanced analytical discussions
    • `sonar` – fast, concise replies

    **Required Args:**
        message: User message or question
        mode: Always "pro"
        model: One of the models listed above
        profile: Enhances conversation context - available profiles:
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
        conversation_id: Maintain context between turns
        temperature: Controls creativity (0.1–1.0, default 0.7)
        stream: Whether to stream the response (default: false)
        raw_mode: Return full JSON (true) or clean text answer (false, recommended)
        prompt_source: Source of the prompt for context tracking (default: None)
        query_source: Source of the query for analytics tracking (default: None)
        should_ask_for_mcp_tool_confirmation: Whether to ask for confirmation before executing MCP tools (default: False)
        search_focus: Specific focus area for the chat (e.g., 'technical', 'academic', 'news', default: None)
        timezone: Timezone for context-aware responses (e.g., 'UTC', 'America/New_York', default: None)

    Returns:
        Clean text response (default) or full JSON with conversation context and metadata.
    """
    try:
        logger.info(f"Chatting with Perplexity: {message}")

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

        # For chat, we'll use the search method but treat it as a conversation
        result = await api.search(
            query=message,
            mode=search_mode,
            sources=[SearchSource.WEB],
            language="english",
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
                "message": message,
                "response": result.answer,
                "conversation_id": conversation_id or str(result.timestamp),
                "mode": result.mode,
                "model": result.model,
                "model_used": model,
                "timestamp": result.timestamp,
                "sources": result.sources or [],
                "profile": search_profile.value if search_profile else None,
                "sources_count": len(result.sources) if result.sources else 0,
                "temperature": temperature,
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
        logger.error(f"Chat error: {e}")
        return create_error_response(f"Error in chat: {str(e)}", raw_mode)