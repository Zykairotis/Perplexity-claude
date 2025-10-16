"""
Server settings and configuration management.
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pathlib import Path


class ServerConfig(BaseModel):
    """Main server configuration."""

    # Server settings
    name: str = Field(default="perplexity", description="Server name")
    version: str = Field(default="1.0.0", description="Server version")
    log_level: str = Field(default="INFO", description="Logging level")

    # Perplexity API settings
    perplexity_timeout: int = Field(default=120, description="Perplexity API timeout in seconds")
    default_mode: str = Field(default="pro", description="Default search mode")
    default_sources: list[str] = Field(default=["web"], description="Default search sources")

    # Validation settings
    required_model: bool = Field(default=True, description="Whether model parameter is required")
    required_profile: bool = Field(default=True, description="Whether profile parameter is required")

    # Performance settings
    max_results_default: int = Field(default=5, description="Default max results")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Max file size in bytes (10MB)")

    class Config:
        env_prefix = "PERPLEXITY_MCP_"
        case_sensitive = False


def load_config(config_path: Optional[Path] = None) -> ServerConfig:
    """
    Load configuration from environment variables and optional config file.

    Args:
        config_path: Optional path to configuration file

    Returns:
        ServerConfig instance
    """
    # Load from environment variables
    config_data = {}

    # Override with config file if provided
    if config_path and config_path.exists():
        import json
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            config_data.update(file_config)

    return ServerConfig(**config_data)


def get_default_config() -> ServerConfig:
    """Get default configuration."""
    return ServerConfig()