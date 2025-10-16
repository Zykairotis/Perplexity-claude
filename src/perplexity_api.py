"""
Perplexity AI API Wrapper
A comprehensive Python API wrapper for Perplexity AI with streaming support
"""

import sys
import os
# Add the current directory to Python path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import asyncio
import json
import re
import time
from typing import Dict, List, Optional, Union, AsyncGenerator, Any
from dataclasses import dataclass, asdict
from enum import Enum
from perplexity_fixed import Client, PerplexityError
from perplexity_profiles import SearchProfile, apply_profile_to_query, validate_profile


def load_cookies_from_env() -> Dict[str, str]:
    """Load cookies from JSON file path specified in .example.env"""
    cookies = {}

    # Try multiple possible paths for cookies.json
    possible_paths = [
        "cookies.json",  # Current directory
        "/app/cookies.json",  # Docker container path
        "../cookies.json",  # Parent directory
        "/home/mewtwo/Zykairotis/Perplexity-claude/cookies.json",  # Original path
    ]

    for cookie_path in possible_paths:
        try:
            with open(cookie_path, 'r') as f:
                cookie_data = json.load(f)
                cookies = cookie_data.get('cookies', {})
                if cookies:
                    print(f"✅ Loaded {len(cookies)} cookies from {cookie_path}")
                    return cookies
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            continue

    print(f"⚠️ Could not load cookies from any of the attempted paths: {possible_paths}")
    return {}


class SearchMode(Enum):
    """Available search modes"""
    AUTO = "auto"
    PRO = "pro"
    REASONING = "reasoning"
    DEEP_RESEARCH = "deep research"


class SearchSource(Enum):
    """Available search sources"""
    WEB = "web"
    SCHOLAR = "scholar"
    SOCIAL = "social"


class ProModel(Enum):
    """Available models for Pro mode"""
    SONAR = "sonar"
    GPT_4_5 = "gpt-4.5"
    GPT_4O = "gpt-4o"
    CLAUDE_3_7_SONNET = "claude 3.7 sonnet"
    GEMINI_2_0_FLASH = "gemini 2.0 flash"
    GROK_2 = "grok-2"
    CLAUDE_45_SONNET = "claude45sonnet"
    CLAUDE_45_SONNET_THINKING = "claude45sonnetthinking"
    GPT_5 = "gpt5"
    GPT_5_THINKING = "gpt5thinking"


class ReasoningModel(Enum):
    """Available models for Reasoning mode"""
    R1 = "r1"
    O3_MINI = "o3-mini"
    CLAUDE_3_7_SONNET = "claude 3.7 sonnet"


@dataclass
class SearchResult:
    """Structured search result"""
    query: str
    answer: str
    sources: List[Dict[str, Any]]
    mode: str
    model: Optional[str]
    language: str
    timestamp: float
    backend_uuid: Optional[str] = None
    context_uuid: Optional[str] = None
    related_queries: List[str] = None
    chunks: List[str] = None
    raw_response: Dict[str, Any] = None
    prompt_source: Optional[str] = None
    query_source: Optional[str] = None
    should_ask_for_mcp_tool_confirmation: Optional[bool] = None
    search_focus: Optional[str] = None
    timezone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2, default=str)


@dataclass
class StreamChunk:
    """Streaming response chunk"""
    step_type: str
    content: Dict[str, Any]
    timestamp: float
    raw_data: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class PerplexityAPIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, error_code: Optional[str] = None, raw_response: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.raw_response = raw_response


