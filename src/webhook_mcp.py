#!/usr/bin/env python3
"""
MCP Webhook-Perplexity Integration Server

A Model Context Protocol (MCP) server that enables AI agents to call external webhooks
and analyze the responses using Perplexity AI.
"""

import asyncio
import json
import logging
import os
import sys
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, field_validator

# Add the current directory to Python path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import Perplexity API from existing codebase
from perplexity_api import PerplexityAPI, SearchMode, SearchSource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
webhook_port = int(os.getenv("WEBHOOK_MCP_PORT", "8000"))
mcp = FastMCP("webhook-perplexity")

# Configuration
class WebhookConfig:
    """Configuration for webhook operations"""
    def __init__(self):
        self.default_timeout = int(os.getenv("WEBHOOK_DEFAULT_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("WEBHOOK_MAX_RETRIES", "3"))
        self.retry_delay = float(os.getenv("WEBHOOK_RETRY_DELAY", "1.0"))
        self.user_agent = os.getenv("WEBHOOK_USER_AGENT", "Webhook-MCP-Server/1.0")

        # Perplexity API configuration
        self.perplexity_api_url = os.getenv("PERPLEXITY_API_URL", "http://localhost:9522/api/search/files/stream")
        self.perplexity_timeout = int(os.getenv("PERPLEXITY_TIMEOUT", "120"))
        self.default_perplexity_mode = os.getenv("DEFAULT_PERPLEXITY_MODE", "auto")
        self.default_perplexity_sources = os.getenv("DEFAULT_PERPLEXITY_SOURCES", "web").split(",")

# Global configuration instance
config = WebhookConfig()

# Global Perplexity API instance
perplexity_api = None

async def get_perplexity_api():
    """Get or create Perplexity API instance"""
    global perplexity_api
    if perplexity_api is None:
        perplexity_api = PerplexityAPI()
    return perplexity_api

# Request/Response Models
class WebhookRequest(BaseModel):
    """Webhook request model"""
    url: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Union[Dict[str, Any], str]] = None
    auth_type: Optional[str] = None
    auth_credentials: Optional[Dict[str, str]] = None
    timeout: int = 30

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        """Validate URL format and security"""
        parsed = urlparse(v)
        if parsed.scheme not in ['http', 'https']:
            raise ValueError("URL must use HTTP or HTTPS protocol")

        # Basic SSRF protection
        if parsed.hostname in ['localhost', '127.0.0.1'] or parsed.hostname.startswith('192.168.'):
            raise ValueError("Internal network access not allowed")

        return v

    @field_validator('method')
    @classmethod
    def validate_method(cls, v):
        """Validate HTTP method"""
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD']
        if v.upper() not in allowed_methods:
            raise ValueError(f"Method must be one of: {allowed_methods}")
        return v.upper()

class WebhookResponse(BaseModel):
    """Webhook response model"""
    status_code: int
    headers: Dict[str, str]
    body: Any
    response_time: float
    error: Optional[str] = None

class AnalysisRequest(BaseModel):
    """Analysis request model"""
    response_data: Union[Dict[str, Any], str]
    analysis_query: Optional[str] = None
    perplexity_mode: str = "auto"
    perplexity_model: Optional[str] = None
    sources: List[str] = ["web"]

    @field_validator('sources')
    @classmethod
    def validate_sources(cls, v):
        """Validate and normalize source names"""
        valid_sources = {"web": "web", "scholar": "scholar", "social": "social"}
        normalized = []
        for source in v:
            source_lower = source.lower()
            if source_lower in valid_sources:
                normalized.append(valid_sources[source_lower])
            else:
                normalized.append("web")  # Default to web if invalid
        return normalized

class AuthHandler:
    """Handle different authentication methods"""

    @staticmethod
    def add_auth_headers(headers: Dict[str, str], auth_type: str, auth_credentials: Dict[str, str]) -> Dict[str, str]:
        """Add authentication headers based on auth type"""
        new_headers = headers.copy()

        if auth_type == "bearer":
            token = auth_credentials.get("token")
            if token:
                new_headers["Authorization"] = f"Bearer {token}"

        elif auth_type == "basic":
            username = auth_credentials.get("username")
            password = auth_credentials.get("password")
            if username and password:
                import base64
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                new_headers["Authorization"] = f"Basic {credentials}"

        elif auth_type == "api_key":
            key = auth_credentials.get("key")
            header_name = auth_credentials.get("header_name", "X-API-Key")
            if key:
                new_headers[header_name] = key

        return new_headers

class WebhookClient:
    """HTTP client for webhook calls with retry logic"""

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=config.default_timeout,
            headers={"User-Agent": config.user_agent}
        )

    async def call_webhook(self, request: WebhookRequest) -> WebhookResponse:
        """Call webhook with retry logic"""
        headers = request.headers or {}

        # Add authentication
        if request.auth_type and request.auth_credentials:
            headers = AuthHandler.add_auth_headers(
                headers, request.auth_type, request.auth_credentials
            )

        # Prepare request body
        body = None
        if request.body:
            if isinstance(request.body, dict):
                body = json.dumps(request.body)
                headers["Content-Type"] = "application/json"
            else:
                body = request.body

        start_time = time.time()
        last_error = None

        for attempt in range(config.max_retries + 1):
            try:
                response = await self.client.request(
                    method=request.method,
                    url=request.url,
                    headers=headers,
                    content=body,
                    timeout=request.timeout
                )

                response_time = time.time() - start_time

                # Parse response body
                try:
                    if response.headers.get("content-type", "").startswith("application/json"):
                        response_body = response.json()
                    else:
                        response_body = response.text
                except Exception:
                    response_body = response.text

                return WebhookResponse(
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    body=response_body,
                    response_time=response_time
                )

            except Exception as e:
                last_error = str(e)

                # Don't retry on final attempt
                if attempt == config.max_retries:
                    break

                logger.warning(f"Request failed attempt {attempt + 1}/{config.max_retries + 1}: {last_error}")
                await asyncio.sleep(config.retry_delay * (2 ** attempt))

        # Return error response if all attempts failed
        return WebhookResponse(
            status_code=0,
            headers={},
            body="",
            response_time=time.time() - start_time,
            error=f"Request failed after {config.max_retries + 1} attempts: {last_error}"
        )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

