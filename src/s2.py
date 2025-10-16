from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
import httpx
import json
import time
import tiktoken
from typing import List, Dict, Any, Optional
import re

app = FastAPI(
    title="Custom LiteLLM-like Perplexity Proxy",
    description="A LiteLLM-style API proxy for Perplexity AI wrapper. Supports non-streaming /v1/completions and /v1/chat/completions endpoints. This proxy communicates with the main Perplexity server running on port 9522.",
    version="1.0.0"
)

class URLNormalizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log incoming request
        print(f"🔍 Incoming request: {request.method} {request.url.path}")

        # Fix double slashes in URL path
        if "//" in request.url.path:
            # Normalize double slashes to single slashes, but preserve leading slash
            normalized_path = "/" + "/".join(part for part in request.url.path.split("/") if part)
            print(f"🔧 Normalizing URL: {request.url.path} -> {normalized_path}")

            # Create new URL with normalized path
            from starlette.datastructures import URL
            new_url = request.url.replace(path=normalized_path)
            request._url = new_url

        response = await call_next(request)
        print(f"📤 Response status: {response.status_code}")
        return response

# Add the middleware
app.add_middleware(URLNormalizeMiddleware)

# Perplexity server URL (configured to communicate with existing server on port 9522)
PERPLEXITY_URL = "http://localhost:9522/api/search/files/stream"

# Fixed parameters (can be customized later)
DEFAULT_LANGUAGE = "en-US"
DEFAULT_INCOGNITO = False
DEFAULT_RAW_RESPONSE = False
DEFAULT_SOURCES = "web"  # Comma-separated, e.g., "web,scholar"

# Initialize tiktoken encoding for GPT-4
encoding = tiktoken.encoding_for_model("gpt-4")

# Helper function to count tokens using GPT-4 encoding
def count_tokens(text: str) -> int:
    """Count tokens in text using GPT-4 encoding"""
    tokens = encoding.encode(text)
    return len(tokens)

# Model mapping: Parse model name to determine mode and model_preference
# Example: model="pro-grok4" -> mode="pro", model_preference="grok4"
# If no prefix, default to "pro"
def parse_model(model: str) -> tuple[str, Optional[str]]:
    parts = model.split("-", maxsplit=1)
    if len(parts) == 2:
        mode, model_pref = parts
        # Map deep and lab modes to their specific models
        if mode == "deep":
            return "deep research", "pplx_alpha"
        elif mode == "lab":
            return "deep lab", "pplx_beta"
        return mode, model_pref
    return "pro", model  # Default to pro mode with model as preference

# Helper to format messages as a single query (for chat/completions)
def format_messages_as_query(messages: List[Dict[str, str]]) -> str:
    # Extract just the content without role prefixes
    formatted = []
    for msg in messages:
        content = msg.get("content", "")
        if content:
            formatted.append(content)
    return "\n".join(formatted)

# Import profile support
try:
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from perplexity_profiles import validate_profile, apply_profile_to_query
except ImportError:
    # Profile support not available, will continue without profiles
    validate_profile = None
    apply_profile_to_query = None

