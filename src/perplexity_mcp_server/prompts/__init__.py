"""
Prompt management for Perplexity MCP server.

Provides comprehensive prompt templates and management for different use cases,
including specialized prompts for search workshops, consultations, and analysis.
"""

from .manager import PromptManager, get_prompt_manager
from .templates import (
    get_search_template,
    get_analysis_template,
    get_chat_template,
    get_troubleshooting_template
)
from .search_workshop_prompt import search_workshop
from .consultation_session_prompt import consultation_session
from .file_analysis_deep_dive_prompt import file_analysis_deep_dive
from .research_assistant_prompt import research_assistant
from .list_server_assets_prompt import list_server_assets

__all__ = [
    "PromptManager",
    "get_prompt_manager",
    "get_search_template",
    "get_analysis_template",
    "get_chat_template",
    "get_troubleshooting_template",
    "search_workshop",
    "consultation_session",
    "file_analysis_deep_dive",
    "research_assistant",
    "list_server_assets"
]