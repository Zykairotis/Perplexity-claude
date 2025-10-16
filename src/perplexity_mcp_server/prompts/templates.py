"""
Pre-defined prompt templates for different use cases.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def get_search_template(profile: str, **kwargs) -> str:
    """
    Get search prompt template for a specific profile.

    Args:
        profile: Profile name
        **kwargs: Additional variables for template substitution

    Returns:
        Search prompt template
    """
    templates = {
        "research": "do a detailed research on {query} and provide me with most recent information about this be very detailed about it also make sure u are reffering to multiple sources like this",
        "code_analysis": "analyze {query} in detail, explain the logic, identify potential issues, suggest improvements, and provide best practices for this type of implementation",
        "troubleshooting": "help me troubleshoot {query} step by step, identify common causes, provide solutions, and include preventative measures for similar problems",
        "documentation": "provide comprehensive documentation for {query}, including setup instructions, usage examples, and best practices",
        "architecture": "analyze the architectural aspects of {query}, discuss design patterns, scalability considerations, and structural improvements",
        "security": "evaluate the security implications of {query}, identify potential vulnerabilities, and recommend security best practices",
        "performance": "analyze the performance characteristics of {query}, identify bottlenecks, and suggest optimization strategies",
        "tutorial": "create a step-by-step tutorial for {query}, with clear examples and explanations for each step",
        "comparison": "provide a detailed comparison of different approaches to {query}, including pros and cons and recommendations",
        "trending": "provide information about current trends and latest developments related to {query}",
        "best_practices": "explain industry best practices for {query}, including standards and guidelines",
        "integration": "provide guidance on how to integrate {query} with other systems, including compatibility considerations",
        "debugging": "help debug {query} systematically, using appropriate debugging tools and techniques",
        "optimization": "provide specific optimization recommendations for {query}, with measurable improvements"
    }

    template = templates.get(profile, "{query}")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        return template


def get_analysis_template(analysis_type: str, **kwargs) -> str:
    """
    Get analysis prompt template for a specific type.

    Args:
        analysis_type: Type of analysis
        **kwargs: Additional variables for template substitution

    Returns:
        Analysis prompt template
    """
    templates = {
        "code_review": "perform a comprehensive code review of {content}, focusing on correctness, maintainability, performance, and security",
        "security_audit": "conduct a security audit of {content}, identifying vulnerabilities and security risks",
        "performance_analysis": "analyze the performance characteristics of {content} and identify optimization opportunities",
        "documentation_review": "review this documentation ({content}) for clarity, completeness, and accuracy"
    }

    template = templates.get(analysis_type, "analyze {content}")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        return template


def get_chat_template(chat_type: str, **kwargs) -> str:
    """
    Get chat prompt template for a specific type.

    Args:
        chat_type: Type of chat interaction
        **kwargs: Additional variables for template substitution

    Returns:
        Chat prompt template
    """
    templates = {
        "technical_qa": "provide a detailed technical explanation for: {message}",
        "explanation": "explain {message} in a clear and understandable way",
        "guidance": "provide step-by-step guidance for: {message}"
    }

    template = templates.get(chat_type, "{message}")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        return template


def get_troubleshooting_template(issue: str, **kwargs) -> str:
    """
    Get troubleshooting prompt template.

    Args:
        issue: Description of the issue
        **kwargs: Additional variables for template substitution

    Returns:
        Troubleshooting prompt template
    """
    template = (
        "help me troubleshoot this issue: {issue}. "
        "Please provide: "
        "1. Step-by-step diagnostic process "
        "2. Common causes and symptoms "
        "3. Specific solutions and fixes "
        "4. Prevention strategies for the future "
        "5. Tools or commands that can help"
    )

    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        return template


def get_file_analysis_template(file_type: str, query: str, **kwargs) -> str:
    """
    Get file analysis prompt template.

    Args:
        file_type: Type of file being analyzed
        query: Analysis request
        **kwargs: Additional variables for template substitution

    Returns:
        File analysis prompt template
    """
    template = (
        "File Type: {file_type}\n"
        "Analysis Request: {query}\n\n"
        "File Content:\n"
        "{content}\n\n"
        "Please provide a comprehensive analysis of this file content based on the request."
    )

    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing template variable: {e}")
        return template