"""
Spaces resource provider for Perplexity MCP server.

Provides access to configured spaces and space management information.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


async def get_configured_spaces() -> Dict:
    """
    Get all configured Perplexity spaces from spaces.json.
    
    Returns:
        Dictionary containing:
        - spaces: Dict of space name -> UUID mappings
        - count: Number of configured spaces
        - last_updated: Timestamp of last update
    """
    try:
        from perplexity_api import load_spaces_mapping
        
        spaces = load_spaces_mapping()
        
        return {
            "spaces": spaces,
            "count": len(spaces),
            "last_updated": datetime.now().isoformat(),
            "format": "name -> UUID mappings"
        }
    except Exception as e:
        logger.error(f"Error loading configured spaces: {e}")
        return {
            "spaces": {},
            "count": 0,
            "error": str(e)
        }


async def get_space_info(space_identifier: str) -> Dict:
    """
    Get information about a specific space by name or UUID.
    
    Args:
        space_identifier: Space name or UUID
    
    Returns:
        Dictionary with space information
    """
    try:
        from perplexity_api import load_spaces_mapping, resolve_space_to_uuid
        
        # Try to resolve the identifier
        uuid = resolve_space_to_uuid(space_identifier)
        
        if not uuid:
            return {
                "found": False,
                "identifier": space_identifier,
                "error": "Space not found in configuration"
            }
        
        # Get all spaces to find the name
        spaces = load_spaces_mapping()
        space_name = None
        for name, space_uuid in spaces.items():
            if space_uuid == uuid:
                space_name = name
                break
        
        return {
            "found": True,
            "identifier": space_identifier,
            "name": space_name,
            "uuid": uuid,
            "type": "configured"
        }
        
    except Exception as e:
        logger.error(f"Error getting space info for {space_identifier}: {e}")
        return {
            "found": False,
            "identifier": space_identifier,
            "error": str(e)
        }


async def get_spaces_summary() -> Dict:
    """
    Get a summary of all configured spaces with usage statistics.
    
    Returns:
        Dictionary with spaces summary and metadata
    """
    try:
        spaces_data = await get_configured_spaces()
        
        # Build summary
        spaces_list = []
        for name, uuid in spaces_data.get("spaces", {}).items():
            spaces_list.append({
                "name": name,
                "uuid": uuid,
                "configured": True
            })
        
        return {
            "total_spaces": spaces_data.get("count", 0),
            "spaces": spaces_list,
            "last_updated": spaces_data.get("last_updated"),
            "capabilities": [
                "Search within space context",
                "Access historical conversations",
                "Use uploaded documents",
                "Reference web links"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting spaces summary: {e}")
        return {
            "total_spaces": 0,
            "spaces": [],
            "error": str(e)
        }
