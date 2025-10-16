#!/usr/bin/env python3
"""
Working MCP Client Example for Webhook MCP Server

This script demonstrates how to properly use the Webhook MCP Server
using the FastMCP client library.
"""

import asyncio
import json
from typing import Dict, Any
from fastmcp import FastMCP
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

async def demonstrate_webhook_mcp():
    """Demonstrate how to use the Webhook MCP Server"""

    print("🚀 Webhook MCP Server Usage Example")
    print("=" * 50)

    # Option 1: Connect to streamable-http server
    try:
        print("\n📡 Connecting to MCP server...")

        # Connect using SSE client (more reliable than streamable-http for now)
        async with sse_client('http://localhost:8000/sse') as (read, write):
            async with ClientSession(read, write) as session:

                # Initialize the session
                print("🔧 Initializing session...")
                await session.initialize()
                print("✅ Session initialized successfully")

                # List available tools
                print("\n🛠️  Available Tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"   • {tool.name}: {tool.description}")

                # List available resources
                print("\n📁 Available Resources:")
                resources = await session.list_resources()
                for resource in resources.resources:
                    print(f"   • {resource.uri}: {resource.description}")

                # Example 1: Read webhook configuration
                print("\n⚙️  Reading webhook configuration...")
                try:
                    config_result = await session.read_resource("webhook://config")
                    print("✅ Configuration retrieved:")
                    for content in config_result.contents:
                        if hasattr(content, 'text'):
                            config_data = json.loads(content.text)
                            print(f"   Timeout: {config_data.get('default_timeout')}s")
                            print(f"   Max Retries: {config_data.get('max_retries')}")
                            print(f"   Perplexity Mode: {config_data.get('default_perplexity_mode')}")
                except Exception as e:
                    print(f"❌ Failed to read configuration: {e}")

                # Example 2: Make a simple webhook call
                print("\n🌐 Making a test webhook call...")
                try:
                    webhook_result = await session.call_tool(
                        "call_webhook",
                        {
                            "url": "https://httpbin.org/json",
                            "method": "GET",
                            "timeout": 10
                        }
                    )

                    print("✅ Webhook call successful!")
                    for content in webhook_result.content:
                        if hasattr(content, 'text'):
                            result_data = json.loads(content.text)
                            print(f"   Status: {result_data.get('status_code')}")
                            print(f"   Response Time: {result_data.get('response_time', 0):.2f}s")

                except Exception as e:
                    print(f"❌ Webhook call failed: {e}")

                # Example 3: Make a webhook call with analysis
                print("\n🧠 Making webhook call with Perplexity analysis...")
                try:
                    analysis_result = await session.call_tool(
                        "webhook_and_analyze",
                        {
                            "url": "https://httpbin.org/ip",
                            "method": "GET",
                            "timeout": 10,
                            "analysis_query": "What can you tell me about this IP address response?",
                            "perplexity_mode": "auto",
                            "sources": ["web"],
                            "profile": "research"
                        }
                    )

                    print("✅ Webhook call and analysis completed!")
                    for content in analysis_result.content:
                        if hasattr(content, 'text'):
                            result_data = json.loads(content.text)
                            webhook_data = result_data.get('webhook_response', {})
                            analysis_data = result_data.get('perplexity_analysis', {})

                            print(f"   Webhook Status: {webhook_data.get('status_code')}")
                            print(f"   Analysis: {analysis_data.get('analysis', 'No analysis available')[:100]}...")

                except Exception as e:
                    print(f"❌ Analysis call failed: {e}")

                # Example 4: Read server statistics
                print("\n📊 Reading server statistics...")
                try:
                    stats_result = await session.read_resource("webhook://stats")
                    print("✅ Statistics retrieved:")
                    for content in stats_result.contents:
                        if hasattr(content, 'text'):
                            stats_data = json.loads(content.text)
                            print(f"   Total Calls: {stats_data.get('total_calls', 0)}")
                            print(f"   Successful Calls: {stats_data.get('successful_calls', 0)}")

                except Exception as e:
                    print(f"❌ Failed to read statistics: {e}")

    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure the MCP server is running: docker compose up -d")
        print("   2. Check if port 8000 is accessible: docker ps")
        print("   3. Try the stdio version instead (see below)")

async def demonstrate_stdio_version():
    """Demonstrate using the MCP server via stdio (local)"""

    print("\n" + "=" * 50)
    print("📺 Alternative: Using STDIO Version")
    print("=" * 50)

    try:
        # Connect using stdio (local execution)
        async with stdio_client(["python", "src/webhook_mcp.py"]) as (read, write):
            async with ClientSession(read, write) as session:

                await session.initialize()
                print("✅ STDIO session initialized")

                # Make a simple call
                result = await session.call_tool(
                    "call_webhook",
                    {
                        "url": "https://httpbin.org/uuid",
                        "method": "GET"
                    }
                )

                print("✅ STDIO webhook call successful!")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(f"   Response: {content.text[:100]}...")

    except Exception as e:
        print(f"❌ STDIO version failed: {e}")

def show_integration_examples():
    """Show integration examples for different MCP clients"""

    print("\n" + "=" * 50)
    print("🔌 Integration Examples")
    print("=" * 50)

    print("""
1. Claude Desktop Integration:
   Add to your Claude Desktop config:

   {
     "mcpServers": {
       "webhook-perplexity": {
         "command": "python",
         "args": ["src/webhook_mcp.py"],
         "cwd": "/path/to/Perplexity-claude"
       }
     }
   }

2. Remote MCP Client:
   For remote access, use the streamable-http transport:

   server_url = "http://your-server:8000"
   # Use appropriate MCP client library

3. Python MCP Client:
   ```python
   from mcp.client.sse import sse_client
   from mcp.client.session import ClientSession

   async with sse_client('http://localhost:8000/sse') as (read, write):
       async with ClientSession(read, write) as session:
           await session.initialize()
           result = await session.call_tool("call_webhook", {...})
   ```

4. Available Tools:
   • call_webhook - Make HTTP requests to external APIs
   • analyze_with_perplexity - Analyze data using Perplexity AI
   • webhook_and_analyze - Combined webhook + analysis workflow
   • search_perplexity - Enhanced search with profile support
   • chat_with_perplexity - Conversational AI with context and profile support
   • analyze_file_with_perplexity - File analysis with AI and profile support

5. Available Resources:
   • webhook://config - Server configuration
   • webhook://stats - Usage statistics
   • webhook://health - Server health status
   • perplexity://models - Available models and capabilities
   • perplexity://health - Perplexity API status

6. Profile Enhancements:
   Available search profiles for enhanced queries:
   • research - Deep research with multiple sources
   • code_analysis - Code analysis with explanations
   • troubleshooting - Step-by-step troubleshooting
   • documentation - Comprehensive documentation
   • architecture - Architectural analysis
   • security - Security evaluation
   • performance - Performance analysis
   • tutorial - Step-by-step tutorials
   • comparison - Detailed comparisons
   • trending - Latest trends and developments
   • best_practices - Industry best practices
   • integration - Integration guidance
   • debugging - Systematic debugging
   • optimization - Performance optimization

7. Profile Usage Examples:
   ```python
   # Enhanced search with research profile
   result = await session.call_tool("search_perplexity", {
       "query": "latest AI developments",
       "profile": "research",
       "mode": "deep research"
   })

   # Code analysis with specialized profile
   result = await session.call_tool("analyze_file_with_perplexity", {
       "file_content": "def example(): pass",
       "file_type": "python",
       "query": "Analyze this code",
       "profile": "code_analysis"
   })

   # Chat with troubleshooting profile
   result = await session.call_tool("chat_with_perplexity", {
       "message": "My Docker container won't start",
       "profile": "troubleshooting",
       "mode": "pro"
   })
   ```
""")

async def main():
    """Main function to run all examples"""

    # Run the main demonstration
    await demonstrate_webhook_mcp()

    # Show alternative stdio version
    await demonstrate_stdio_version()

    # Show integration examples
    show_integration_examples()

    print("\n" + "=" * 50)
    print("✨ Examples completed!")
    print("\nNeed help? Check:")
    print("• MCP_SERVER_SUMMARY.md for detailed documentation")
    print("• Docker logs: docker logs perplexity-unofficial-webhook-mcp-1")
    print("• Server status: docker ps | grep webhook")

if __name__ == "__main__":
    # Install required dependencies if needed
    try:
        import mcp
        import fastmcp
    except ImportError:
        print("❌ Missing dependencies. Install with:")
        print("   pip install mcp fastmcp")
        exit(1)

    # Run the examples
    asyncio.run(main())
