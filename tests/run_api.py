"""
Test Script for Perplexity API
Run this script to test the perplexity_api.py module

Usage:
    python tests/run_api.py [options]
    
Examples:
    # Basic test
    python tests/run_api.py
    
    # Test with custom query
    python tests/run_api.py --query "What is quantum computing?"
    
    # Test streaming
    python tests/run_api.py --streaming
    
    # Test all modes
    python tests/run_api.py --test-all
"""

import sys
import os
import asyncio
import argparse
import json
from typing import Optional, Dict

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from perplexity_api import (
    PerplexityAPI, 
    SearchMode, 
    ProModel, 
    ReasoningModel,
    SearchSource,
    SearchProfile,
    PerplexityAPIError
)


class PerplexityAPITester:
    """Test runner for Perplexity API"""
    
    def __init__(self, cookies: Optional[Dict[str, str]] = None, verbose: bool = True):
        """
        Initialize the tester
        
        Args:
            cookies: Optional cookies for authentication
            verbose: Enable verbose output
        """
        self.api = PerplexityAPI(cookies)
        self.verbose = verbose
        self.test_results = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose is enabled"""
        if self.verbose:
            prefix = {
                "INFO": "ℹ️ ",
                "SUCCESS": "✅",
                "ERROR": "❌",
                "WARN": "⚠️ "
            }.get(level, "  ")
            print(f"{prefix} {message}")
    
    async def test_basic_search(self, query: str = "What is artificial intelligence?"):
        """Test basic search functionality"""
        self.log("Testing basic search...", "INFO")
        try:
            result = await self.api.search(query, mode=SearchMode.AUTO)
            
            self.log(f"Query: {result.query}", "SUCCESS")
            self.log(f"Answer length: {len(result.answer)} chars", "SUCCESS")
            self.log(f"Number of sources: {len(result.sources)}", "SUCCESS")
            self.log(f"Mode: {result.mode}", "SUCCESS")
            
            if self.verbose:
                print("\n" + "="*80)
                print("ANSWER:")
                print("="*80)
                print(result.answer[:500] + "..." if len(result.answer) > 500 else result.answer)
                print("="*80 + "\n")
            
            self.test_results.append(("Basic Search", True, None))
            return result
            
        except Exception as e:
            self.log(f"Basic search failed: {str(e)}", "ERROR")
            self.test_results.append(("Basic Search", False, str(e)))
            return None
    
    async def test_pro_search(self, query: str = "Explain quantum computing"):
        """Test Pro mode search with specific model"""
        self.log("Testing Pro search with model...", "INFO")
        try:
            result = await self.api.search(
                query,
                mode=SearchMode.PRO,
                model=ProModel.SONAR
            )
            
            self.log(f"Query: {result.query}", "SUCCESS")
            self.log(f"Mode: {result.mode}", "SUCCESS")
            self.log(f"Model: {result.model}", "SUCCESS")
            self.log(f"Answer length: {len(result.answer)} chars", "SUCCESS")
            
            self.test_results.append(("Pro Search", True, None))
            return result
            
        except Exception as e:
            self.log(f"Pro search failed: {str(e)}", "ERROR")
            self.test_results.append(("Pro Search", False, str(e)))
            return None
    
    async def test_streaming_search(self, query: str = "Latest developments in AI"):
        """Test streaming search"""
        self.log("Testing streaming search...", "INFO")
        try:
            chunk_count = 0
            final_answer = None
            
            async for chunk in self.api.search_stream(query, mode=SearchMode.AUTO):
                chunk_count += 1
                
                if chunk.step_type == "SEARCH_WEB":
                    self.log(f"🔍 Searching web...", "INFO")
                elif chunk.step_type == "SEARCH_RESULTS":
                    results = chunk.content.get('web_results', [])
                    self.log(f"📄 Found {len(results)} sources", "INFO")
                elif chunk.step_type == "FINAL":
                    self.log("✅ Search completed", "SUCCESS")
                    final_answer = chunk.content.get('answer')
                
                if self.verbose and chunk_count <= 5:
                    print(f"  Chunk {chunk_count}: {chunk.step_type}")
            
            self.log(f"Received {chunk_count} chunks", "SUCCESS")
            self.test_results.append(("Streaming Search", True, None))
            return True
            
        except Exception as e:
            self.log(f"Streaming search failed: {str(e)}", "ERROR")
            self.test_results.append(("Streaming Search", False, str(e)))
            return None
    
    async def test_with_profile(self, query: str = "How to implement a REST API?"):
        """Test search with profile enhancement"""
        self.log("Testing search with code_analysis profile...", "INFO")
        try:
            result = await self.api.search(
                query,
                mode=SearchMode.PRO,
                model=ProModel.CLAUDE_45_SONNET,
                profile=SearchProfile.CODE_ANALYSIS
            )
            
            self.log(f"Query: {result.query}", "SUCCESS")
            self.log(f"Profile enhanced search completed", "SUCCESS")
            self.log(f"Answer length: {len(result.answer)} chars", "SUCCESS")
            
            self.test_results.append(("Profile Search", True, None))
            return result
            
        except Exception as e:
            self.log(f"Profile search failed: {str(e)}", "ERROR")
            self.test_results.append(("Profile Search", False, str(e)))
            return None
    
    async def test_different_sources(self, query: str = "Machine learning research papers"):
        """Test search with different sources"""
        self.log("Testing search with scholar source...", "INFO")
        try:
            result = await self.api.search(
                query,
                mode=SearchMode.AUTO,
                sources=[SearchSource.SCHOLAR, SearchSource.WEB]
            )
            
            self.log(f"Query: {result.query}", "SUCCESS")
            self.log(f"Sources used: scholar, web", "SUCCESS")
            self.log(f"Number of sources: {len(result.sources)}", "SUCCESS")
            
            self.test_results.append(("Different Sources", True, None))
            return result
            
        except Exception as e:
            self.log(f"Different sources search failed: {str(e)}", "ERROR")
            self.test_results.append(("Different Sources", False, str(e)))
            return None
    
    async def test_session_info(self):
        """Test getting session information"""
        self.log("Testing session info...", "INFO")
        try:
            info = await self.api.get_session_info()
            
            self.log("Session info retrieved:", "SUCCESS")
            if self.verbose:
                print(json.dumps(info, indent=2))
            
            self.test_results.append(("Session Info", True, None))
            return info
            
        except Exception as e:
            self.log(f"Session info failed: {str(e)}", "ERROR")
            self.test_results.append(("Session Info", False, str(e)))
            return None
    
    async def test_raw_response(self, query: str = "What is Python?"):
        """Test getting raw API response"""
        self.log("Testing raw response...", "INFO")
        try:
            response = await self.api.search(query, raw_response=True)
            
            self.log("Raw response received", "SUCCESS")
            self.log(f"Response type: {type(response)}", "SUCCESS")
            
            if self.verbose and isinstance(response, dict):
                print("\nRaw response keys:", list(response.keys()))
            
            self.test_results.append(("Raw Response", True, None))
            return response
            
        except Exception as e:
            self.log(f"Raw response failed: {str(e)}", "ERROR")
            self.test_results.append(("Raw Response", False, str(e)))
            return None
    
    async def test_all(self, custom_query: Optional[str] = None):
        """Run all tests"""
        self.log("="*80, "INFO")
        self.log("STARTING COMPREHENSIVE API TESTS", "INFO")
        self.log("="*80 + "\n", "INFO")
        
        query = custom_query if custom_query else "What is artificial intelligence?"
        
        # Run all tests
        await self.test_basic_search(query)
        await asyncio.sleep(1)  # Rate limiting
        
        await self.test_pro_search()
        await asyncio.sleep(1)
        
        await self.test_streaming_search()
        await asyncio.sleep(1)
        
        await self.test_with_profile()
        await asyncio.sleep(1)
        
        await self.test_different_sources()
        await asyncio.sleep(1)
        
        await self.test_session_info()
        await asyncio.sleep(1)
        
        await self.test_raw_response()
        
        # Print summary
        self.print_summary()
    
    async def run_custom_test(self, query: str, mode: str = "auto", 
                             model: Optional[str] = None, streaming: bool = False):
        """Run a custom test with specified parameters"""
        self.log(f"Running custom test: {query}", "INFO")
        self.log(f"Mode: {mode}, Streaming: {streaming}", "INFO")
        
        try:
            if streaming:
                await self.test_streaming_search(query)
            else:
                result = await self.api.search(query, mode=mode, model=model)
                
                if self.verbose:
                    print("\n" + "="*80)
                    print("CUSTOM QUERY RESULT:")
                    print("="*80)
                    print(f"Query: {result.query}")
                    print(f"Mode: {result.mode}")
                    print(f"Model: {result.model}")
                    print(f"\nAnswer:\n{result.answer}")
                    print("\nSources:")
                    for i, source in enumerate(result.sources[:5], 1):
                        print(f"  {i}. {source.get('name', 'N/A')} - {source.get('url', 'N/A')}")
                    print("="*80 + "\n")
        
        except Exception as e:
            self.log(f"Custom test failed: {str(e)}", "ERROR")
    
    def print_summary(self):
        """Print test results summary"""
        self.log("\n" + "="*80, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("="*80, "INFO")
        
        total = len(self.test_results)
        passed = sum(1 for _, success, _ in self.test_results if success)
        failed = total - passed
        
        for test_name, success, error in self.test_results:
            status = "PASS" if success else "FAIL"
            level = "SUCCESS" if success else "ERROR"
            self.log(f"{test_name}: {status}", level)
            if error and self.verbose:
                print(f"    Error: {error}")
        
        self.log("\n" + "="*80, "INFO")
        self.log(f"Total Tests: {total}", "INFO")
        self.log(f"Passed: {passed}", "SUCCESS")
        self.log(f"Failed: {failed}", "ERROR" if failed > 0 else "INFO")
        self.log("="*80 + "\n", "INFO")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.api.close()


async def main():
    """Main entry point for the test script"""
    parser = argparse.ArgumentParser(description="Test Perplexity API")
    parser.add_argument("--query", "-q", type=str, help="Custom query to test")
    parser.add_argument("--mode", "-m", type=str, default="auto", 
                       choices=["auto", "pro", "reasoning", "deep research"],
                       help="Search mode")
    parser.add_argument("--model", type=str, help="Model to use (for pro/reasoning modes)")
    parser.add_argument("--streaming", "-s", action="store_true", help="Use streaming search")
    parser.add_argument("--test-all", "-a", action="store_true", help="Run all tests")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    parser.add_argument("--cookies-file", type=str, help="Path to JSON file containing cookies")
    
    args = parser.parse_args()
    
    # Load cookies if provided
    cookies = None
    if args.cookies_file:
        try:
            with open(args.cookies_file, 'r') as f:
                cookies = json.load(f)
            print(f"✅ Loaded cookies from {args.cookies_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load cookies: {e}")
    
    # Initialize tester
    tester = PerplexityAPITester(cookies=cookies, verbose=not args.quiet)
    
    try:
        if args.test_all:
            # Run all tests
            await tester.test_all(args.query)
        elif args.query:
            # Run custom test
            await tester.run_custom_test(
                query=args.query,
                mode=args.mode,
                model=args.model,
                streaming=args.streaming
            )
        else:
            # Default: run basic test
            print("\n💡 Running basic test. Use --help for more options.\n")
            await tester.test_basic_search()
            tester.print_summary()
    
    finally:
        await tester.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
