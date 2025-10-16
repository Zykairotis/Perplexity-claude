"""Search workshop prompt implementation for guided search sessions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp.server.fastmcp.prompts import base
from typing import List, Optional
from utils.perplexity_client import get_perplexity_api


async def search_workshop(query: str, profile: str = "research", context: str = "general") -> str:
    """Interactive search workshop that guides users through effective research."""

    try:
        # Get available profiles for context
        api = get_perplexity_api()
        available_profiles = ["research", "code_analysis", "troubleshooting", "documentation",
                            "architecture", "security", "performance", "tutorial", "comparison",
                            "trending", "best_practices", "integration", "debugging", "optimization"]

        if profile not in available_profiles:
            profile = "research"  # fallback to default

        prompt = f"""🔍 **Search Workshop: {query}**

Let's conduct a comprehensive search using the **{profile}** profile approach.

**📋 Current Search Configuration:**
- **Query**: {query}
- **Profile**: {profile}
- **Context**: {context}

**🎯 Profile-Specific Strategy:**
"""

        # Add profile-specific guidance
        profile_guidance = {
            "research": "Deep analysis with multiple sources and comprehensive coverage",
            "code_analysis": "Focus on code quality, logic explanation, and improvement suggestions",
            "troubleshooting": "Step-by-step problem resolution with preventative measures",
            "documentation": "Clear, structured information with practical examples",
            "architecture": "System design patterns, scalability, and structural considerations",
            "security": "Vulnerability assessment, security best practices, and risk analysis",
            "performance": "Bottleneck identification and optimization strategies",
            "tutorial": "Step-by-step learning with practical exercises",
            "comparison": "Detailed feature analysis with pros/cons and recommendations",
            "trending": "Latest developments and emerging technology insights",
            "best_practices": "Industry standards and professional guidelines",
            "integration": "Compatibility considerations and implementation guidance",
            "debugging": "Systematic issue identification and resolution techniques",
            "optimization": "Performance improvements with measurable results"
        }

        prompt += f"{profile_guidance.get(profile, profile_guidance['research'])}\n\n"

        # Suggest search refinement strategies
        prompt += "**🔧 Search Enhancement Suggestions:**\n"

        if len(query.split()) < 3:
            prompt += "• Consider adding more specific keywords to narrow results\n"
        if "?" not in query and "how" not in query.lower():
            prompt += "• Try phrasing as a question for more targeted answers\n"
        if "vs" not in query.lower() and "compare" not in query.lower():
            prompt += f"• For {profile} analysis, consider comparison terms for deeper insights\n"

        prompt += f"""
**🚀 Recommended Next Steps:**
1. **Execute Search**: Use `search_perplexity` with your optimized query
2. **Analyze Results**: Review sources and identify key insights
3. **Follow-up**: Use `chat_with_perplexity` for deeper exploration
4. **Document**: Save important findings for reference

**💡 Pro Tips for {profile} Searches:**
"""

        # Add profile-specific tips
        if profile == "research":
            prompt += "- Look for recent publications and authoritative sources\n- Cross-reference information across multiple sources\n- Note publication dates for relevance\n- Identify key experts in the field"
        elif profile == "code_analysis":
            prompt += "- Focus on actual code examples and implementations\n- Look for performance benchmarks\n- Consider edge cases and error handling\n- Check for recent API changes"
        elif profile == "troubleshooting":
            prompt += "- Search for specific error messages\n- Include version numbers and environment details\n- Look for official documentation and GitHub issues\n- Consider multiple solution approaches"
        elif profile == "security":
            prompt += "- Prioritize official security advisories\n- Look for CVEs and security bulletins\n- Check for recent patch releases\n- Verify source credibility carefully"
        else:
            prompt += "- Include relevant technical terms and frameworks\n- Consider your specific use case context\n- Look for recent developments in the field\n- Verify information currency"

        prompt += f"""

**🎯 Suggested Search Query:**
Based on your input, consider this optimized version:
`{query} {profile_guidance.get(profile, '').split('.')[0].lower()}`

Ready to proceed with your search? Use the search tools to begin your research journey!
"""

        return prompt

    except Exception as e:
        return f"Error generating search workshop prompt: {str(e)}"