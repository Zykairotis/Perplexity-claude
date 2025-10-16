#!/usr/bin/env python3
"""
Example usage script for the Webhook MCP Server

This script demonstrates how to use the webhook MCP server tools
in various scenarios.
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webhook_mcp import (
    call_webhook, 
    analyze_with_perplexity, 
    webhook_and_analyze,
    get_webhook_config,
    get_webhook_stats
)

async def example_1_simple_webhook_call():
    """Example 1: Simple webhook call to httpbin.org"""
    print("\n=== Example 1: Simple Webhook Call ===")
    
    try:
        result = await call_webhook(
            url="https://httpbin.org/post",
            method="POST",
            body={"message": "Hello from Webhook MCP!", "timestamp": "2023-01-01T00:00:00Z"}
        )
        
        print(f"Status Code: {result['status_code']}")
        print(f"Response Time: {result['response_time']:.2f}s")
        print(f"Response Body: {json.dumps(result['body'], indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

async def example_2_authenticated_webhook():
    """Example 2: Webhook call with authentication"""
    print("\n=== Example 2: Authenticated Webhook Call ===")
    
    try:
        # Using httpbin.org's bearer token endpoint for testing
        result = await call_webhook(
            url="https://httpbin.org/bearer",
            method="GET",
            auth_type="bearer",
            auth_credentials={"token": "test-token-123"}
        )
        
        print(f"Status Code: {result['status_code']}")
        print(f"Response Body: {json.dumps(result['body'], indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

async def example_3_perplexity_analysis():
    """Example 3: Analyze data with Perplexity"""
    print("\n=== Example 3: Perplexity Analysis ===")
    
    try:
        # Sample API response data
        api_response = {
            "user_id": "12345",
            "action": "file_upload",
            "file_size": 2048576,  # 2MB
            "file_type": "pdf",
            "timestamp": "2023-01-01T12:00:00Z",
            "status": "success"
        }
        
        result = await analyze_with_perplexity(
            response_data=api_response,
            analysis_query="Analyze this file upload event for security and performance implications",
            perplexity_mode="detailed",
            sources=["web", "academic"]
        )
        
        print(f"Analysis: {result['analysis']}")
        print(f"Follow-up Questions: {result['follow_up_questions']}")
        print(f"Related Topics: {result['related_topics']}")
        print(f"Sources Used: {result['sources_used']}")
        
    except Exception as e:
        print(f"Error: {e}")

async def example_4_complete_workflow():
    """Example 4: Complete webhook and analysis workflow"""
    print("\n=== Example 4: Complete Workflow ===")
    
    try:
        # Simulate calling a user analytics API
        result = await webhook_and_analyze(
            url="https://httpbin.org/post",
            method="POST",
            body={
                "event": "user_login",
                "user_id": "user_123",
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "timestamp": "2023-01-01T12:00:00Z",
                "success": True
            },
            analysis_query="Analyze this login event for security concerns and user behavior patterns",
            perplexity_mode="detailed",
            sources=["web", "academic"]
        )
        
        # Webhook response
        webhook_response = result["webhook_response"]
        print(f"Webhook Status: {webhook_response['status_code']}")
        print(f"Webhook Response Time: {webhook_response['response_time']:.2f}s")
        
        # Perplexity analysis
        analysis = result["perplexity_analysis"]
        print(f"\nAI Analysis: {analysis['analysis']}")
        print(f"\nFollow-up Questions:")
        for i, question in enumerate(analysis['follow_up_questions'], 1):
            print(f"  {i}. {question}")
        
        print(f"\nRelated Topics:")
        for topic in analysis['related_topics']:
            print(f"  - {topic}")
        
        print(f"\nTimestamp: {result['timestamp']}")
        
    except Exception as e:
        print(f"Error: {e}")

async def example_5_error_handling():
    """Example 5: Error handling demonstration"""
    print("\n=== Example 5: Error Handling ===")
    
    try:
        # This should fail with an invalid URL
        result = await call_webhook(
            url="https://invalid-domain-that-does-not-exist.com/api",
            method="GET",
            timeout=5
        )
        
        if result['error']:
            print(f"Expected error occurred: {result['error']}")
            print(f"Status Code: {result['status_code']}")
        else:
            print("Unexpected success")
            
    except Exception as e:
        print(f"Exception caught: {e}")

async def example_6_configuration_and_stats():
    """Example 6: Configuration and statistics"""
    print("\n=== Example 6: Configuration and Statistics ===")
    
    try:
        # Get configuration
        config = await get_webhook_config()
        print("Current Configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        # Get statistics
        stats = await get_webhook_stats()
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")

async def example_7_real_world_scenario():
    """Example 7: Real-world scenario - API monitoring"""
    print("\n=== Example 7: Real-world Scenario - API Monitoring ===")
    
    try:
        # Simulate monitoring an external API
        api_endpoints = [
            "https://httpbin.org/status/200",  # Success
            "https://httpbin.org/status/500",  # Server error
            "https://httpbin.org/delay/2",     # Slow response
        ]
        
        for endpoint in api_endpoints:
            print(f"\nChecking endpoint: {endpoint}")
            
            result = await webhook_and_analyze(
                url=endpoint,
                method="GET",
                analysis_query=f"Analyze this API response from {endpoint} for issues and recommendations",
                perplexity_mode="concise"
            )
            
            webhook_response = result["webhook_response"]
            analysis = result["perplexity_analysis"]
            
            print(f"  Status: {webhook_response['status_code']}")
            print(f"  Response Time: {webhook_response['response_time']:.2f}s")
            print(f"  Analysis: {analysis['analysis'][:100]}...")
            
            # Small delay between requests
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Error: {e}")

async def main():
    """Run all examples"""
    print("Webhook MCP Server - Usage Examples")
    print("=" * 50)
    
    # Run all examples
    await example_1_simple_webhook_call()
    await example_2_authenticated_webhook()
    await example_3_perplexity_analysis()
    await example_4_complete_workflow()
    await example_5_error_handling()
    await example_6_configuration_and_stats()
    await example_7_real_world_scenario()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("\nTo run these examples with your own APIs:")
    print("1. Replace the URLs with your actual webhook endpoints")
    print("2. Add proper authentication credentials")
    print("3. Customize the analysis queries for your use case")
    print("4. Adjust configuration parameters as needed")

if __name__ == "__main__":
    # Set up environment for examples
    os.environ["WEBHOOK_DEFAULT_TIMEOUT"] = "10"
    os.environ["WEBHOOK_MAX_RETRIES"] = "2"
    os.environ["PERPLEXITY_TIMEOUT"] = "30"
    
    # Run examples
    asyncio.run(main())