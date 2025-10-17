"""
Space/Collection Management Tools for Perplexity MCP Server.

Provides tools for creating and managing Perplexity spaces (collections).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Optional
import logging

from utils.perplexity_client import get_perplexity_api


logger = logging.getLogger(__name__)


async def create_perplexity_space(
    title: str,
    description: str = "",
    emoji: str = "",
    instructions: str = "",
    access: int = 1,
    auto_save: bool = True
) -> dict:
    """
    Create a new Perplexity space/collection.

    A Perplexity space is a dedicated collection that can contain:
    - Historical chat conversations
    - Uploaded documents and files
    - Web links and references
    - Custom knowledge base items

    Args:
        title: Name of the space (required)
        description: Detailed description of the space's purpose and content
        emoji: Emoji character to represent the space (optional)
        instructions: System prompt/instructions for the AI agent when operating in this space.
                     This defines how the agent should behave and respond within the space context.
        access: Access level (1 = private, 2 = team, 3 = public) - default is 1 (private)
        auto_save: If True, automatically save the space UUID to spaces.json for easy reference

    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - uuid: Unique identifier for the created space
        - title: Space name
        - slug: URL-friendly identifier
        - full_response: Complete API response with all space details

    Example:
        # Create a trading analysis space
        result = await create_perplexity_space(
            title="Trading Analysis",
            description="A dedicated space for analyzing market trends, stock performance, and trading strategies",
            emoji="📊",
            instructions="You are a financial analyst assistant. Provide data-driven insights on market trends, analyze trading patterns, and offer investment recommendations based on the documents and conversations in this space.",
            auto_save=True
        )
        # Returns: {'success': True, 'uuid': 'ca8b447a-4d33-4936-a3e5-a9d31b789cb3', ...}
    """
    logger.info(f"Creating new Perplexity space: {title}")
    
    try:
        api_manager = get_perplexity_api()
        api = await api_manager.get_client()
        
        result = await api.create_space(
            title=title,
            description=description,
            emoji=emoji,
            instructions=instructions,
            access=access,
            auto_save=auto_save
        )
        
        logger.info(f"Successfully created space: {title} (UUID: {result.get('uuid')})")
        
        return {
            "success": True,
            "uuid": result.get('uuid'),
            "title": result.get('title'),
            "slug": result.get('slug'),
            "description": result.get('description'),
            "instructions": result.get('instructions'),
            "emoji": result.get('emoji'),
            "access": result.get('access'),
            "thread_count": result.get('thread_count', 0),
            "page_count": result.get('page_count', 0),
            "file_count": result.get('file_count', 0),
            "owner": result.get('owner_user', {}).get('username'),
            "auto_saved": auto_save,
            "full_response": result
        }
        
    except Exception as e:
        logger.error(f"Failed to create space '{title}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "title": title
        }


async def list_perplexity_spaces() -> dict:
    """
    List all configured Perplexity spaces from spaces.json.

    Returns:
        Dictionary containing:
        - spaces: Dict of space name -> UUID mappings
        - count: Number of configured spaces

    Example:
        result = await list_perplexity_spaces()
        # Returns: {'spaces': {'trading': 'ca8b447a-...', 'research': 'd2b9558b-...'}, 'count': 2}
    """
    logger.info("Listing configured Perplexity spaces")
    
    try:
        # Import here to avoid circular dependencies
        import sys
        import os
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from perplexity_api import load_spaces_mapping
        
        spaces = load_spaces_mapping()
        
        return {
            "success": True,
            "spaces": spaces,
            "count": len(spaces)
        }
        
    except Exception as e:
        logger.error(f"Failed to list spaces: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "spaces": {},
            "count": 0
        }
