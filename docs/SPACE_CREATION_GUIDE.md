# Perplexity Space Creation Feature Guide

## Overview

This feature allows you to programmatically create new Perplexity spaces (collections) directly from your application. Spaces can be created via the Web Interface, REST API, Python API, or MCP Server tools.

## What Gets Created

When you create a space, you get:
- **Unique UUID**: Identifier for accessing the space
- **Title & Slug**: Name and URL-friendly identifier
- **Description**: Optional detailed description
- **Instructions**: System prompt for AI behavior in this space
- **Emoji**: Visual identifier (optional)
- **Access Control**: Private (1), Team (2), or Public (3)
- **Auto-save Option**: Automatically add to spaces.json

## Methods to Create Spaces

### 1. Web Interface

**Steps:**
1. Open `http://localhost:9522`
2. Click the green "➕ Create New Space" button
3. Fill in the form:
   - **Space Name*** (required): e.g., "Trading Analysis"
   - **Description**: "A dedicated space for market analysis and trading strategies"
   - **Emoji**: "📊"
   - **Instructions**: "You are a financial analyst. Provide data-driven insights..."
   - **Auto-save**: Keep checked to save to spaces.json
4. Click "Create Space"
5. Copy the UUID from the success message

**Example:**
```
Space Name: Trading Analysis
Description: Dedicated space for analyzing market trends and trading strategies
Emoji: 📊
Instructions: You are a financial analyst assistant. Provide data-driven 
              insights on market trends, analyze trading patterns, and offer 
              investment recommendations based on available data.
Auto-save: ✓ Checked
```

### 2. REST API

**Endpoint:** `POST /api/spaces/create`

**Request Body:**
```json
{
  "title": "Trading Analysis",
  "description": "A dedicated space for market analysis and trading strategies",
  "emoji": "📊",
  "instructions": "You are a financial analyst assistant. Provide data-driven insights on market trends.",
  "access": 1,
  "auto_save": true
}
```

**Response:**
```json
{
  "success": true,
  "uuid": "ca8b447a-4d33-4936-a3e5-a9d31b789cb3",
  "title": "Trading Analysis",
  "slug": "trading-analysis-.p65LwSPR2WZoDSRMu7IxA",
  "full_response": {
    "number": 0,
    "has_next_page": false,
    "updated_datetime": "2025-10-16T19:59:40.441645",
    "uuid": "ca8b447a-4d33-4936-a3e5-a9d31b789cb3",
    "title": "Trading Analysis",
    "description": "A dedicated space for market analysis...",
    "instructions": "You are a financial analyst assistant...",
    "emoji": "📊",
    "access": 1,
    "thread_count": 0,
    "page_count": 0,
    "file_count": 0
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:9522/api/spaces/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Trading Analysis",
    "description": "Market analysis and trading strategies",
    "emoji": "📊",
    "instructions": "You are a financial analyst assistant.",
    "access": 1,
    "auto_save": true
  }'
```

### 3. Python API

**Basic Usage:**
```python
from perplexity_api import PerplexityAPI

async def create_trading_space():
    api = PerplexityAPI()
    
    result = await api.create_space(
        title="Trading Analysis",
        description="A dedicated space for market analysis and trading strategies",
        emoji="📊",
        instructions="You are a financial analyst assistant. Provide data-driven insights on market trends, analyze trading patterns, and offer investment recommendations.",
        access=1,  # 1=private, 2=team, 3=public
        auto_save=True  # Automatically save to spaces.json
    )
    
    print(f"✅ Space created: {result['uuid']}")
    print(f"   Title: {result['title']}")
    print(f"   Slug: {result['slug']}")
    
    return result

# Run it
import asyncio
asyncio.run(create_trading_space())
```

