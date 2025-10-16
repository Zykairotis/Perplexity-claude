"""
Base classes and utilities for MCP tools.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ToolResponse(BaseModel):
    """Standard response format for tools."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ValidationResult(BaseModel):
    """Validation result for tool inputs."""
    is_valid: bool
    error_message: Optional[str] = None
    normalized_data: Optional[Dict[str, Any]] = None


# Constants for validation
VALID_MODELS = ["claude45sonnet", "claude45sonnetthinking", "gpt5", "gpt5thinking", "sonar"]
VALID_SOURCES = ["web", "scholar", "social"]
REQUIRED_MODE = "pro"


def validate_model(model: Optional[str]) -> ValidationResult:
    """Validate model parameter."""
    if not model:
        return ValidationResult(
            is_valid=False,
            error_message=f"Model is required. Available models: {VALID_MODELS}"
        )

    if model not in VALID_MODELS:
        return ValidationResult(
            is_valid=False,
            error_message=f"Invalid model '{model}'. Available models: {VALID_MODELS}"
        )

    return ValidationResult(is_valid=True, normalized_data={"model": model})


def validate_mode(mode: str) -> ValidationResult:
    """Validate mode parameter."""
    if mode != REQUIRED_MODE:
        return ValidationResult(
            is_valid=False,
            error_message=f"Only '{REQUIRED_MODE}' mode is supported. Please use mode='{REQUIRED_MODE}'"
        )

    return ValidationResult(is_valid=True, normalized_data={"mode": mode})


def validate_sources(sources: List[str]) -> ValidationResult:
    """Validate sources parameter."""
    if not sources:
        return ValidationResult(is_valid=True, normalized_data={"sources": ["web"]})

    # Filter valid sources
    valid_sources_lower = [s.lower() for s in VALID_SOURCES]
    filtered_sources = []

    for source in sources:
        if source.lower() in valid_sources_lower:
            filtered_sources.append(source.lower())

    if not filtered_sources:
        return ValidationResult(is_valid=True, normalized_data={"sources": ["web"]})

    return ValidationResult(is_valid=True, normalized_data={"sources": filtered_sources})


def format_response(
    data: Any,
    raw_mode: bool = False,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Format response based on raw_mode preference."""
    if raw_mode:
        response = {
            "data": data,
            "metadata": metadata or {}
        }
        return json.dumps(response, indent=2, default=str)
    else:
        # Return clean text/answer
        if isinstance(data, dict) and "answer" in data:
            return data["answer"]
        return str(data)


def create_error_response(error_message: str, raw_mode: bool = False) -> str:
    """Create standardized error response."""
    if raw_mode:
        error_data = {
            "error": error_message,
            "success": False
        }
        return json.dumps(error_data, indent=2)
    else:
        return f"Error: {error_message}"