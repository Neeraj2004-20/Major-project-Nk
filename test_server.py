"""
Test Server Startup
Validates all components are working correctly
"""

import requests
import time
import sys
from typing import Dict, Any
import json


def print_section(title: str):
    """Print formatted section title"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def test_endpoint(name: str, url: str, method: str = "GET", timeout: int = 5) -> bool:
    """Test an endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        else:
            response = requests.post(url, timeout=timeout)
        
        status = "✓" if response.status_code < 400 else "✗"
        print(f"{status} {name}: {response.status_code}")
        return response.status_code < 400
    except requests.exceptions.ConnectionError:
        print(f"✗ {name}: Connection failed (server not running)")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ {name}: Request timeout")
        return False
    except Exception as e:
        print(f"✗ {name}: {type(e).__name__}: {str(e)}")
        return False


def test_health(base_url: str) -> bool:
    """Test health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Uptime: {data.get('uptime_formatted', 'unknown')}")
            return True
    except:
        pass
    return False


def test_metrics(base_url: str) -> bool:
    """Test metrics endpoint"""
    try:
        response = requests.get(f"{base_url}/metrics", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Total Requests: {data.get('performance', {}).get('total_requests', 0)}")
            return True
    except:
        pass
    return False


def main():
    """Run all tests"""
    base_url = "http://localhost:5501"
    
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 AI MARKET PREDICTOR - SERVER VALIDATION  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Wait for server
    print("\n⏳ Waiting for server to be ready...")
    for i in range(30):
        try:
            requests.get(f"{base_url}/health", timeout=2)
            print("✓ Server is responding\n")
            break
        except:
            time.sleep(1)
            if i == 29:
                print("\n❌ Server failed to start")
                return False
    
    # Test endpoints
    print_section("System Endpoints")
    results = []
    results.append(test_endpoint("Health Check", f"{base_url}/health"))
    results.append(test_endpoint("Metrics", f"{base_url}/metrics"))
    results.append(test_endpoint("Status", f"{base_url}/api/status"))
    
    print_section("Documentation")
    results.append(test_endpoint("Swagger Docs", f"{base_url}/docs"))
    results.append(test_endpoint("ReDoc", f"{base_url}/redoc"))
    
    print_section("Web Interface")
    results.append(test_endpoint("Home Page", f"{base_url}/"))
    
    # Detailed info
    print_section("System Information")
    test_health(base_url)
    test_metrics(base_url)
    
    # Summary
    print_section("Test Summary")
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! Server is ready for production.\n")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check logs for details.\n")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
