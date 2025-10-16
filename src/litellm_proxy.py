from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import json
import time
import tiktoken
from typing import List, Dict, Any, Optional

app = FastAPI(
    title="Custom LiteLLM-like Perplexity Proxy",
    description="A LiteLLM-style API proxy for Perplexity AI wrapper. Supports non-streaming /v1/completions and /v1/chat/completions endpoints. This proxy communicates with the main Perplexity server running on port 9522.",
    version="1.0.0"
)

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
        return mode, model_pref
    return "pro", model  # Default to pro mode with model as preference

# Helper to format messages as a single query (for chat/completions)
def format_messages_as_query(messages: List[Dict[str, str]]) -> str:
    formatted = []
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")
    return "\n".join(formatted)

# Helper to call Perplexity and parse the SSE response for the answer
async def call_perplexity(query: str, mode: str, model_preference: Optional[str], continue_chat: bool) -> str:
    async with httpx.AsyncClient() as client:
        form_data = {
            "query": query,
            "mode": mode,
            "model_preference": model_preference if model_preference else "",
            "incognito": str(DEFAULT_INCOGNITO).lower(),
            "continue_chat": True,
            "raw_response": str(DEFAULT_RAW_RESPONSE).lower(),
            "language": DEFAULT_LANGUAGE,
            "sources": DEFAULT_SOURCES,
        }

        files = {}

        try:
            response = await client.post(PERPLEXITY_URL, data=form_data, files=files if files else None, timeout=60.0)
            response.raise_for_status()

            full_response = response.text
            print(f"Debug - Full response: {full_response[:500]}...")

            # The response contains literal \n characters in JSON strings
            # We need to split on actual double newlines, not the \n\n text
            # First, let's replace the literal \n with actual newlines
            actual_response = full_response.replace('\\n', '\n')
            # Now normalize line endings
            normalized_response = actual_response.replace('\r\n', '\n').replace('\r', '\n')
            # Split on actual double newlines
            events = [event.strip() for event in normalized_response.split('\n\n') if event.strip()]
            print(f"Debug - Found {len(events)} events to process.")

            answer = ""
            for i, event in enumerate(events):
                print(f"Debug - Event {i}: {event[:200]}...")
                if not event.startswith("data: "):
                    continue

                data_str = event[6:].strip()
                if data_str == "[DONE]":
                    break

                try:
                    chunk = json.loads(data_str)
                    if chunk.get("type") == "chunk" and chunk.get("data", {}).get("step_type") == "FINAL":
                        print("\n>>> Debug - Found FINAL chunk.")
                        final_content = chunk.get("data", {}).get("content", {})
                        print(f"Debug - Final content type: {type(final_content)}")
                        print(f"Debug - Final content value: {final_content}")
                        
                        answer_json_str = final_content.get("answer")
                        
                        if answer_json_str and isinstance(answer_json_str, str):
                            try:
                                # The answer itself is another JSON string
                                answer_data = json.loads(answer_json_str)
                                answer = answer_data.get("answer", "")
                                if answer:
                                    print(f"Debug - Successfully extracted nested answer: '{answer}'")
                                    return answer
                            except json.JSONDecodeError:
                                # If it's not a JSON string, use it directly
                                answer = answer_json_str
                                print(f"Debug - Using direct string as answer: '{answer}'")
                                return answer
                except json.JSONDecodeError as e:
                    print(f"Debug - Error decoding JSON from event: {e}")
                    print(f"Debug - Problematic data string: {data_str}")
                    continue
            
            if not answer:
                print("\n>>> Debug - Failed to find a valid answer in any event.")
                raise ValueError("No valid answer found in the response")

            return answer

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Perplexity API error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Pydantic models for OpenAI-like requests
class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = None  # Ignored for now
    temperature: Optional[float] = None  # Ignored
    top_p: Optional[float] = None  # Ignored

class ChatCompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = None  # Ignored for now
    temperature: Optional[float] = None  # Ignored
    top_p: Optional[float] = None  # Ignored

# /v1/completions endpoint (generation, continue_chat=false)
@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    mode, model_preference = parse_model(request.model)
    query = request.prompt

    answer = await call_perplexity(query=query, mode=mode, model_preference=model_preference, continue_chat=False)

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
async def chat_completions(request: CompletionRequest):
    mode, model_preference = parse_model(request.model)
    query = request.prompt

    answer = await call_perplexity(query=query, mode=mode, model_preference=model_preference, continue_chat=True)

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

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting LiteLLM-style Perplexity Proxy Server...")
    print("📡 This proxy communicates with the main Perplexity server on port 9522")
    print("🌐 LiteLLM-compatible endpoints available on port 4000")
    print("📚 API Documentation: http://localhost:4000/docs")
    uvicorn.run(app, host="0.0.0.0", port=4000)  # Run on port 4000, like LiteLLM example