# Helper to call Perplexity and parse the SSE response for the answer
async def call_perplexity(query: str, mode: str, model_preference: Optional[str], continue_chat: bool, profile: Optional[str] = None,
                         prompt_source: Optional[str] = None, query_source: Optional[str] = None,
                         should_ask_for_mcp_tool_confirmation: Optional[bool] = None,
                         search_focus: Optional[str] = None, timezone: Optional[str] = None) -> str:
    # Apply profile enhancement if available
    enhanced_query = query
    if profile and apply_profile_to_query and validate_profile:
        try:
            search_profile = validate_profile(profile)
            if search_profile:
                enhanced_query = apply_profile_to_query(query, search_profile)
                print(f"🎯 Applied profile '{profile}' to query")
            else:
                print(f"⚠️ Invalid profile '{profile}', using original query")
        except Exception as e:
            print(f"⚠️ Error applying profile '{profile}': {e}, using original query")

    async with httpx.AsyncClient() as client:
        form_data = {
            "query": enhanced_query,
            "mode": mode,
            "model_preference": model_preference if model_preference else "",
            "incognito": str(DEFAULT_INCOGNITO).lower(),
            "continue_chat": str(continue_chat).lower(),
            "raw_response": str(DEFAULT_RAW_RESPONSE).lower(),
            "language": DEFAULT_LANGUAGE,
            "sources": DEFAULT_SOURCES,
        }

        # Add profile to form data if specified
        if profile:
            form_data["profile"] = profile

        # Add new optional fields if specified
        if prompt_source:
            form_data["prompt_source"] = prompt_source
        if query_source:
            form_data["query_source"] = query_source
        if should_ask_for_mcp_tool_confirmation is not None:
            form_data["should_ask_for_mcp_tool_confirmation"] = str(should_ask_for_mcp_tool_confirmation).lower()
        if search_focus:
            form_data["search_focus"] = search_focus
        if timezone:
            form_data["timezone"] = timezone

        files = {}

        try:
            response = await client.post(PERPLEXITY_URL, data=form_data, files=files if files else None, timeout=360.0)
            response.raise_for_status()

            full_response = response.text


            # Handle the response which contains literal \n sequences instead of actual newlines
            # First decode the escaped newlines to actual newlines
            decoded_response = full_response.replace('\\n', '\n').replace('\\r', '\r')

            # Then normalize line endings
            normalized_response = decoded_response.replace('\r\n', '\n').replace('\r', '\n')

            # Split on double newlines to get event blocks
            event_blocks = normalized_response.split('\n\n')
            filtered_blocks = [block.strip() for block in event_blocks if block.strip()]

            # Extract JSON data from each block that starts with 'data: '
            events = []
            for block in filtered_blocks:
                if block.startswith('data: '):
                    data_str = block[6:].strip()  # Remove 'data: ' prefix
                    events.append(data_str)



            answer = ""
            for i, data_str in enumerate(events):
                print(f"Debug - Event {i} preview: {data_str[:200]}...")
                if data_str == '[DONE]':
                    break
                try:
                    # Check if this is a FINAL event by looking for the pattern manually first
                    if '"step_type": "FINAL"' in data_str:
                        print("\n>>> Debug - Found FINAL chunk (manual detection).")

                        # Manual extraction approach for malformed JSON
                        # Look for the answer field pattern: "answer": "{\"answer\": \"actual_content..."
                        import re

                        # Pattern to match the nested answer structure
                        answer_pattern = r'"answer":\s*"{\s*\\"answer\\":\s*\\"([^"]*(?:\\"[^"]*)*)'
                        match = re.search(answer_pattern, data_str, re.DOTALL)

                        if match:
                            raw_answer = match.group(1)
                            # Clean up the extracted answer
                            answer = (raw_answer
                                    .replace('\\"', '"')
                                    .replace('\\\\', '\\')
                                    .replace('\\n', '\n')
                                    .replace('\\t', '\t')
                                    .replace('\\r', '\r')
                                    .replace('\\/', '/')
                                    .replace('\\u2014', '—')
                                    .replace('\\u2019', "'")
                                    .replace('\\u201c', '"')
                                    .replace('\\u201d', '"')
                                    .replace('\\u2013', '–')
                                    .replace('\\u2018', "'")
                                    .replace('\\u2026', '…')
                                    .replace('\\u00a0', ' ')
                                    .strip())

                            if answer and len(answer) > 10:  # Basic sanity check
                                print(f"Debug - Manual extraction successful: '{answer[:100]}...'")
                                break

                        # Fallback: try broader pattern matching
                        broader_pattern = r'"answer":\s*"[^"]*"([^"]+)'
                        broader_match = re.search(broader_pattern, data_str, re.DOTALL)
                        if broader_match:
                            raw_content = broader_match.group(1)
                            # Extract readable text, removing JSON artifacts
                            clean_content = re.sub(r'[{}",\\]', ' ', raw_content)
                            clean_content = re.sub(r'\s+', ' ', clean_content).strip()

                            if len(clean_content) > 50:  # Must be substantial content
                                answer = clean_content
                                print(f"Debug - Fallback extraction successful: '{answer[:100]}...'")
                                break

                    # Fallback to normal JSON parsing for non-FINAL events
                    try:
                        chunk = json.loads(data_str)
                        if chunk.get("type") == "chunk" and chunk.get("data", {}).get("step_type") == "FINAL":
                            print("\n>>> Debug - Found FINAL chunk via JSON parsing.")
                            final_content = chunk.get("data", {}).get("content", {})
                            answer_json_str = final_content.get("answer", "")

                            if answer_json_str:
                                try:
                                    answer_data = json.loads(answer_json_str)
                                    answer = answer_data.get("answer", "")
                                    if answer:
                                        print(f"Debug - JSON parsing successful: '{answer[:100]}...'")
                                        break
                                except json.JSONDecodeError:
                                    print("Debug - Nested JSON failed, already handled above")
                    except json.JSONDecodeError:
                        # Skip non-FINAL events that fail JSON parsing
                        continue

                except json.JSONDecodeError as e:
                    print(f"Debug - Error decoding JSON from event: {e}")
                    print(f"Debug - Problematic data string (first 300 chars): {data_str[:300]}")
                    continue

            if not answer:

                raise ValueError("No valid answer found in the response")

            return answer

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Perplexity API error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Pydantic models for OpenAI-like requests following Chat Completions API structure
from pydantic import Field, field_validator
from enum import Enum
from typing import Union

