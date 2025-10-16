"""
Prompt manager for handling prompt templates and dynamic generation.
"""

import logging
from typing import Dict, Optional, Any
import json

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages prompt templates and dynamic prompt generation."""

    def __init__(self):
        self.templates = {}
        self.load_default_templates()

    def load_default_templates(self):
        """Load default prompt templates."""
        self.templates = {
            "search": {
                "research": "do a detailed research on this and provide me with most recent information about this be very detailed about it also make sure u are reffering to multiple sources like this",
                "code_analysis": "analyze this code in detail, explain the logic, identify potential issues, suggest improvements, and provide best practices for this type of implementation",
                "troubleshooting": "help me troubleshoot this issue step by step, identify common causes, provide solutions, and include preventative measures for similar problems",
                "documentation": "provide comprehensive documentation for this, including setup instructions, usage examples, and best practices",
                "architecture": "analyze the architectural aspects of this, discuss design patterns, scalability considerations, and structural improvements",
                "security": "evaluate the security implications of this, identify potential vulnerabilities, and recommend security best practices",
                "performance": "analyze the performance characteristics of this, identify bottlenecks, and suggest optimization strategies",
                "tutorial": "create a step-by-step tutorial for this, with clear examples and explanations for each step",
                "comparison": "provide a detailed comparison of different approaches to this, including pros and cons and recommendations",
                "trending": "provide information about current trends and latest developments related to this topic",
                "best_practices": "explain industry best practices for this, including standards and guidelines",
                "integration": "provide guidance on how to integrate this with other systems, including compatibility considerations",
                "debugging": "help debug this issue systematically, using appropriate debugging tools and techniques",
                "optimization": "provide specific optimization recommendations for this, with measurable improvements"
            },
            "analysis": {
                "code_review": "perform a comprehensive code review, focusing on correctness, maintainability, performance, and security",
                "security_audit": "conduct a security audit of this code, identifying vulnerabilities and security risks",
                "performance_analysis": "analyze the performance characteristics and identify optimization opportunities",
                "documentation_review": "review this documentation for clarity, completeness, and accuracy"
            },
            "chat": {
                "technical_qa": "provide a detailed technical explanation for this question",
                "explanation": "explain this concept in a clear and understandable way",
                "guidance": "provide step-by-step guidance for this process or task"
            }
        }

    def get_template(self, category: str, template_name: str, **kwargs) -> str:
        """
        Get a prompt template with variable substitution.

        Args:
            category: Template category (search, analysis, chat)
            template_name: Name of the template
            **kwargs: Variables to substitute in the template

        Returns:
            Formatted prompt string
        """
        try:
            if category not in self.templates:
                logger.warning(f"Unknown template category: {category}")
                return ""

            if template_name not in self.templates[category]:
                logger.warning(f"Unknown template: {template_name} in category: {category}")
                return ""

            template = self.templates[category][template_name]

            # Format template with provided variables
            try:
                return template.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing template variable: {e}")
                return template

        except Exception as e:
            logger.error(f"Error getting template: {e}")
            return ""

    def add_template(self, category: str, template_name: str, template: str):
        """
        Add a new prompt template.

        Args:
            category: Template category
            template_name: Name of the template
            template: Template string
        """
        if category not in self.templates:
            self.templates[category] = {}

        self.templates[category][template_name] = template
        logger.info(f"Added template: {category}.{template_name}")

    def list_templates(self, category: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        List available templates.

        Args:
            category: Optional category to filter by

        Returns:
            Dictionary of available templates
        """
        if category:
            return {category: self.templates.get(category, {})}
        return self.templates

    def enhance_query(self, query: str, profile: str) -> str:
        """
        Enhance a query with profile-specific instructions.

        Args:
            query: Original query
            profile: Profile name for enhancement

        Returns:
            Enhanced query string
        """
        try:
            enhancement = self.get_template("search", profile)
            if enhancement:
                return f"{query}. {enhancement}"
            return query

        except Exception as e:
            logger.error(f"Error enhancing query: {e}")
            return query


# Global prompt manager instance
_prompt_manager = None


def get_prompt_manager() -> PromptManager:
    """Get the global prompt manager instance."""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager