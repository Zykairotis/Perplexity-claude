"""
Perplexity Search Profiles
Specialized profiles for enhancing search effectiveness for coding and tech-related work
"""

from typing import Dict, Optional
from enum import Enum

class SearchProfile(Enum):
    """Available search profiles for different use cases"""
    RESEARCH = "research"
    CODE_ANALYSIS = "code_analysis"
    TROUBLESHOOTING = "troubleshooting"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TUTORIAL = "tutorial"
    COMPARISON = "comparison"
    TRENDING = "trending"
    BEST_PRACTICES = "best_practices"
    INTEGRATION = "integration"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"

# Profile definitions with specific instructions
PROFILE_INSTRUCTIONS = {
    SearchProfile.RESEARCH: "do a detailed research on this and provide me with most recent information about this be very detailed about it also make sure u are reffering to multiple sources like this",

    SearchProfile.CODE_ANALYSIS: "analyze this code in detail, explain the logic, identify potential issues, suggest improvements, and provide best practices for this type of implementation",

    SearchProfile.TROUBLESHOOTING: "help me troubleshoot this issue step by step, identify common causes, provide solutions, and include preventative measures for similar problems",

    SearchProfile.DOCUMENTATION: "provide comprehensive documentation for this, including setup instructions, usage examples, configuration options, and maintenance guidelines",

    SearchProfile.ARCHITECTURE: "analyze the architectural implications, discuss design patterns, scalability considerations, and provide architectural recommendations",

    SearchProfile.SECURITY: "evaluate security implications, identify vulnerabilities, suggest security measures, and provide security best practices for this context",

    SearchProfile.PERFORMANCE: "analyze performance characteristics, identify bottlenecks, suggest optimizations, and provide performance benchmarks and monitoring strategies",

    SearchProfile.TUTORIAL: "create a step-by-step tutorial with clear explanations, code examples, common pitfalls, and practice exercises",

    SearchProfile.COMPARISON: "provide detailed comparisons between alternatives, including pros and cons, use cases, and recommendations for different scenarios",

    SearchProfile.TRENDING: "focus on the latest trends, recent developments, emerging technologies, and current best practices in this area",

    SearchProfile.BEST_PRACTICES: "provide industry best practices, coding standards, guidelines, and recommendations for professional implementation",

    SearchProfile.INTEGRATION: "explain how to integrate this with existing systems, compatibility considerations, API requirements, and integration patterns",

    SearchProfile.DEBUGGING: "provide systematic debugging approach, common debugging techniques, tools, and methods to identify and fix issues",

    SearchProfile.OPTIMIZATION: "suggest specific optimizations, performance tuning strategies, resource usage improvements, and measurable enhancement techniques"
}

def get_profile_instruction(profile: SearchProfile) -> str:
    """Get the instruction string for a specific profile"""
    return PROFILE_INSTRUCTIONS.get(profile, "")

def apply_profile_to_query(query: str, profile: Optional[SearchProfile]) -> str:
    """
    Apply profile-specific instructions to enhance the search query

    Args:
        query: Original search query
        profile: Profile to apply (optional)

    Returns:
        Enhanced query with profile-specific instructions
    """
    if profile is None:
        return query

    profile_instruction = get_profile_instruction(profile)
    if not profile_instruction:
        return query

    # Combine original query with profile-specific instruction
    enhanced_query = f"{query}. {profile_instruction}"
    return enhanced_query

def list_available_profiles() -> Dict[str, str]:
    """Get a list of all available profiles with their descriptions"""
    return {
        profile.value: instruction[:100] + "..." if len(instruction) > 100 else instruction
        for profile, instruction in PROFILE_INSTRUCTIONS.items()
    }

def validate_profile(profile_name: str) -> Optional[SearchProfile]:
    """Validate and convert profile name to SearchProfile enum"""
    try:
        return SearchProfile(profile_name.lower())
    except ValueError:
        return None