class ResponseAnalyzer:
    """Analyze webhook responses using Perplexity AI"""

    def __init__(self):
        self.api = None

    async def get_api(self):
        """Get Perplexity API instance"""
        if not self.api:
            self.api = await get_perplexity_api()
        return self.api

    async def analyze_response(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Analyze webhook response using Perplexity AI"""
        try:
            api = await self.get_api()

            # Prepare the analysis query
            if request.analysis_query:
                query = request.analysis_query
            else:
                # Generate a default analysis query based on the response data
                data_str = json.dumps(request.response_data, indent=2) if isinstance(request.response_data, dict) else str(request.response_data)
                query = f"Analyze the following webhook response data and provide insights:\n\n{data_str}"

            # Prepare search parameters
            # Map perplexity modes to valid SearchMode values
            mode_mapping = {
                "auto": SearchMode.AUTO,
                "pro": SearchMode.PRO,
                "reasoning": SearchMode.REASONING,
                "deep_research": SearchMode.DEEP_RESEARCH,
                "concise": SearchMode.AUTO,  # Map concise to auto
                "detailed": SearchMode.PRO   # Map detailed to pro
            }

            search_mode = mode_mapping.get(request.perplexity_mode.lower(), SearchMode.AUTO)

            search_params = {
                "query": query,
                "mode": search_mode,
                "sources": [SearchSource(s) for s in request.sources],
                "timeout": config.perplexity_timeout
            }

            if request.perplexity_model:
                search_params["model"] = request.perplexity_model

            # Perform the search
            result = await api.search(**search_params)

            # Extract and return the analysis - access SearchResult attributes directly
            return {
                "analysis": getattr(result, "answer", "No analysis available"),
                "sources": getattr(result, "sources", []),
                "follow_up_questions": getattr(result, "follow_up_questions", []),
                "related_topics": getattr(result, "related_topics", []),
                "query_used": query,
                "mode_used": request.perplexity_mode,
                "sources_used": request.sources
            }

        except Exception as e:
            logger.error(f"Error analyzing response with Perplexity: {str(e)}")
            return {
                "analysis": f"Error during analysis: {str(e)}",
                "sources": [],
                "follow_up_questions": [],
                "related_topics": [],
                "query_used": request.analysis_query or "Auto-generated query",
                "mode_used": request.perplexity_mode,
                "sources_used": request.sources,
                "error": str(e)
            }

# Global instances
webhook_client = WebhookClient()
response_analyzer = ResponseAnalyzer()

# MCP Tools
@mcp.tool()
async def call_webhook(
    url: str,
    method: str = "POST",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[Dict[str, Any], str]] = None,
    auth_type: Optional[str] = None,
    auth_credentials: Optional[Dict[str, str]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Call an external webhook with authentication support.

    Args:
        url: URL of the webhook to call
        method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD)
        headers: HTTP headers
        body: Request body (can be dict for JSON or string)
        auth_type: Authentication type (bearer, basic, api_key)
        auth_credentials: Authentication credentials
        timeout: Request timeout in seconds

    Returns:
        Webhook response including status code, headers, body, and response time
    """
    try:
        request = WebhookRequest(
            url=url,
            method=method,
            headers=headers,
            body=body,
            auth_type=auth_type,
            auth_credentials=auth_credentials,
            timeout=timeout
        )

        response = await webhook_client.call_webhook(request)

        logger.info(f"Webhook call completed: {method} {url} -> {response.status_code} ({response.response_time:.2f}s)")

        return response.model_dump()

    except Exception as e:
        logger.error(f"Error calling webhook: {str(e)}")
        return {
            "status_code": 0,
            "headers": {},
            "body": "",
            "response_time": 0,
            "error": f"Failed to call webhook: {str(e)}"
        }

@mcp.tool()
async def analyze_with_perplexity(
    response_data: Union[Dict[str, Any], str],
    analysis_query: Optional[str] = None,
    perplexity_mode: str = "auto",
    perplexity_model: Optional[str] = None,
    sources: List[str] = ["web"]
) -> Dict[str, Any]:
    """
    Analyze webhook response data using Perplexity AI.

    Args:
        response_data: The webhook response data to analyze
        analysis_query: Custom analysis query (optional, will generate one if not provided)
        perplexity_mode: Perplexity search mode (auto, concise, detailed)
        perplexity_model: Specific Perplexity model to use
        sources: Sources for Perplexity search (web, academic, news, etc.)

    Returns:
        Analysis results including insights, sources, and follow-up questions
    """
    try:
        request = AnalysisRequest(
            response_data=response_data,
            analysis_query=analysis_query,
            perplexity_mode=perplexity_mode,
            perplexity_model=perplexity_model,
            sources=sources
        )

        result = await response_analyzer.analyze_response(request)

        logger.info(f"Perplexity analysis completed using mode: {perplexity_mode}")

        return result

    except Exception as e:
        logger.error(f"Error analyzing with Perplexity: {str(e)}")
        return {
            "analysis": f"Error during analysis: {str(e)}",
            "sources": [],
            "follow_up_questions": [],
            "related_topics": [],
            "query_used": analysis_query or "Auto-generated query",
            "mode_used": perplexity_mode,
            "sources_used": sources,
            "error": str(e)
        }

@mcp.tool()
async def webhook_and_analyze(
    url: str,
    method: str = "POST",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[Dict[str, Any], str]] = None,
    auth_type: Optional[str] = None,
    auth_credentials: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    analysis_query: Optional[str] = None,
    perplexity_mode: str = "auto",
    perplexity_model: Optional[str] = None,
    sources: List[str] = ["web"]
) -> Dict[str, Any]:
    """
    Call a webhook and then analyze the response using Perplexity AI in one operation.

    Args:
        url: URL of the webhook to call
        method: HTTP method
        headers: HTTP headers
        body: Request body
        auth_type: Authentication type
        auth_credentials: Authentication credentials
        timeout: Request timeout
        analysis_query: Custom analysis query
        perplexity_mode: Perplexity search mode
        perplexity_model: Specific Perplexity model
        sources: Sources for Perplexity search

    Returns:
        Combined webhook response and analysis results
    """
    try:
        # Call the webhook
        webhook_result = await call_webhook(
            url=url,
            method=method,
            headers=headers,
            body=body,
            auth_type=auth_type,
            auth_credentials=auth_credentials,
            timeout=timeout
        )

        # Only analyze if webhook call was successful
        if webhook_result.get("status_code", 0) > 0:
            # Analyze the response
            analysis_result = await analyze_with_perplexity(
                response_data=webhook_result.get("body", ""),
                analysis_query=analysis_query,
                perplexity_mode=perplexity_mode,
                perplexity_model=perplexity_model,
                sources=sources
            )
        else:
            analysis_result = {
                "analysis": "Webhook call failed, unable to analyze response",
                "sources": [],
                "follow_up_questions": [],
                "related_topics": [],
                "query_used": analysis_query or "N/A",
                "mode_used": perplexity_mode,
                "sources_used": sources,
                "error": "Webhook call failed"
            }

        return {
            "webhook_response": webhook_result,
            "perplexity_analysis": analysis_result,
            "timestamp": time.time()
        }

    except Exception as e:
        logger.error(f"Error in webhook_and_analyze: {str(e)}")
        return {
            "webhook_response": {
                "status_code": 0,
                "headers": {},
                "body": "",
                "response_time": 0,
                "error": f"Operation failed: {str(e)}"
            },
            "perplexity_analysis": {
                "analysis": f"Operation failed: {str(e)}",
                "sources": [],
                "follow_up_questions": [],
                "related_topics": [],
                "query_used": analysis_query or "N/A",
                "mode_used": perplexity_mode,
                "sources_used": sources,
                "error": str(e)
            },
            "timestamp": time.time()
        }