class PerplexityAPI:
    """
    Comprehensive Perplexity AI API Wrapper
    
    Provides both synchronous-style and streaming interfaces for Perplexity AI
    """
    
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        """
        Initialize the API wrapper

        Args:
            cookies: Dictionary of cookies for authentication. If None, loads from environment.
        """
        self.cookies = cookies or load_cookies_from_env()
        self._client = None
        self._session_info = {}
    
    async def _get_client(self) -> Client:
        """Get or create the client instance"""
        if self._client is None:
            self._client = await Client(self.cookies)
        return self._client
    
    async def search(
        self,
        query: str,
        mode: Union[SearchMode, str] = SearchMode.AUTO,
        model: Optional[Union[ProModel, ReasoningModel, str]] = None,
        sources: List[Union[SearchSource, str]] = None,
        language: str = "en-US",
        files: Optional[Dict[str, str]] = None,
        follow_up: Optional[Dict[str, Any]] = None,
        incognito: bool = False,
        timeout: Optional[float] = 60.0,
        raw_response: bool = False,
        profile: Optional[Union[SearchProfile, str]] = None,
        prompt_source: str = "user",
        query_source: str = "home",
        should_ask_for_mcp_tool_confirmation: bool = True,
        search_focus: str = "internet",
        timezone: str = "Europe/Berlin"
    ) -> Union[SearchResult, Dict[str, Any]]:
        """
        Perform a search query

        Args:
            query: Search query string
            mode: Search mode (auto, pro, reasoning, deep research)
            model: Model to use (only for pro/reasoning modes)
            sources: List of sources to search (web, scholar, social)
            language: Language code (default: en-US)
            files: Dictionary of files to upload {filename: content}
            follow_up: Previous query info for follow-up queries
            incognito: Enable incognito mode
            timeout: Request timeout in seconds
            raw_response: If True, return raw API response instead of SearchResult
            profile: Search profile to enhance query (research, code_analysis, troubleshooting, etc.)
            prompt_source: Source of the prompt (default: "user")
            query_source: Source of the query (default: "home")
            should_ask_for_mcp_tool_confirmation: Whether to ask for MCP tool confirmation (default: True)
            search_focus: Focus of the search (default: "internet")
            timezone: Timezone for the search (default: "Europe/Berlin")

        Returns:
            SearchResult object with structured response or raw Dict if raw_response=True

        Raises:
            PerplexityAPIError: If the search fails
        """
        try:
            # Convert enums to strings
            if isinstance(mode, SearchMode):
                mode = mode.value
            if isinstance(model, (ProModel, ReasoningModel)):
                model = model.value
            if sources is None:
                sources = [SearchSource.WEB.value]
            else:
                sources = [s.value if isinstance(s, SearchSource) else s for s in sources]

            # Handle profile parameter
            search_profile = None
            if profile:
                if isinstance(profile, str):
                    search_profile = validate_profile(profile)
                else:
                    search_profile = profile

            # Apply profile enhancement to query
            enhanced_query = apply_profile_to_query(query, search_profile)

            client = await self._get_client()

            # Perform the search with enhanced query
            start_time = time.time()
            response = await client.search(
                query=enhanced_query,
                mode=mode,
                model=model,
                sources=sources,
                files=files or {},
                language=language,
                follow_up=follow_up,
                incognito=incognito,
                prompt_source=prompt_source,
                query_source=query_source,
                should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
                search_focus=search_focus,
                timezone=timezone
            )
            
            if isinstance(response, dict) and 'error' in response:
                raise PerplexityAPIError(
                    f"Search failed: {response.get('message', 'Unknown error')}",
                    error_code=response.get('error'),
                    raw_response=response
                )
            
            # Return raw response if requested
            if raw_response:
                return response
            
            # Parse the response
            return self._parse_response(query, response, mode, model, language, start_time, prompt_source, query_source, should_ask_for_mcp_tool_confirmation, search_focus, timezone)
            
        except Exception as e:
            if isinstance(e, PerplexityAPIError):
                raise
            raise PerplexityAPIError(f"Search failed: {str(e)}", raw_response={"error": str(e)})
    
    async def search_stream(
        self,
        query: str,
        mode: Union[SearchMode, str] = SearchMode.AUTO,
        model: Optional[Union[ProModel, ReasoningModel, str]] = None,
        sources: List[Union[SearchSource, str]] = None,
        language: str = "en-US",
        files: Optional[Dict[str, str]] = None,
        follow_up: Optional[Dict[str, Any]] = None,
        incognito: bool = False,
        profile: Optional[Union[SearchProfile, str]] = None,
        prompt_source: str = "user",
        query_source: str = "home",
        should_ask_for_mcp_tool_confirmation: bool = True,
        search_focus: str = "internet",
        timezone: str = "Europe/Berlin"
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Perform a streaming search query

        Args:
            query: Search query string
            mode: Search mode (auto, pro, reasoning, deep research)
            model: Model to use (only for pro/reasoning modes)
            sources: List of sources to search (web, scholar, social)
            language: Language code (default: en-US)
            files: Dictionary of files to upload {filename: content}
            follow_up: Previous query info for follow-up queries
            incognito: Enable incognito mode
            profile: Search profile to enhance query (research, code_analysis, troubleshooting, etc.)
            prompt_source: Source of the prompt (default: "user")
            query_source: Source of the query (default: "home")
            should_ask_for_mcp_tool_confirmation: Whether to ask for MCP tool confirmation (default: True)
            search_focus: Focus of the search (default: "internet")
            timezone: Timezone for the search (default: "Europe/Berlin")

        Yields:
            StreamChunk objects with real-time updates

        Raises:
            PerplexityAPIError: If the search fails
        """
        try:
            # Convert enums to strings
            if isinstance(mode, SearchMode):
                mode = mode.value
            if isinstance(model, (ProModel, ReasoningModel)):
                model = model.value
            if sources is None:
                sources = [SearchSource.WEB.value]
            else:
                sources = [s.value if isinstance(s, SearchSource) else s for s in sources]

            # Handle profile parameter
            search_profile = None
            if profile:
                if isinstance(profile, str):
                    search_profile = validate_profile(profile)
                else:
                    search_profile = profile

            # Apply profile enhancement to query
            enhanced_query = apply_profile_to_query(query, search_profile)

            client = await self._get_client()

            # Get the stream with enhanced query
            stream = client.search_stream(
                query=enhanced_query,
                mode=mode,
                model=model,
                sources=sources,
                files=files or {},
                language=language,
                follow_up=follow_up,
                incognito=incognito,
                prompt_source=prompt_source,
                query_source=query_source,
                should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
                search_focus=search_focus,
                timezone=timezone
            )
            
            async for chunk in stream:
                if isinstance(chunk, dict) and 'error' in chunk:
                    raise PerplexityAPIError(
                        f"Stream error: {chunk.get('message', 'Unknown error')}",
                        error_code=chunk.get('error'),
                        raw_response=chunk
                    )
                
                # Parse and yield stream chunks
                parsed_chunks = self._parse_stream_chunk(chunk)
                for parsed_chunk in parsed_chunks:
                    yield parsed_chunk
                    
        except Exception as e:
            if isinstance(e, PerplexityAPIError):
                raise
            raise PerplexityAPIError(f"Streaming search failed: {str(e)}", raw_response={"error": str(e)})
    
    def _parse_response(self, query: str, response: Dict[str, Any], mode: str,
                       model: Optional[str], language: str, start_time: float,
                       prompt_source: str = "user", query_source: str = "home",
                       should_ask_for_mcp_tool_confirmation: bool = True,
                       search_focus: str = "internet", timezone: str = "Europe/Berlin") -> SearchResult:
        """Parse the API response into a SearchResult"""
        answer = ""
        sources = []
        backend_uuid = response.get('backend_uuid')
        context_uuid = response.get('context_uuid')
        related_queries = []
        chunks = []

        # Enhanced extraction for answer and sources from response
        if 'text' in response and isinstance(response['text'], list):
            for step in response['text']:
                if step.get('step_type') == 'FINAL':
                    answer_content = step.get('content', {})
                    if 'answer' in answer_content:
                        raw_answer = answer_content['answer']
                        try:
                            # Handle nested JSON structure (double parsing)
                            if isinstance(raw_answer, str):
                                answer_data = json.loads(raw_answer)
                            else:
                                answer_data = raw_answer

                            # Extract the main answer with fallbacks
                            if isinstance(answer_data, dict):
                                answer = answer_data.get('answer', '')
                                sources = answer_data.get('web_results', answer_data.get('sources', []))
                                chunks = answer_data.get('chunks', [])
                            else:
                                answer = str(answer_data)

                        except (json.JSONDecodeError, TypeError) as e:
                            # If parsing fails, try to extract from nested structure
                            try:
                                # Try to find JSON in the raw string
                                json_match = re.search(r'\{.*\}', raw_answer, re.DOTALL)
                                if json_match:
                                    answer_data = json.loads(json_match.group())
                                    answer = answer_data.get('answer', str(raw_answer))
                                    sources = answer_data.get('web_results', answer_data.get('sources', []))
                                else:
                                    # If no JSON found, use raw answer
                                    answer = str(raw_answer)
                            except:
                                # Final fallback - use raw answer as string
                                answer = str(raw_answer)

        # Extract related queries if available
        if 'related_queries' in response:
            related_queries = response['related_queries']

        return SearchResult(
            query=query,
            answer=answer,
            sources=sources,
            mode=mode,
            model=model,
            language=language,
            timestamp=start_time,
            backend_uuid=backend_uuid,
            context_uuid=context_uuid,
            related_queries=related_queries,
            chunks=chunks,
            raw_response=response,
            prompt_source=prompt_source,
            query_source=query_source,
            should_ask_for_mcp_tool_confirmation=should_ask_for_mcp_tool_confirmation,
            search_focus=search_focus,
            timezone=timezone
        )
    
    def _parse_stream_chunk(self, chunk: Dict[str, Any]) -> List[StreamChunk]:
        """Parse a stream chunk into StreamChunk objects"""
        chunks = []
        timestamp = time.time()
        
        if 'text' in chunk and isinstance(chunk['text'], list):
            for step in chunk['text']:
                step_type = step.get('step_type', 'unknown')
                content = step.get('content', {})
                
                chunks.append(StreamChunk(
                    step_type=step_type,
                    content=content,
                    timestamp=timestamp,
                    raw_data=chunk
                ))
        
        return chunks
    
    async def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        client = await self._get_client()
        
        # Handle float('inf') values that aren't JSON serializable
        copilot_remaining = getattr(client, 'copilot', 0)
        file_uploads_remaining = getattr(client, 'file_upload', 0)
        
        # Convert inf to a large number or -1 to indicate unlimited
        if copilot_remaining == float('inf'):
            copilot_remaining = -1  # -1 indicates unlimited
        if file_uploads_remaining == float('inf'):
            file_uploads_remaining = -1  # -1 indicates unlimited
            
        return {
            'has_cookies': bool(self.cookies),
            'copilot_queries_remaining': copilot_remaining,
            'file_uploads_remaining': file_uploads_remaining,
            'owns_account': getattr(client, 'own', False)
        }
    
    async def close(self):
        """Close the client session"""
        if self._client and hasattr(self._client, 'session'):
            await self._client.session.close()
        self._client = None


# Convenience functions for quick usage
async def quick_search(query: str, mode: str = "auto", cookies: Optional[Dict] = None) -> str:
    """
    Quick search function that returns just the answer text
    
    Args:
        query: Search query
        mode: Search mode (auto, pro, reasoning, deep research)
        cookies: Optional cookies dictionary
        
    Returns:
        Answer text string
    """
    api = PerplexityAPI(cookies)
    try:
        result = await api.search(query, mode=mode)
        return result.answer
    finally:
        await api.close()


async def search_with_sources(query: str, mode: str = "auto", cookies: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Search function that returns answer with sources
    
    Args:
        query: Search query
        mode: Search mode (auto, pro, reasoning, deep research)
        cookies: Optional cookies dictionary
        
    Returns:
        Dictionary with answer and sources
    """
    api = PerplexityAPI(cookies)
    try:
        result = await api.search(query, mode=mode)
        return {
            'answer': result.answer,
            'sources': result.sources,
            'related_queries': result.related_queries
        }
    finally:
        await api.close()


async def raw_search(query: str, mode: str = "auto", model: Optional[str] = None, 
                    sources: Optional[List[str]] = None, cookies: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Raw search function that returns the unprocessed API response
    
    Args:
        query: Search query
        mode: Search mode (auto, pro, reasoning, deep research)
        model: Model to use (only for pro/reasoning modes)
        sources: List of sources to search (web, scholar, social)
        cookies: Optional cookies dictionary
        
    Returns:
        Raw API response dictionary
    """
    api = PerplexityAPI(cookies)
    try:
        response = await api.search(query, mode=mode, model=model, sources=sources, raw_response=True)
        return response
    finally:
        await api.close()


# Example usage and testing
async def example_usage():
    """Example usage of the API wrapper"""
    
    # Initialize with cookies (optional)
    cookies = {
        'pplx.visitor-id': 'your-visitor-id',
        'pplx.session-id': 'your-session-id',
        # Add your cookies here
    }
    
    api = PerplexityAPI(cookies)
    
    try:
        # Basic search
        print("=== Basic Search ===")
        result = await api.search("What is artificial intelligence?")
        print(f"Answer: {result.answer[:200]}...")
        print(f"Sources: {len(result.sources)}")
        
        # Pro search with specific model
        print("\n=== Pro Search ===")
        result = await api.search(
            "Explain quantum computing",
            mode=SearchMode.PRO,
            model=ProModel.SONAR
        )
        print(f"Answer: {result.answer[:200]}...")
        
        # Streaming search
        print("\n=== Streaming Search ===")
        async for chunk in api.search_stream("Latest developments in AI"):
            if chunk.step_type == "SEARCH_WEB":
                print(f"🔍 Searching: {chunk.content}")
            elif chunk.step_type == "SEARCH_RESULTS":
                results = chunk.content.get('web_results', [])
                print(f"📄 Found {len(results)} sources")
            elif chunk.step_type == "FINAL":
                print("✅ Search completed")
        
        # Get session info
        print("\n=== Session Info ===")
        session_info = await api.get_session_info()
        print(json.dumps(session_info, indent=2))
        
    finally:
        await api.close()


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())