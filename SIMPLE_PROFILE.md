# Simple Profile - No Query Enhancement

## Overview

The **"simple"** profile is a special profile that passes your query directly to Perplexity AI **without any additional prompt enhancement or instructions**.

## Why Use Simple Profile?

Use the simple profile when:
- ✅ Your query is already perfectly crafted
- ✅ You don't want any additional context or instructions
- ✅ You want the raw Perplexity AI behavior
- ✅ You're testing query variations
- ✅ You want maximum control over the exact prompt

## Comparison

### Without Profile (Empty String)
```python
query = "What is Docker?"
# Sent as-is to Perplexity
```

### With "research" Profile
```python
query = "What is Docker?"
# Enhanced to: "What is Docker?. do a detailed research on this and provide me with most recent information about this be very detailed about it also make sure u are reffering to multiple sources like this"
```

### With "simple" Profile
```python
query = "What is Docker?"
# Sent as-is: "What is Docker?" (no enhancement)
```

## Usage

### MCP Tool
```json
{
  "tool": "search_perplexity",
  "arguments": {
    "query": "What is Docker?",
    "mode": "pro",
    "model": "claude45sonnet",
    "profile": "simple"  // ← Uses query as-is
  }
}
```

### REST API
```bash
curl -X POST http://localhost:9522/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Docker?",
    "mode": "pro",
    "profile": "simple"
  }'
```

### Python API
```python
from perplexity_api import PerplexityAPI

api = PerplexityAPI()
result = await api.search(
    query="What is Docker?",
    mode="pro",
    profile="simple"
)
```

### Web Interface
1. Open http://localhost:9522
2. Enter your query
3. Select "⚡ Simple (No Enhancement)" from Profile dropdown
4. Search!

## Behavior

**Input Query:**
```
"Explain quantum computing"
```

**With simple profile:**
```
Sent to Perplexity: "Explain quantum computing"
(No additional text added)
```

**With research profile:**
```
Sent to Perplexity: "Explain quantum computing. do a detailed research on this and provide me with most recent information about this be very detailed about it also make sure u are reffering to multiple sources like this"
```

## When to Use Each

| Profile | When to Use |
|---------|------------|
| `simple` | Query is already perfect, want raw AI behavior |
| No profile (empty) | Default behavior, let system decide |
| `research` | Want comprehensive, multi-source research |
| `code_analysis` | Analyzing code, need technical depth |
| `troubleshooting` | Step-by-step problem solving |
| Others | Specific domain expertise needed |

## Code Implementation

In `perplexity_profiles.py`:

```python
class SearchProfile(Enum):
    SIMPLE = "simple"  # Added first in the list
    RESEARCH = "research"
    # ... other profiles

PROFILE_INSTRUCTIONS = {
    SearchProfile.SIMPLE: "",  # Empty string = no enhancement
    SearchProfile.RESEARCH: "do a detailed research...",
    # ... other instructions
}
```

The `apply_profile_to_query()` function checks if instruction is empty:
- If empty: Returns original query unchanged
- If not empty: Appends instruction to query

## Testing

### Test 1: Verify Profile Exists
```bash
curl http://localhost:9522/api/profiles | jq '.profiles.simple'
```
**Expected:** `""` (empty string)

### Test 2: Test Query Enhancement
```python
from perplexity_profiles import apply_profile_to_query, validate_profile

original = "What is Docker?"
simple_profile = validate_profile("simple")
enhanced = apply_profile_to_query(original, simple_profile)

assert original == enhanced  # Should be True
print("✅ Simple profile doesn't modify query")
```

### Test 3: MCP Tool Test
```json
{
  "tool": "search_perplexity",
  "arguments": {
    "query": "Test query",
    "mode": "pro",
    "model": "sonar",
    "profile": "simple"
  }
}
```
**Expected:** Query sent to Perplexity without modification

## Available Profiles (Complete List)

1. **simple** - ⚡ No enhancement (NEW!)
2. research - 🔬 Detailed multi-source research
3. code_analysis - 💻 Code review and analysis
4. troubleshooting - 🔧 Step-by-step problem solving
5. documentation - 📚 Comprehensive docs
6. architecture - 🏗️ Design patterns and scalability
7. security - 🔒 Security assessment
8. performance - ⚡ Performance optimization
9. tutorial - 📖 Step-by-step learning
10. comparison - ⚖️ Alternative comparisons
11. trending - 📈 Latest developments
12. best_practices - ✨ Industry standards
13. integration - 🔗 System integration
14. debugging - 🐛 Debugging techniques
15. optimization - 🎯 Specific improvements

## Notes

- The "simple" profile is functionally equivalent to no profile when it comes to query enhancement
- However, it's explicit: you're stating you want simple, unenhanced behavior
- Useful for A/B testing different profile effects
- Good for when you've already crafted a complex, multi-part query

## Summary

✅ **"simple" profile added successfully**  
✅ Query passes through unchanged  
✅ Available in all interfaces (MCP, REST, Web, Python)  
✅ Containers rebuilt and running  
✅ Ready to use!