# MCP Resources
@mcp.resource("webhook://config")
async def get_webhook_config() -> Dict[str, Any]:
    """Get current webhook configuration"""
    return {
        "default_timeout": config.default_timeout,
        "max_retries": config.max_retries,
        "retry_delay": config.retry_delay,
        "user_agent": config.user_agent,
        "perplexity_api_url": config.perplexity_api_url,
        "perplexity_timeout": config.perplexity_timeout,
        "default_perplexity_mode": config.default_perplexity_mode,
        "default_perplexity_sources": config.default_perplexity_sources
    }

@mcp.resource("webhook://stats")
async def get_webhook_stats() -> Dict[str, Any]:
    """Get webhook call statistics"""
    return {
        "total_calls": 0,
        "successful_calls": 0,
        "failed_calls": 0,
        "average_response_time": 0,
        "last_call_timestamp": None
    }

@mcp.resource("webhook://health")
async def get_health() -> Dict[str, Any]:
    """Get server health status"""
    try:
        # Test Perplexity API connection
        api = await get_perplexity_api()
        perplexity_status = "connected" if api else "disconnected"
    except Exception:
        perplexity_status = "error"

    return {
        "status": "healthy",
        "timestamp": time.time(),
        "server": "webhook-perplexity",
        "version": "1.0.0",
        "perplexity_api": perplexity_status,
        "configuration": {
            "default_timeout": config.default_timeout,
            "max_retries": config.max_retries
        }
    }