**Advanced Example with Error Handling:**
```python
from perplexity_api import PerplexityAPI, PerplexityAPIError

async def create_space_with_error_handling():
    api = PerplexityAPI()
    
    try:
        result = await api.create_space(
            title="Research Hub",
            description="Academic research and paper analysis",
            emoji="🔬",
            instructions="""You are a research assistant. Help analyze academic papers, 
            summarize findings, and identify research gaps. Provide citations and 
            maintain academic rigor.""",
            auto_save=True
        )
        
        if result.get('uuid'):
            # Space created successfully
            space_uuid = result['uuid']
            
            # Now you can immediately use it
            search_result = await api.search(
                query="Latest developments in AI",
                space=space_uuid
            )
            
            print(f"Search in new space: {search_result.answer}")
            
    except PerplexityAPIError as e:
        print(f"❌ Failed to create space: {e}")
    finally:
        await api.close()
```

### 4. MCP Server Tool

**Tool Name:** `create_perplexity_space`

**Parameters:**
- `title` (string, required): Space name
- `description` (string): Space description
- `emoji` (string): Emoji character
- `instructions` (string): System prompt
- `access` (int): Access level (1=private, 2=team, 3=public)
- `auto_save` (bool): Auto-save to spaces.json

**Example MCP Call:**
```json
{
  "tool": "create_perplexity_space",
  "arguments": {
    "title": "Coding Projects",
    "description": "Software development and code analysis workspace",
    "emoji": "💻",
    "instructions": "You are a senior software engineer. Provide code reviews, architectural guidance, and best practice recommendations.",
    "auto_save": true
  }
}
```

**List Spaces Tool:**
```json
{
  "tool": "list_perplexity_spaces",
  "arguments": {}
}
```

## Parameters Explained

### title (Required)
- **Type:** String
- **Purpose:** Name of the space
- **Example:** "Trading Analysis", "Research Hub", "Coding Projects"
- **Best Practice:** Use descriptive, concise names

### description
- **Type:** String
- **Purpose:** Detailed explanation of the space's purpose
- **Example:** "A dedicated workspace for analyzing market trends, tracking portfolio performance, and researching investment opportunities"
- **Best Practice:** Be specific about what the space will contain and how it will be used

### emoji
- **Type:** String (single emoji character)
- **Purpose:** Visual identifier for the space
- **Example:** "📊" for trading, "🔬" for research, "💻" for coding
- **Best Practice:** Choose an emoji that represents the space's purpose

### instructions
- **Type:** String
- **Purpose:** System prompt that defines AI behavior in this space
- **Example:** 
  ```
  You are a financial analyst assistant specializing in equity markets. 
  When responding to queries in this space:
  - Provide data-driven analysis
  - Reference historical patterns
  - Include risk assessments
  - Cite sources when available
  - Maintain a professional, analytical tone
  ```
- **Best Practice:** 
  - Be specific about the AI's role
  - Define expected behavior
  - Set tone and style guidelines
  - Include domain expertise requirements

### access
- **Type:** Integer
- **Values:**
  - `1` = Private (default, only you)
  - `2` = Team (shared with team members)
  - `3` = Public (visible to everyone)
- **Example:** `1` for personal spaces
- **Best Practice:** Start with private (1) unless collaboration needed

### auto_save
- **Type:** Boolean
- **Default:** False (True in MCP/Web Interface)
- **Purpose:** Automatically add space to spaces.json
- **Example:** `true`
- **Best Practice:** Enable for spaces you'll use frequently

## Use Cases & Examples

### 1. Trading & Finance Space
```python
await api.create_space(
    title="Trading Analysis",
    description="Market analysis, portfolio tracking, and investment research",
    emoji="📊",
    instructions="""You are a quantitative analyst. Analyze market data, 
    identify trends, assess risk/reward ratios, and provide evidence-based 
    investment recommendations. Use technical and fundamental analysis.""",
    auto_save=True
)
```

### 2. Academic Research Space
```python
await api.create_space(
    title="Research Hub",
    description="Academic paper analysis and literature review",
    emoji="🔬",
    instructions="""You are a research assistant. Help analyze papers, 
    summarize methodologies, identify research gaps, and suggest future 
    directions. Maintain academic rigor and provide proper citations.""",
    auto_save=True
)
```

