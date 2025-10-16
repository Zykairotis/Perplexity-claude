"""
Data models for Perplexity MCP server.

Defines Pydantic models for request and response validation.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


# Request Models
class SearchRequest(BaseModel):
    """Model for search requests."""
    query: str = Field(..., description="The search query or question")
    mode: str = Field("pro", description="Search mode: always 'pro'")
    model: str = Field(..., description="Specific model to use")
    sources: List[str] = Field(["web"], description="Sources: web, scholar, social")
    language: str = Field("english", description="Response language")
    max_results: int = Field(5, description="Maximum number of search results")
    stream: bool = Field(False, description="Whether to stream the response")
    profile: str = Field(..., description="Search profile")
    raw_mode: bool = Field(False, description="Return full JSON response or clean text")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt for context tracking")
    query_source: Optional[str] = Field(None, description="Source of the query for analytics tracking")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(False, description="Whether to ask for confirmation before executing MCP tools")
    search_focus: Optional[str] = Field(None, description="Specific focus area for the search")
    timezone: Optional[str] = Field(None, description="Timezone for context-aware responses")


class ChatRequest(BaseModel):
    """Model for chat requests."""
    message: str = Field(..., description="The message or question")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuity")
    mode: str = Field("pro", description="Chat mode: always 'pro'")
    model: str = Field(..., description="Specific model to use")
    temperature: float = Field(0.7, description="Temperature for response generation")
    stream: bool = Field(False, description="Whether to stream the response")
    profile: str = Field(..., description="Search profile")
    raw_mode: bool = Field(False, description="Return full JSON response or clean text")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt for context tracking")
    query_source: Optional[str] = Field(None, description="Source of the query for analytics tracking")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(False, description="Whether to ask for confirmation before executing MCP tools")
    search_focus: Optional[str] = Field(None, description="Specific focus area for the chat")
    timezone: Optional[str] = Field(None, description="Timezone for context-aware responses")


class FileAnalysisRequest(BaseModel):
    """Model for file analysis requests."""
    file_content: str = Field(..., description="Content of the file to analyze")
    file_type: str = Field("text", description="Type of file: text, pdf, image, etc.")
    query: str = Field(..., description="What to analyze about the file")
    mode: str = Field("pro", description="Analysis mode: always 'pro'")
    model: str = Field(..., description="Specific model to use")
    profile: str = Field(..., description="Search profile")
    raw_mode: bool = Field(False, description="Return full JSON response or clean text")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt for context tracking")
    query_source: Optional[str] = Field(None, description="Source of the query for analytics tracking")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(False, description="Whether to ask for confirmation before executing MCP tools")
    search_focus: Optional[str] = Field(None, description="Specific focus area for the analysis")
    timezone: Optional[str] = Field(None, description="Timezone for context-aware responses")


# Response Models
class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = Field(True, description="Whether the operation was successful")
    timestamp: float = Field(..., description="Response timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SearchResponse(BaseResponse):
    """Model for search responses."""
    query: str = Field(..., description="Original search query")
    answer: str = Field(..., description="Search answer/result")
    mode: str = Field(..., description="Search mode used")
    model: str = Field(..., description="Model used for search")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Search sources")
    related_queries: List[str] = Field(default_factory=list, description="Related queries")
    profile: Optional[str] = Field(None, description="Profile used")
    sources_count: int = Field(0, description="Number of sources")


class ChatResponse(BaseResponse):
    """Model for chat responses."""
    message: str = Field(..., description="Original user message")
    response: str = Field(..., description="Chat response")
    conversation_id: str = Field(..., description="Conversation ID")
    mode: str = Field(..., description="Chat mode used")
    model: str = Field(..., description="Model used for chat")
    temperature: float = Field(0.7, description="Temperature used")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Sources referenced")
    profile: Optional[str] = Field(None, description="Profile used")


class FileAnalysisResponse(BaseResponse):
    """Model for file analysis responses."""
    file_type: str = Field(..., description="Type of file analyzed")
    analysis_request: str = Field(..., description="Original analysis request")
    analysis: str = Field(..., description="Analysis result")
    mode: str = Field(..., description="Analysis mode used")
    model: str = Field(..., description="Model used for analysis")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Sources referenced")
    profile: Optional[str] = Field(None, description="Profile used")


# Utility Models
class ErrorResponse(BaseResponse):
    """Model for error responses."""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., description="Health status")
    connection: str = Field(..., description="Connection status")
    api_working: bool = Field(..., description="Whether API is working")
    test_result: Optional[Dict[str, Any]] = Field(None, description="Test result details")
    error: Optional[str] = Field(None, description="Error message if unhealthy")


class ModelsResponse(BaseModel):
    """Model for available models response."""
    models: Dict[str, Dict[str, str]] = Field(..., description="Available models with descriptions")
    mode: str = Field(..., description="Default mode")
    required_profile: bool = Field(..., description="Whether profile is required")
    required_sources: List[str] = Field(..., description="Required sources")


class ProfilesResponse(BaseModel):
    """Model for available profiles response."""
    profiles: Dict[str, str] = Field(..., description="Available profiles with descriptions")
    usage: str = Field(..., description="Usage instructions")
    examples: Dict[str, str] = Field(..., description="Usage examples")
    integration: str = Field(..., description="Integration information")