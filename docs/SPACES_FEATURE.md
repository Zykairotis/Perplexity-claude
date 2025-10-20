# Perplexity Spaces Feature

## Overview

This feature allows you to access specific Perplexity AI "spaces" - collections of chats, historical documents, and links that you've organized in your Perplexity web interface. By specifying a space, your queries will have access to that specific collection's context.

## What is a Space?

A Perplexity Space is a collection that can contain:
- Historical chat conversations
- Uploaded documents
- Web links and references
- Custom knowledge base items

Each space has a unique UUID identifier that you can use to target queries to that specific collection.

## Setup

### 1. Get Your Space UUID

To find your space UUID:
1. Open Perplexity in your browser
2. Navigate to the space you want to use
3. Open browser DevTools (F12)
4. Go to the Network tab
5. Perform a search in that space
6. Look for the `perplexity_ask` request
7. In the request payload, find the `target_collection_uuid` field
8. Copy the UUID (format: `ca8b447a-4d33-4936-a3e5-a9d31b789cb3`)

### 2. Add Space to Configuration

Edit the `spaces.json` file in the project root:

```json
{
  "spaces": {
    "trading": "ca8b447a-4d33-4936-a3e5-a9d31b789cb3",
    "research": "d2b9558b-5e44-5047-b4f6-b0e42c890de4",
    "coding": "e3c0669c-6f55-6158-c5g7-c1f53d901ef5"
  }
}
```

- **Key**: Friendly name you want to use (e.g., "trading")
- **Value**: The UUID from Perplexity

## Usage

### Web Interface

1. Open the web interface at `http://localhost:9522`
2. Select a space from the "Space" dropdown
3. Enter your query
4. The search will be performed within the context of that space

### REST API

```bash
# Using space name (resolved from spaces.json)
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest trends?",
    "mode": "auto",
    "space": "trading"
  }'

# Using direct UUID
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest trends?",
    "mode": "auto",
    "space": "ca8b447a-4d33-4936-a3e5-a9d31b789cb3"
  }'
```

### Python API

```python
from perplexity_api import PerplexityAPI

# Initialize API
api = PerplexityAPI()

# Search with space name
result = await api.search(
    query="What are the latest trends?",
    mode="auto",
    space="trading"  # Uses the UUID mapped in spaces.json
)

# Search with direct UUID
result = await api.search(
    query="What are the latest trends?",
    mode="auto",
    space="ca8b447a-4d33-4936-a3e5-a9d31b789cb3"
)

print(result.answer)
```

### Streaming API

```python
# Stream with space
async for chunk in api.search_stream(
    query="Analyze recent market data",
    mode="pro",
    space="trading"
):
    if chunk.step_type == "FINAL":
        print(chunk.content)
```

## How It Works

1. **Space Resolution**: When you provide a space parameter:
   - If it's a valid UUID format, it's used directly
   - Otherwise, it's looked up in `spaces.json`
   - The resolved UUID is added to the API payload as `target_collection_uuid`

2. **API Integration**: The UUID is passed to Perplexity's API in the request:
   ```json
   {
     "params": {
       "target_collection_uuid": "ca8b447a-4d33-4936-a3e5-a9d31b789cb3",
       ...
     }
   }
   ```

3. **Context Access**: Perplexity uses this UUID to:
   - Access the specific space's content
   - Include relevant documents and history
   - Provide more contextualized responses

## Examples

### Trading Analysis with Space Context
```python
# Your trading space contains historical market data and analysis
result = await api.search(
    query="Compare today's trends with last week",
    mode="pro",
    model="claude45sonnet",
    space="trading"
)
```

### Research with Specific Papers
```python
# Your research space contains specific academic papers
result = await api.search(
    query="Summarize the methodology from the papers",
    mode="deep research",
    space="research"
)
```

### Coding Project Context
```python
# Your coding space contains your project documentation
result = await api.search(
    query="What's our authentication flow?",
    mode="pro",
    space="coding"
)
```

## Benefits

1. **Contextualized Responses**: Queries have access to your curated collection
2. **Organized Knowledge**: Different spaces for different topics
3. **Privacy**: Keep different types of information in separate spaces
4. **Efficiency**: No need to re-upload documents for each query

## Notes

- The space parameter is optional - omit it for regular searches
- Invalid or missing space names will be ignored (falls back to default)
- You can use either friendly names (from spaces.json) or direct UUIDs
- Multiple users can share the same spaces.json configuration

## Troubleshooting

**Space not found warning:**
```
⚠️ Could not resolve space: my_space
```
Solution: Check that the space name exists in spaces.json

**Space not working:**
1. Verify the UUID is correct
2. Ensure you have access to that space in your Perplexity account
3. Check that your cookies are valid and up-to-date

## Future Enhancements

Potential future features:
- Automatic space discovery
- Multi-space queries
- Space management API
- Dynamic space creation
