"""
Perplexity API client management.

Handles API client creation, caching, and session management.
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


class PerplexityClientManager:
    """Manages Perplexity API client instances."""

    def __init__(self):
        self._client = None
        self._cookies = None

    def load_cookies_from_env(self) -> Dict[str, str]:
        """Load cookies from JSON file path specified in environment."""
        cookies = {}

        # Try multiple possible paths for cookies.json
        possible_paths = [
            "cookies.json",  # Current directory
            "/app/cookies.json",  # Docker container path
            "../cookies.json",  # Parent directory
            "../../cookies.json",  # Project root
            "/home/mewtwo/Zykairotis/Perplexity-claude/cookies.json",  # Original path
        ]

        for cookie_path in possible_paths:
            try:
                import json
                with open(cookie_path, 'r') as f:
                    cookie_data = json.load(f)
                    cookies = cookie_data.get('cookies', {})
                    if cookies:
                        logger.info(f"✅ Loaded {len(cookies)} cookies from {cookie_path}")
                        self._cookies = cookies
                        return cookies
                    else:
                        logger.warning(f"⚠️ No cookies found in {cookie_path}")
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                continue

        logger.warning(f"⚠️ Could not load cookies from any of the attempted paths: {possible_paths}")
        return {}

    async def get_client(self):
        """Get or create the Perplexity API client."""
        if self._client is None:
            # Import from the original codebase
            try:
                from perplexity_api import PerplexityAPI
                cookies = self.load_cookies_from_env()
                self._client = PerplexityAPI(cookies)
            except ImportError as e:
                logger.error(f"Failed to import PerplexityAPI: {e}")
                raise RuntimeError("Could not import PerplexityAPI from src directory")

        return self._client

    async def close(self):
        """Close the client session."""
        if self._client and hasattr(self._client, 'close'):
            await self._client.close()
        self._client = None


# Global client manager instance
_client_manager = PerplexityClientManager()


def get_perplexity_api():
    """Get the Perplexity API client instance."""
    return _client_manager