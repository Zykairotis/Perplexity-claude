"""
Profile validation and management utilities.

Handles validation and listing of search profiles.
"""

import logging
from typing import Dict, Optional
import sys
import os

logger = logging.getLogger(__name__)

# Add the src directory to Python path for imports
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


def validate_profile(profile_name: str) -> Optional[object]:
    """
    Validate a profile name and return the profile object if valid.

    Args:
        profile_name: Name of the profile to validate

    Returns:
        Profile object if valid, None otherwise
    """
    try:
        from perplexity_profiles import SearchProfile

        # Try to get profile by name
        try:
            return SearchProfile(profile_name)
        except ValueError:
            # If not a valid profile, return None
            logger.warning(f"Invalid profile: {profile_name}")
            return None

    except ImportError as e:
        logger.error(f"Failed to import SearchProfile: {e}")
        # Fallback validation
        valid_profiles = [
            "research", "code_analysis", "troubleshooting", "documentation",
            "architecture", "security", "performance", "tutorial",
            "comparison", "trending", "best_practices", "integration",
            "debugging", "optimization"
        ]

        if profile_name in valid_profiles:
            # Return a simple profile object
            class SimpleProfile:
                def __init__(self, name):
                    self.value = name
            return SimpleProfile(profile_name)

        return None


def list_available_profiles() -> Dict[str, str]:
    """
    Get a list of all available profiles with their descriptions.

    Returns:
        Dictionary mapping profile names to descriptions
    """
    profiles = {
        "research": "Detailed research with multiple sources and comprehensive analysis",
        "code_analysis": "Code review, logic analysis, and improvement suggestions",
        "troubleshooting": "Step-by-step troubleshooting with solutions and prevention",
        "documentation": "Comprehensive documentation with examples and guidelines",
        "architecture": "Architectural analysis with design patterns and scalability",
        "security": "Security evaluation with vulnerability identification",
        "performance": "Performance analysis with optimization recommendations",
        "tutorial": "Step-by-step tutorials with examples and exercises",
        "comparison": "Detailed comparisons with pros/cons and recommendations",
        "trending": "Latest trends and emerging technologies",
        "best_practices": "Industry best practices and coding standards",
        "integration": "Integration guidance with compatibility considerations",
        "debugging": "Systematic debugging with tools and techniques",
        "optimization": "Specific optimizations with measurable improvements"
    }

    try:
        # Try to get profiles from the original module
        from perplexity_profiles import list_available_profiles as original_list_profiles
        original_profiles = original_list_profiles()

        # Merge with our profiles, preferring original descriptions
        for key, value in original_profiles.items():
            if key in profiles:
                profiles[key] = value

    except ImportError:
        logger.warning("Could not import original profile list, using fallback")

    return profiles