class MessageRole(str, Enum):
    """Valid message roles for chat completions"""
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"  # For function calling
    tool = "tool"  # For tool calling

class ToolCall(BaseModel):
    """Tool call structure for function calling"""
    id: str
    type: str = "function"
    function: Dict[str, Any]

class ChatMessage(BaseModel):
    """Individual message in a chat conversation"""
    role: MessageRole
    content: Optional[str] = None  # Can be None for tool calls
    name: Optional[str] = None  # For multi-user scenarios
    tool_calls: Optional[List[ToolCall]] = None  # For function calling
    tool_call_id: Optional[str] = None  # For tool responses

class Function(BaseModel):
    """Function definition for function calling"""
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class Tool(BaseModel):
    """Tool definition for tool calling"""
    type: str = "function"
    function: Function

class ResponseFormat(BaseModel):
    """Response format specification"""
    type: str = Field("text", description="Response format type")

class CompletionRequest(BaseModel):
    """Request model for /v1/completions endpoint - Full OpenAI compatibility"""
    model: str
    prompt: Union[str, List[str], List[int], List[List[int]]]
    suffix: Optional[str] = Field(None, description="Suffix to append after completion")
    max_tokens: Optional[int] = Field(None, ge=1, le=8192, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(1.0, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    n: Optional[int] = Field(1, ge=1, le=128, description="Number of completions to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream responses")
    logprobs: Optional[int] = Field(None, ge=0, le=5, description="Include log probabilities")
    echo: Optional[bool] = Field(False, description="Echo back the prompt")
    stop: Optional[Union[str, List[str]]] = Field(None, description="Stop sequences")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Presence penalty")
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    best_of: Optional[int] = Field(1, ge=1, le=20, description="Best of N completions")
    logit_bias: Optional[Dict[str, float]] = Field(None, description="Token bias")
    user: Optional[str] = Field(None, description="End-user identifier")
    seed: Optional[int] = Field(None, description="Seed for reproducible outputs")
    profile: Optional[str] = Field(None, description="Search profile for enhanced queries (research, code_analysis, etc.)")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt (user_input, api_call, etc.)")
    query_source: Optional[str] = Field(None, description="Source of the query (manual, automated, etc.)")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(True, description="Whether to ask for MCP tool confirmation")
    search_focus: Optional[str] = Field(None, description="Focus area for search (web, academic, news, etc.)")
    timezone: Optional[str] = Field("UTC", description="Timezone for the request")

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v):
        """Convert prompt to string if needed"""
        if isinstance(v, list):
            if all(isinstance(item, str) for item in v):
                return "\n".join(v)
            elif all(isinstance(item, int) for item in v):
                # Token IDs - convert back to text (simplified)
                return f"[Token sequence of length {len(v)}]"
            elif all(isinstance(item, list) for item in v):
                # Multiple token sequences
                return f"[Multiple token sequences: {len(v)} sequences]"
        return str(v)

class ChatCompletionRequest(BaseModel):
    """Request model for /v1/chat/completions endpoint - Full OpenAI compatibility"""
    model: str
    messages: List[ChatMessage] = Field(..., min_items=1, description="List of messages in the conversation")
    functions: Optional[List[Function]] = Field(None, description="Available functions (deprecated)")
    function_call: Optional[Union[str, Dict[str, str]]] = Field(None, description="Function call control (deprecated)")
    tools: Optional[List[Tool]] = Field(None, description="Available tools")
    tool_choice: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Tool choice control")
    max_tokens: Optional[int] = Field(None, ge=1, le=8192, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(1.0, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    n: Optional[int] = Field(1, ge=1, le=128, description="Number of completions to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream responses")
    stop: Optional[Union[str, List[str]]] = Field(None, description="Stop sequences")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Presence penalty")
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    logit_bias: Optional[Dict[str, float]] = Field(None, description="Token bias")
    user: Optional[str] = Field(None, description="End-user identifier")
    seed: Optional[int] = Field(None, description="Seed for reproducible outputs")
    response_format: Optional[ResponseFormat] = Field(None, description="Response format")
    top_logprobs: Optional[int] = Field(None, ge=0, le=20, description="Top log probabilities")
    logprobs: Optional[bool] = Field(False, description="Include log probabilities")
    profile: Optional[str] = Field(None, description="Search profile for enhanced queries (research, code_analysis, etc.)")
    prompt_source: Optional[str] = Field(None, description="Source of the prompt (user_input, api_call, etc.)")
    query_source: Optional[str] = Field(None, description="Source of the query (manual, automated, etc.)")
    should_ask_for_mcp_tool_confirmation: Optional[bool] = Field(True, description="Whether to ask for MCP tool confirmation")
    search_focus: Optional[str] = Field(None, description="Focus area for search (web, academic, news, etc.)")
    timezone: Optional[str] = Field("UTC", description="Timezone for the request")

    @field_validator('messages')
    @classmethod
    def validate_messages(cls, v):
        """Ensure at least one message and valid conversation structure"""
        if not v:
            raise ValueError("At least one message is required")

        # More flexible validation - allow any role sequence
        for msg in v:
            if msg.role == MessageRole.assistant and msg.tool_calls and not msg.content:
                # Assistant message with tool calls but no content is valid
                continue
            if msg.role == MessageRole.tool and not msg.tool_call_id:
                raise ValueError("Tool messages must have tool_call_id")
            if msg.role in [MessageRole.system, MessageRole.user, MessageRole.assistant] and not msg.content and not msg.tool_calls:
                raise ValueError(f"{msg.role} messages must have content or tool_calls")

        return v

    @field_validator('model')
    @classmethod
    def validate_model(cls, v):
        """Validate model name format"""
        if not v or not isinstance(v, str):
            raise ValueError("Model name must be a non-empty string")
        return v

    @field_validator('stop')
    @classmethod
    def validate_stop(cls, v):
        """Validate stop sequences"""
        if v is None:
            return v
        if isinstance(v, str):
            return [v]
        if isinstance(v, list):
            if len(v) > 4:
                raise ValueError("Maximum 4 stop sequences allowed")
            return v
        raise ValueError("Stop must be string or list of strings")

    @field_validator('tools')
    @classmethod
    def validate_tools(cls, v):
        """Validate tools if provided"""
        if v is None:
            return v
        if len(v) > 128:
            raise ValueError("Maximum 128 tools allowed")
        return v

# /v1/completions endpoint (generation, continue_chat=false)
@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    print(f"\n=== COMPLETIONS REQUEST ===")
    print(f"Model: {request.model}")
    print(f"Prompt: '{request.prompt}'")
    print(f"Max tokens: {request.max_tokens}")
    print(f"Temperature: {request.temperature}")
    print(f"Profile: {request.profile}")
    print(f"Prompt source: {request.prompt_source}")
    print(f"Query source: {request.query_source}")
    print(f"Should ask for MCP tool confirmation: {request.should_ask_for_mcp_tool_confirmation}")
    print(f"Search focus: {request.search_focus}")
    print(f"Timezone: {request.timezone}")
    print(f"========================\n")

    mode, model_preference = parse_model(request.model)
    query = request.prompt

    print(f"Parsed - Mode: '{mode}', Model Preference: '{model_preference}'")
    print(f"Final Query sent to Perplexity: '{query}'\n")

    answer = await call_perplexity(query=query, mode=mode, model_preference=model_preference, continue_chat=False,
                                  profile=request.profile, prompt_source=request.prompt_source,
                                  query_source=request.query_source,
                                  should_ask_for_mcp_tool_confirmation=request.should_ask_for_mcp_tool_confirmation,
                                  search_focus=request.search_focus, timezone=request.timezone)



    # Count tokens using GPT-4 encoding
    prompt_tokens = count_tokens(query)
    completion_tokens = count_tokens(answer)
    total_tokens = prompt_tokens + completion_tokens

    # Format as OpenAI completions response
    return {
        "id": f"cmpl-{int(time.time())}",
        "object": "text_completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "text": answer,
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
    }

# /v1/chat/completions endpoint (chat, continue_chat=true)
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    print(f"\n=== CHAT COMPLETIONS REQUEST ===")
    print(f"Model: {request.model}")
    print(f"Messages ({len(request.messages)}):")
    for i, msg in enumerate(request.messages):
        print(f"  [{i}] {msg.role}: '{msg.content}'")
    print(f"Max tokens: {request.max_tokens}")
    print(f"Temperature: {request.temperature}")
    print(f"Profile: {request.profile}")
    print(f"Prompt source: {request.prompt_source}")
    print(f"Query source: {request.query_source}")
    print(f"Should ask for MCP tool confirmation: {request.should_ask_for_mcp_tool_confirmation}")
    print(f"Search focus: {request.search_focus}")
    print(f"Timezone: {request.timezone}")
    print(f"==============================\n")

    mode, model_preference = parse_model(request.model)

    # Convert messages to query
    query = format_messages_as_query([msg.model_dump() for msg in request.messages])

    print(f"Parsed - Mode: '{mode}', Model Preference: '{model_preference}'")
    print(f"Final Query sent to Perplexity: '{query}'\n")

    answer = await call_perplexity(query=query, mode=mode, model_preference=model_preference, continue_chat=True,
                                  profile=request.profile, prompt_source=request.prompt_source,
                                  query_source=request.query_source,
                                  should_ask_for_mcp_tool_confirmation=request.should_ask_for_mcp_tool_confirmation,
                                  search_focus=request.search_focus, timezone=request.timezone)



    # Count tokens using GPT-4 encoding
    prompt_tokens = count_tokens(query)
    completion_tokens = count_tokens(answer)
    total_tokens = prompt_tokens + completion_tokens

    # Format as OpenAI chat completions response
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
    }

# Optional: Add /api/tags endpoint to handle those 404 requests
@app.get("/api/tags")
async def get_tags():
    """Dummy endpoint to handle requests from tools expecting Ollama-style API"""
    return {
        "models": [
            {"name": "pro-sonar", "model": "pro-sonar", "size": 0},
            {"name": "pro-claude37sonnetthinking", "model": "pro-claude37sonnetthinking", "size": 0},
            {"name": "pro-grok4", "model": "pro-grok4", "size": 0},
            {"name": "pro-claude45sonnet", "model": "pro-claude45sonnet", "size": 0},
            {"name": "pro-claude45sonnetthinking", "model": "pro-claude45sonnetthinking", "size": 0},
            {"name": "pro-gpt5", "model": "pro-gpt5", "size": 0},
            {"name": "pro-gpt5thinking", "model": "pro-gpt5thinking", "size": 0}
        ]
    }

@app.get("/v1/models")
async def list_models():
    """OpenAI-compatible models endpoint"""
    return {
        "object": "list",
        "data": [
            {
                "id": "pro-sonar",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-sonar",
                "parent": None
            },
            {
                "id": "pro-claude37sonnetthinking",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-claude37sonnetthinking",
                "parent": None
            },
            {
                "id": "pro-grok4",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-grok4",
                "parent": None
            },
            {
                "id": "pro-claude45sonnet",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-claude45sonnet",
                "parent": None
            },
            {
                "id": "pro-claude45sonnetthinking",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-claude45sonnetthinking",
                "parent": None
            },
            {
                "id": "pro-gpt5",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-gpt5",
                "parent": None
            },
            {
                "id": "pro-gpt5thinking",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "pro-gpt5thinking",
                "parent": None
            },
            {
                "id": "deep-research",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "deep-research",
                "parent": None
            },
            {
                "id": "lab-beta",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "perplexity",
                "permission": [],
                "root": "lab-beta",
                "parent": None
            }
        ]
    }

@app.get("//v1/models")
async def list_models_double_slash():
    """OpenAI-compatible models endpoint (double-slash version)"""
    return await list_models()

@app.post("//v1/chat/completions")
async def chat_completions_double_slash(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint (double-slash version)"""
    return await chat_completions(request)

@app.get("/health")
async def health_check():
    """Health check endpoint to verify proxy and Perplexity server connectivity"""
    try:
        async with httpx.AsyncClient() as client:
            # Test connection to Perplexity server with a simple request
            response = await client.post(
                PERPLEXITY_URL,
                json={
                    "query": "test",
                    "language": DEFAULT_LANGUAGE,
                    "incognito": DEFAULT_INCOGNITO,
                    "raw_response": DEFAULT_RAW_RESPONSE,
                    "sources": DEFAULT_SOURCES
                },
                timeout=5.0
            )

            return {
                "status": "healthy",
                "proxy_server": "running",
                "perplexity_server": "connected" if response.status_code in [200, 201] else "error",
                "perplexity_status_code": response.status_code,
                "timestamp": int(time.time())
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "proxy_server": "running",
            "perplexity_server": "disconnected",
            "error": str(e),
            "timestamp": int(time.time())
        }

@app.get("/debug/config")
async def debug_config():
    """Debug endpoint to show current configuration"""
    return {
        "perplexity_url": PERPLEXITY_URL,
        "default_language": DEFAULT_LANGUAGE,
        "default_incognito": DEFAULT_INCOGNITO,
        "default_raw_response": DEFAULT_RAW_RESPONSE,
        "default_sources": DEFAULT_SOURCES,
        "server_info": {
            "title": app.title,
            "version": app.version,
            "description": app.description
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting LiteLLM-style Perplexity Proxy Server...")
    print("📡 This proxy communicates with the main Perplexity server on port 9522")
    print("🌐 LiteLLM-compatible endpoints available on port 4000")
    print("📚 API Documentation: http://localhost:4000/docs")
    uvicorn.run(app, host="0.0.0.0", port=4000)  # Run on port 4000, like LiteLLM example
