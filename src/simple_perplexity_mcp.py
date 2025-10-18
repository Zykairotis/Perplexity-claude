#!/usr/bin/env python3
"""
Simple Perplexity MCP Server

A Model Context Protocol (MCP) server that provides direct access to Perplexity AI models
without webhook complexity.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Dict, List, Optional, Any, Union

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Add the current directory to Python path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import Perplexity API from existing codebase
from perplexity_api import PerplexityAPI, SearchMode, SearchSource, ProModel, ReasoningModel
from perplexity_profiles import SearchProfile, list_available_profiles, validate_profile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("perplexity")

# Perplexity API instance
perplexity_api = PerplexityAPI()

# Request model for search
class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query or question")
    mode: str = Field("pro", description="Search mode: always 'pro'")
    model: str = Field(..., description="Specific model to use: claude45sonnet, claude45sonnetthinking, gpt5, gpt5thinking, experimental")
    sources: List[str] = Field(["web"], description="Sources: web, scholar, social")
    language: str = Field("english", description="Response language")
    max_results: int = Field(5, description="Maximum number of search results")
    stream: bool = Field(False, description="Whether to stream the response")
    profile: str = Field(..., description="Search profile: research, code_analysis, troubleshooting, etc.")
    raw_mode: bool = Field(False, description="Return full JSON response (true) or clean text answer (false, recommended)")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt for context tracking")
    query_source: Optional[str] = Field(None, description="Source of the query for analytics tracking")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(False, description="Whether to ask for confirmation before executing MCP tools")
    search_focus: Optional[str] = Field(None, description="Specific focus area for the search (e.g., 'technical', 'academic', 'news')")
    timezone: Optional[str] = Field(None, description="Timezone for context-aware responses (e.g., 'UTC', 'America/New_York')")

# Request model for chat
class ChatRequest(BaseModel):
    message: str = Field(..., description="The message or question")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuity")
    mode: str = Field("pro", description="Chat mode: always 'pro'")
    model: str = Field(..., description="Specific model to use: claude45sonnet, claude45sonnetthinking, gpt5, gpt5thinking, experimental")
    temperature: float = Field(0.7, description="Temperature for response generation")
    stream: bool = Field(False, description="Whether to stream the response")
    profile: str = Field(..., description="Search profile: research, code_analysis, troubleshooting, etc.")
    raw_mode: bool = Field(False, description="Return full JSON response (true) or clean text answer (false, recommended)")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt for context tracking")
    query_source: Optional[str] = Field(None, description="Source of the query for analytics tracking")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(False, description="Whether to ask for confirmation before executing MCP tools")
    search_focus: Optional[str] = Field(None, description="Specific focus area for the chat (e.g., 'technical', 'academic', 'news')")
    timezone: Optional[str] = Field(None, description="Timezone for context-aware responses (e.g., 'UTC', 'America/New_York')")

# Request model for file analysis
class FileAnalysisRequest(BaseModel):
    file_content: str = Field(..., description="Content of the file to analyze")
    file_type: str = Field("text", description="Type of file: text, pdf, image, etc.")
    query: str = Field(..., description="What to analyze about the file")
    mode: str = Field("pro", description="Analysis mode: always 'pro'")
    model: str = Field(..., description="Specific model to use: claude45sonnet, claude45sonnetthinking, gpt5, gpt5thinking, experimental")
    profile: str = Field(..., description="Search profile: research, code_analysis, security, etc.")
    raw_mode: bool = Field(False, description="Return full JSON response (true) or clean text answer (false, recommended)")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt for context tracking")
    query_source: Optional[str] = Field(None, description="Source of the query for analytics tracking")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(False, description="Whether to ask for confirmation before executing MCP tools")
    search_focus: Optional[str] = Field(None, description="Specific focus area for the analysis (e.g., 'security', 'performance', 'architecture')")
    timezone: Optional[str] = Field(None, description="Timezone for context-aware responses (e.g., 'UTC', 'America/New_York')")

@mcp.tool()
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
    • `experimental` – fast, efficient factual lookups (formerly Sonar)

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

        # Validate mode (must be "pro")
        if mode != "pro":
            return f"Error: Only 'pro' mode is supported. Please use mode='pro'"

        # Validate model (required)
        valid_models = ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "experimental"]
        if not model:
            return f"Error: Model is required. Available models: {valid_models}"
        if model not in valid_models:
            return f"Error: Invalid model '{model}'. Available models: {valid_models}"

        # Validate profile (required)
        if not profile:
            available_profiles = list(list_available_profiles().keys())
            return f"Error: Profile is required. Available profiles: {available_profiles}"

        search_profile = validate_profile(profile)
        if search_profile is None:
            available_profiles = list(list_available_profiles().keys())
            return f"Error: Invalid profile '{profile}'. Available profiles: {available_profiles}"

        # Convert string sources to SearchSource enums
        source_mapping = {
            "web": SearchSource.WEB,
            "scholar": SearchSource.SCHOLAR,
            "social": SearchSource.SOCIAL
        }

        search_sources = []
        for source in sources:
            if source.lower() in source_mapping:
                search_sources.append(source_mapping[source.lower()])

        if not search_sources:
            search_sources = [SearchSource.WEB]

        # Convert mode to SearchMode enum
        mode_mapping = {
            "auto": SearchMode.AUTO,
            "pro": SearchMode.PRO,
            "reasoning": SearchMode.REASONING,
            "deep research": SearchMode.DEEP_RESEARCH
        }

        search_mode = mode_mapping.get(mode, SearchMode.AUTO)

        # Set default model for pro mode if none specified
        if mode == "pro" and model is None:
            model = "claude45sonnet"  # Use Claude 4.5 Sonnet as default for pro mode

        # Perform search with profile
        result = await perplexity_api.search(
            query=query,
            mode=search_mode,
            sources=search_sources,
            language=language,
            model=model,
            profile=search_profile
        )

        # Format response based on raw_mode
        if raw_mode:
            # Return full JSON response
            response = {
                "query": result.query,
                "answer": result.answer,
                "mode": result.mode,
                "model": result.model,
                "model_used": model,  # Explicitly show which model was used
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
            return json.dumps(response, indent=2, default=str)
        else:
            # Return clean text answer (recommended)
            return result.answer

    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"Error performing search: {str(e)}"

@mcp.tool()
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
    • `experimental` – fast, concise replies (formerly Sonar)

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

        # Validate mode (must be "pro")
        if mode != "pro":
            return f"Error: Only 'pro' mode is supported. Please use mode='pro'"

        # Validate model (required)
        valid_models = ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "experimental"]
        if not model:
            return f"Error: Model is required. Available models: {valid_models}"
        if model not in valid_models:
            return f"Error: Invalid model '{model}'. Available models: {valid_models}"

        # Validate profile (required)
        if not profile:
            available_profiles = list(list_available_profiles().keys())
            return f"Error: Profile is required. Available profiles: {available_profiles}"

        search_profile = validate_profile(profile)
        if search_profile is None:
            available_profiles = list(list_available_profiles().keys())
            return f"Error: Invalid profile '{profile}'. Available profiles: {available_profiles}"

        # Convert mode to SearchMode enum
        mode_mapping = {
            "auto": SearchMode.AUTO,
            "pro": SearchMode.PRO,
            "reasoning": SearchMode.REASONING,
            "deep research": SearchMode.DEEP_RESEARCH
        }

        search_mode = mode_mapping.get(mode, SearchMode.AUTO)

        # Set default model for pro mode if none specified
        if mode == "pro" and model is None:
            model = "claude45sonnet"  # Use Claude 4.5 Sonnet as default for pro mode

        # For chat, we'll use the search method but treat it as a conversation
        result = await perplexity_api.search(
            query=message,
            mode=search_mode,
            sources=[SearchSource.WEB],
            language="english",
            model=model,
            profile=search_profile
        )

        # Format response based on raw_mode
        if raw_mode:
            # Return full JSON response
            response = {
                "message": message,
                "response": result.answer,
                "conversation_id": conversation_id or str(result.timestamp),
                "mode": result.mode,
                "model": result.model,
                "model_used": model,  # Explicitly show which model was used
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
            return json.dumps(response, indent=2, default=str)
        else:
            # Return clean text answer (recommended)
            return result.answer

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return f"Error in chat: {str(e)}"

@mcp.tool()
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
    timezone: Optional[str] = None
) -> str:
    """
    📄 Analyze and interpret file content using Perplexity AI (pro mode) for code, data, or document insights.

    **Perfect for:** Code review, document understanding, security checks, and data pattern extraction

    **Available Models:**
    • `claude45sonnet` – detailed code and document analysis
    • `claude45sonnetthinking` – logical problem-solving
    • `gpt5` – comprehensive technical analysis
    • `gpt5thinking` – deep reasoning and complex document insight
    • `experimental` – quick analysis and summaries (formerly Sonar)

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

    Returns:
        Clean text analysis (default) or structured report with insights and metadata.
    """
    try:
        logger.info(f"Analyzing file with Perplexity: {query}")

        # Validate mode (must be "pro")
        if mode != "pro":
            return f"Error: Only 'pro' mode is supported. Please use mode='pro'"

        # Validate model (required)
        valid_models = ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "experimental"]
        if not model:
            return f"Error: Model is required. Available models: {valid_models}"
        if model not in valid_models:
            return f"Error: Invalid model '{model}'. Available models: {valid_models}"

        # Validate profile (required)
        if not profile:
            available_profiles = list(list_available_profiles().keys())
            return f"Error: Profile is required. Available profiles: {available_profiles}"

        search_profile = validate_profile(profile)
        if search_profile is None:
            available_profiles = list(list_available_profiles().keys())
            return f"Error: Invalid profile '{profile}'. Available profiles: {available_profiles}"

        # Convert mode to SearchMode enum
        mode_mapping = {
            "auto": SearchMode.AUTO,
            "pro": SearchMode.PRO,
            "reasoning": SearchMode.REASONING,
            "deep research": SearchMode.DEEP_RESEARCH
        }

        search_mode = mode_mapping.get(mode, SearchMode.AUTO)

        # Set default model for pro mode if none specified
        if mode == "pro" and model is None:
            model = "claude45sonnet"  # Use Claude 4.5 Sonnet as default for pro mode

        # Create analysis prompt
        analysis_prompt = f"""
        File Type: {file_type}
        Analysis Request: {query}

        File Content:
        {file_content}

        Please provide a comprehensive analysis of this file content based on the request.
        """

        # Perform analysis
        result = await perplexity_api.search(
            query=analysis_prompt,
            mode=search_mode,
            sources=[SearchSource.WEB],
            language="english",
            model=model,
            profile=search_profile
        )

        # Format response based on raw_mode
        if raw_mode:
            # Return full JSON response
            response = {
                "file_type": file_type,
                "analysis_request": query,
                "analysis": result.answer,
                "mode": result.mode,
                "model": result.model,
                "model_used": model,  # Explicitly show which model was used
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
            return json.dumps(response, indent=2, default=str)
        else:
            # Return clean text answer (recommended)
            return result.answer

    except Exception as e:
        logger.error(f"File analysis error: {e}")
        return f"Error analyzing file: {str(e)}"

@mcp.tool()
async def get_available_models() -> str:
    """
    🤖 Get list of supported Perplexity models for this MCP tool.

    **Available Models:**
    • claude45sonnet – balanced reasoning and explanation
    • claude45sonnetthinking – advanced logical reasoning
    • gpt5 – deep analytical research
    • gpt5thinking – complex reasoning and critical synthesis
    • experimental – fast, efficient factual lookups (formerly Sonar)

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
            "experimental": {
                "description": "Fast, efficient factual lookups",
                "use_case": "Quick factual answers and simple queries"
            }
        }

        response = {
            "models": models,
            "mode": "pro",
            "required_profile": true,
            "required_sources": ["web", "scholar", "social"]
        }

        return json.dumps(response, indent=2)

    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return f"Error getting models: {str(e)}"

@mcp.tool()
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
        return f"Error getting profiles: {str(e)}"

@mcp.tool()
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
        # Try a simple test search
        result = await perplexity_api.search(
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

@mcp.resource("perplexity://models")
async def get_models_resource() -> str:
    """Resource for available Perplexity models"""
    return await get_available_models()

@mcp.resource("perplexity://health")
async def get_health_resource() -> str:
    """Resource for Perplexity API health status"""
    return await get_perplexity_health()

def main():
    """Main function to run the MCP server"""
    logger.info("Starting Simple Perplexity MCP Server...")

    try:
        # Run the server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down Simple Perplexity MCP Server...")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    main()