### 3. Software Development Space
```python
await api.create_space(
    title="Code Review",
    description="Code analysis, architectural reviews, and best practices",
    emoji="💻",
    instructions="""You are a senior software architect. Review code for:
    - Design patterns and architecture
    - Performance optimization
    - Security vulnerabilities
    - Code maintainability
    - Best practices adherence
    Provide constructive feedback with examples.""",
    auto_save=True
)
```

### 4. Personal Learning Space
```python
await api.create_space(
    title="Learning Journey",
    description="Personal study notes and concept explanations",
    emoji="📚",
    instructions="""You are a patient tutor. Explain concepts clearly, 
    provide examples, break down complex topics, and adapt to the learner's 
    pace. Use analogies and visual descriptions when helpful.""",
    auto_save=True
)
```

## After Creation

### Using Your New Space

Once created, you can immediately use the space UUID:

```python
# Create space
space_result = await api.create_space(title="My Space", auto_save=True)
space_uuid = space_result['uuid']

# Use it immediately
result = await api.search(
    query="What should I know?",
    space=space_uuid  # or use the saved name if auto_save=True
)
```

### Managing Spaces

**List all spaces:**
```bash
curl http://localhost:9522/api/spaces
```

**Check spaces.json:**
```bash
cat /home/mewtwo/Zykairotis/Perplexity-claude/spaces.json
```

**Manual entry in spaces.json:**
```json
{
  "spaces": {
    "trading": "ca8b447a-4d33-4936-a3e5-a9d31b789cb3",
    "research": "d2b9558b-5e44-5047-b4f6-b0e42c890de4"
  }
}
```

## Troubleshooting

### Issue: "Authentication Required"
**Solution:** Ensure your cookies.json is up-to-date and contains valid session cookies.

### Issue: "Space Creation Failed"
**Possible Causes:**
1. Invalid cookies (expired session)
2. Network connectivity issues
3. Perplexity API changes

**Solution:** 
- Refresh cookies from browser
- Check network connection
- Verify API endpoint is accessible

### Issue: "Auto-save Failed"
**Cause:** Permissions issue with spaces.json

**Solution:**
```bash
chmod 644 /home/mewtwo/Zykairotis/Perplexity-claude/spaces.json
```

## Best Practices

1. **Meaningful Names**: Use descriptive titles that reflect the space's purpose
2. **Detailed Instructions**: Provide clear system prompts for consistent AI behavior
3. **Organization**: Create separate spaces for different topics/projects
4. **Auto-save**: Enable for frequently used spaces
5. **Documentation**: Keep notes on what each space contains
6. **Regular Updates**: Refresh instructions as your needs evolve

## API Reference

### Endpoint: `/api/spaces/create`
- **Method:** POST
- **Content-Type:** application/json
- **Authentication:** Cookies from cookies.json
- **Rate Limit:** Standard Perplexity API limits

### Endpoint: `/api/spaces`
- **Method:** GET
- **Returns:** List of configured spaces from spaces.json

## Integration Examples

### With Existing Workflows
```python
# Create space for a new project
project_space = await api.create_space(
    title=f"Project: {project_name}",
    description=f"Dedicated space for {project_name}",
    instructions=custom_instructions,
    auto_save=True
)

# Upload project docs (future feature)
# Add team members (future feature)
# Start querying within context
```

### Automated Space Creation
```python
# Create spaces from a config file
spaces_config = [
    {"title": "Trading", "emoji": "📊", "instructions": trading_prompt},
    {"title": "Research", "emoji": "🔬", "instructions": research_prompt},
    {"title": "Coding", "emoji": "💻", "instructions": coding_prompt}
]

for config in spaces_config:
    await api.create_space(**config, auto_save=True)
```

## Security Considerations

1. **Private by Default**: Spaces are created as private (access=1)
2. **Instructions Storage**: System prompts are stored on Perplexity servers
3. **UUID Security**: UUIDs are cryptographically random
4. **Cookie Security**: Keep cookies.json secure and private

## Future Enhancements

Planned features:
- Space deletion API
- Space update/modification
- File upload to spaces
- Team member management
- Space templates
- Bulk operations
- Export/import functionality
