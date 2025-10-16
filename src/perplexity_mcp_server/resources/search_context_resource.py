"""Search context resource provider for dynamic search session information."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict, Any, Optional
from utils.perplexity_client import get_perplexity_api
from config.settings import load_config


async def get_search_context(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get current search context and session information."""
    try:
        config = load_config()

        # Get recent search activity if session_id is provided
        search_history = []
        active_searches = []

        if session_id:
            # In a real implementation, this would fetch from a session store
            search_history = [
                {
                    "query": "React hooks optimization",
                    "profile": "code_analysis",
                    "timestamp": "2025-01-15T10:30:00Z",
                    "result_count": 15
                }
            ]
            active_searches = [
                {
                    "query": "microservices architecture patterns",
                    "profile": "architecture",
                    "status": "in_progress",
                    "progress": 65
                }
            ]

        return {
            "session_id": session_id or "default",
            "config": {
                "default_model": "claude45sonnet",
                "default_mode": "pro",
                "timeout": config.perplexity_timeout,
                "available_profiles": [
                    "research", "code_analysis", "troubleshooting", "documentation",
                    "architecture", "security", "performance", "tutorial", "comparison",
                    "trending", "best_practices", "integration", "debugging", "optimization"
                ]
            },
            "search_history": search_history,
            "active_searches": active_searches,
            "search_suggestions": [
                {
                    "topic": "AI and Machine Learning",
                    "suggested_queries": [
                        "latest developments in large language models",
                        "machine learning optimization techniques 2025",
                        "AI ethics and responsible implementation"
                    ]
                },
                {
                    "topic": "Software Development",
                    "suggested_queries": [
                        "best practices for API design",
                        "container orchestration with Kubernetes",
                        "modern testing strategies for microservices"
                    ]
                }
            ],
            "performance_metrics": {
                "average_response_time": "2.3s",
                "success_rate": 98.5,
                "queries_per_hour": 45,
                "most_used_profiles": ["research", "code_analysis", "troubleshooting"]
            }
        }
    except Exception as e:
        return {
            "error": f"Failed to get search context: {str(e)}",
            "session_id": session_id or "default"
        }


async def get_search_analytics(timeframe: str = "24h") -> Dict[str, Any]:
    """Get search analytics and usage statistics."""
    try:
        # Mock analytics data - in real implementation, this would query a database
        analytics = {
            "timeframe": timeframe,
            "total_searches": 1247,
            "unique_queries": 892,
            "average_results_per_search": 12.4,
            "profile_usage": {
                "research": 324,
                "code_analysis": 287,
                "troubleshooting": 198,
                "architecture": 156,
                "security": 98,
                "performance": 87,
                "tutorial": 76,
                "comparison": 65,
                "documentation": 54,
                "trending": 43,
                "best_practices": 32,
                "integration": 21,
                "debugging": 18,
                "optimization": 15
            },
            "model_usage": {
                "claude45sonnet": 567,
                "claude45sonnetthinking": 234,
                "gpt5": 198,
                "gpt5thinking": 145,
                "sonar": 103
            },
            "response_times": {
                "average": "2.1s",
                "p50": "1.8s",
                "p95": "3.2s",
                "p99": "4.1s"
            },
            "error_rate": 0.8,
            "satisfaction_score": 4.6,
            "top_search_topics": [
                {"topic": "machine learning", "count": 89},
                {"topic": "react development", "count": 76},
                {"topic": "api design", "count": 65},
                {"topic": "database optimization", "count": 54},
                {"topic": "security best practices", "count": 43}
            ]
        }

        return analytics
    except Exception as e:
        return {
            "error": f"Failed to get search analytics: {str(e)}",
            "timeframe": timeframe
        }


async def get_trending_queries(limit: int = 10) -> Dict[str, Any]:
    """Get currently trending search queries."""
    try:
        # Mock trending data - in real implementation, this would track actual trends
        trending_queries = [
            {
                "query": "AI agent development frameworks 2025",
                "count": 156,
                "growth": "+45%",
                "category": "artificial_intelligence"
            },
            {
                "query": "Rust programming patterns",
                "count": 142,
                "growth": "+38%",
                "category": "programming"
            },
            {
                "query": "WebAssembly performance optimization",
                "count": 128,
                "growth": "+32%",
                "category": "web_development"
            },
            {
                "query": "Kubernetes cost optimization",
                "count": 115,
                "growth": "+28%",
                "category": "devops"
            },
            {
                "query": "GraphQL vs REST best practices",
                "count": 98,
                "growth": "+25%",
                "category": "api_design"
            },
            {
                "query": "Machine learning observability",
                "count": 87,
                "growth": "+22%",
                "category": "mlops"
            },
            {
                "query": "TypeScript advanced patterns",
                "count": 76,
                "growth": "+20%",
                "category": "programming"
            },
            {
                "query": "Cloud security compliance",
                "count": 69,
                "growth": "+18%",
                "category": "security"
            },
            {
                "query": "Event-driven architecture patterns",
                "count": 58,
                "growth": "+15%",
                "category": "architecture"
            },
            {
                "query": "LLM prompt engineering techniques",
                "count": 52,
                "growth": "+12%",
                "category": "artificial_intelligence"
            }
        ][:limit]

        categories = list(set(query["category"] for query in trending_queries))

        return {
            "trending_queries": trending_queries,
            "categories": categories,
            "total_queries": sum(query["count"] for query in trending_queries),
            "average_growth": sum(float(query["growth"].rstrip('%')) for query in trending_queries) / len(trending_queries),
            "last_updated": "2025-01-15T12:00:00Z"
        }
    except Exception as e:
        return {
            "error": f"Failed to get trending queries: {str(e)}",
            "limit": limit
        }