# Lifecycle management
async def cleanup():
    """Clean up resources"""
    try:
        await webhook_client.close()
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Main entry point
if __name__ == "__main__":
    import sys

    # Check if we should run in HTTP mode or stdio mode
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run in HTTP mode
        port = int(os.getenv("WEBHOOK_MCP_PORT", "8000"))
        logger.info(f"Starting Webhook MCP server in HTTP mode on port {port}")
        try:
            # FastMCP might not support SSE transport directly, try stdio mode
            # For HTTP mode, we might need to use a different approach or library
            logger.warning("HTTP mode not supported with current FastMCP version, using stdio mode")
            mcp.run()
        except KeyboardInterrupt:
            logger.info("Shutting down Webhook MCP server")
        finally:
            asyncio.run(cleanup())
    else:
        # Run in stdio mode (default for MCP)
        logger.info("Starting Webhook MCP server in stdio mode")
        try:
            # Keep the server running indefinitely
            # MCP servers typically run until interrupted
            import signal
            import time

            # Set up signal handlers
            def signal_handler(signum, frame):
                logger.info(f"Received signal {signum}, shutting down...")
                raise KeyboardInterrupt

            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGINT, signal_handler)

            # Run the MCP server
            mcp.run()
        except KeyboardInterrupt:
            logger.info("Shutting down Webhook MCP server")
        finally:
            asyncio.run(cleanup())
