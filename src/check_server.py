#!/usr/bin/env python3
"""
Simple connectivity test for Webhook MCP Server
Tests if the server is running and provides usage guidance
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

def print_header():
    """Print a nice header"""
    print("🔍 Webhook MCP Server Connectivity Test")
    print("=" * 50)
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

async def test_basic_connectivity():
    """Test basic server connectivity"""
    print("📡 Testing basic connectivity...")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Try to connect to the server
            response = await client.get("http://localhost:8000")

            if response.status_code == 404:
                print("✅ Server is responding (HTTP 404 - this is normal for MCP servers)")
                print("   The server is running but doesn't have regular HTTP endpoints")
                return True
            else:
                print(f"✅ Server is responding (HTTP {response.status_code})")
                return True

    except httpx.ConnectError:
        print("❌ Cannot connect to server on localhost:8000")
        print("   Make sure the server is running: docker compose up -d")
        return False
    except httpx.TimeoutException:
        print("❌ Server connection timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_docker_status():
    """Check Docker container status"""
    print("\n🐳 Checking Docker container status...")

    try:
        import subprocess
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=webhook-mcp", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Header + at least one container
                print("✅ Docker container found:")
                for line in lines:
                    print(f"   {line}")
            else:
                print("❌ No webhook-mcp container found")
                print("   Start with: docker compose up -d")
        else:
            print("❌ Docker command failed")

    except subprocess.TimeoutExpired:
        print("❌ Docker command timed out")
    except FileNotFoundError:
        print("⚠️  Docker not found (may not be in PATH)")
    except Exception as e:
        print(f"❌ Error checking Docker: {e}")

def show_usage_guide():
    """Show how to use the MCP server"""
    print("\n📚 How to Use the Webhook MCP Server")
    print("=" * 50)

    print("""
🎯 IMPORTANT: This is an MCP (Model Context Protocol) server, not a regular HTTP API!

You can use it in several ways:

1️⃣  WITH CLAUDE DESKTOP:
   Add to your Claude Desktop configuration file:

   {
     "mcpServers": {
       "webhook-perplexity": {
         "command": "python",
         "args": ["webhook_mcp.py"],
         "cwd": "/path/to/Perplexity-Unofficial"
       }
     }
   }

2️⃣  WITH MCP CLIENT (Python):
   ```python
   from mcp.client.stdio import stdio_client
   from mcp.client.session import ClientSession

   async with stdio_client(["python", "webhook_mcp.py"]) as (read, write):
       async with ClientSession(read, write) as session:
           await session.initialize()
           result = await session.call_tool("call_webhook", {
               "url": "https://httpbin.org/json",
               "method": "GET"
           })
   ```

3️⃣  AVAILABLE TOOLS:
   • call_webhook - Make HTTP requests to external APIs
   • analyze_with_perplexity - Analyze data using Perplexity AI
   • webhook_and_analyze - Combined webhook + analysis workflow

4️⃣  AVAILABLE RESOURCES:
   • webhook://config - Server configuration
   • webhook://stats - Usage statistics
   • webhook://health - Server health status

5️⃣  FOR TESTING:
   Run: python use_mcp_server.py (if you have the MCP client libs installed)
""")

def show_troubleshooting():
    """Show troubleshooting tips"""
    print("\n🔧 Troubleshooting")
    print("=" * 30)

    print("""
If you're having issues:

🐳 Container Issues:
   • Check status: docker ps | grep webhook
   • View logs: docker logs perplexity-unofficial-webhook-mcp-1
   • Restart: docker compose restart webhook-mcp

🔌 Connection Issues:
   • Make sure port 8000 is not blocked
   • Try: telnet localhost 8000
   • Check firewall settings

📚 Usage Issues:
   • This is NOT a REST API - use MCP protocol
   • Install MCP client: pip install mcp fastmcp
   • See examples in use_mcp_server.py

🔍 More Help:
   • Read MCP_SERVER_SUMMARY.md
   • Check FastMCP documentation
   • MCP specification: https://modelcontextprotocol.io/
""")

async def main():
    """Main test function"""
    print_header()

    # Test basic connectivity
    server_running = await test_basic_connectivity()

    # Check Docker status
    await test_docker_status()

    # Show results
    print("\n" + "=" * 50)
    if server_running:
        print("🎉 SERVER STATUS: RUNNING ✅")
        print("   The MCP server is accessible and ready to use!")
    else:
        print("💥 SERVER STATUS: NOT RUNNING ❌")
        print("   Please start the server first.")

    # Show usage guide
    show_usage_guide()

    # Show troubleshooting
    show_troubleshooting()

    print("\n" + "=" * 50)
    print("✨ Connectivity test completed!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
