"""
Space Creation Wizard Prompt for Perplexity MCP Server.

Provides a guided workflow for creating well-structured Perplexity spaces.
"""

from mcp.types import Prompt, PromptMessage, TextContent


async def space_creation_wizard(
    space_type: str = "general",
    auto_fill: bool = False
) -> Prompt:
    """
    Interactive wizard for creating a new Perplexity space.
    
    This prompt helps users create a well-structured space by guiding them through
    defining the purpose, instructions, and configuration.
    
    Args:
        space_type: Type of space to create (general, research, coding, trading, etc.)
        auto_fill: Whether to auto-fill suggestions based on space_type
    
    Returns:
        Prompt with guided space creation workflow
    """
    
    # Space type templates
    templates = {
        "general": {
            "emoji": "📁",
            "description_template": "A general-purpose space for {purpose}",
            "instructions_template": "You are a helpful assistant in this space."
        },
        "research": {
            "emoji": "🔬",
            "description_template": "Academic research and analysis focused on {purpose}",
            "instructions_template": "You are a research assistant. Analyze papers, summarize methodologies, identify research gaps, and provide academic citations."
        },
        "coding": {
            "emoji": "💻",
            "description_template": "Software development and code analysis for {purpose}",
            "instructions_template": "You are a senior software engineer. Provide code reviews, architectural guidance, debugging help, and best practice recommendations."
        },
        "trading": {
            "emoji": "📊",
            "description_template": "Financial analysis and trading strategies for {purpose}",
            "instructions_template": "You are a financial analyst. Provide data-driven insights on market trends, analyze trading patterns, and offer investment recommendations based on available data."
        },
        "learning": {
            "emoji": "📚",
            "description_template": "Educational content and learning resources about {purpose}",
            "instructions_template": "You are a patient tutor. Explain concepts clearly, provide examples, break down complex topics, and adapt to the learner's pace."
        }
    }
    
    template = templates.get(space_type, templates["general"])
    
    messages = [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"""# 🎯 Perplexity Space Creation Wizard

Let's create a new Perplexity space! I'll guide you through the process.

## Space Type: {space_type.title()}

{f"**Auto-fill enabled**: I'll suggest values based on the '{space_type}' template." if auto_fill else ""}

---

### Step 1: Basic Information

**Space Name** (required):
What should we call this space? Examples:
- For {space_type}: "{space_type.title()} Hub", "My {space_type.title()} Space"
- Be descriptive and concise

Please provide the space name: ________

---

### Step 2: Description

**Description** (recommended):
{template['description_template'].format(purpose="[your specific focus]")}

Describe what this space will contain and its purpose.
Examples for {space_type}:
- "A dedicated workspace for analyzing {space_type} trends and tracking progress"
- "Collection of {space_type} resources, conversations, and reference materials"

Please provide the description: ________

---

### Step 3: Visual Identifier

**Emoji** (optional):
{f"Suggested: {template['emoji']}" if auto_fill else "Choose an emoji that represents this space"}

Examples: 📊 💻 🔬 📚 🎯 🌟 💡 📁

Please provide the emoji (or press enter to skip): ________

---

### Step 4: AI Instructions (System Prompt)

**Instructions** (very important):
This defines how the AI should behave when operating in this space.

{f"Suggested for {space_type}:" if auto_fill else "Define the AI's role and behavior:"}

```
{template['instructions_template']}
```

Guidelines for writing good instructions:
1. Define the AI's role (e.g., "You are a...")
2. Specify the domain expertise
3. List key responsibilities
4. Set tone and style
5. Include any specific constraints

Please provide the instructions: ________

---

### Step 5: Configuration

**Access Level**:
1 = Private (only you)
2 = Team (shared with team)
3 = Public (visible to everyone)

Recommended: 1 (Private)

Please select access level (1/2/3): ________

**Auto-save to spaces.json**:
Should this space be automatically added to your configuration file for easy reference?

Recommended: Yes

Auto-save? (yes/no): ________

---

## Next Steps

After you provide the information above, I will:
1. ✅ Create the space using the Perplexity API
2. ✅ Return the unique UUID
3. ✅ Optionally save to spaces.json
4. ✅ Show you how to use it

## Example Responses

For a trading space:

```json
{{
  "title": "Trading Analysis Hub",
  "description": "A dedicated space for analyzing market trends, tracking portfolio performance, and researching investment opportunities",
  "emoji": "📊",
  "instructions": "You are a financial analyst assistant specializing in equity markets. Provide data-driven insights on market trends, analyze trading patterns with technical and fundamental analysis, and offer evidence-based investment recommendations. Always include risk assessments and cite sources when available.",
  "access": 1,
  "auto_save": true
}}
```

---

**Ready to proceed?** Please provide the requested information, and I'll create your space!

Alternatively, you can use the MCP tool directly:
```
create_perplexity_space(
    title="Your Space Name",
    description="Detailed description",
    emoji="📊",
    instructions="System prompt here",
    access=1,
    auto_save=True
)
```
"""
            )
        )
    ]
    
    return Prompt(
        name="space_creation_wizard",
        description=f"Interactive wizard for creating a {space_type} Perplexity space",
        arguments=[
            {
                "name": "space_type",
                "description": "Type of space to create (general, research, coding, trading, learning)",
                "required": False
            },
            {
                "name": "auto_fill",
                "description": "Whether to auto-fill suggestions based on space type",
                "required": False
            }
        ],
        messages=messages
    )
