#!/usr/bin/env python3
"""
Run all tests for both Perplexity API modules
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test(script_name):
    """Run a single test script and return success status"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {script_name}")
    print('='*60)

    try:
        result = subprocess.run([sys.executable, script_name],
                              capture_output=True, text=True, timeout=300)

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")

        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
            return True
        else:
            print(f"❌ {script_name} failed with exit code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏰ {script_name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"💥 Error running {script_name}: {e}")
        return False

def main():
    """Run all test scripts"""
    print("🚀 Starting Perplexity API test suite...")

    # Change to the test directory
    test_dir = Path(__file__).parent
    os.chdir(test_dir)

    # List of test scripts to run
    test_scripts = [
        "test_perplexity_api.py",
        "test_perplexity_fixed.py"
    ]

    results = []

    for script in test_scripts:
        if os.path.exists(script):
            success = run_test(script)
            results.append((script, success))
        else:
            print(f"❌ Test script not found: {script}")
            results.append((script, False))

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for script, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {script}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()