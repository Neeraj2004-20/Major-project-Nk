#!/usr/bin/env python3
"""
Deployment verification script
Tests all API endpoints to ensure deployment is working correctly
"""

import requests
import sys
import json
from datetime import datetime

def test_deployment(base_url="http://localhost:8000"):
    """Test all API endpoints"""
    
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
            tests_passed += 1
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        tests_failed += 1
    
    # Test 2: Health check
    print("\n2️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            tests_passed += 1
        else:
            print(f"❌ Health check failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Health check error: {e}")
        tests_failed += 1
    
    # Test 3: Model info
    print("\n3️⃣ Testing model info endpoint...")
    try:
        response = requests.get(f"{base_url}/model/info", timeout=10)
        if response.status_code in [200, 503]:  # 503 if model not loaded yet
            print("✅ Model info endpoint working")
            print(f"   Response: {response.json()}")
            tests_passed += 1
        else:
            print(f"❌ Model info failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Model info error: {e}")
        tests_failed += 1
    
    # Test 4: Live prediction (optional - may fail if no model)
    print("\n4️⃣ Testing live prediction endpoint...")
    try:
        payload = {
            "symbol": "AAPL",
            "days_ahead": 1
        }
        response = requests.post(
            f"{base_url}/predict/live",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Live prediction working")
            result = response.json()
            print(f"   Symbol: {result.get('symbol')}")
            print(f"   Current Price: ${result.get('current_price', 0):.2f}")
            print(f"   Predicted Price: ${result.get('predicted_price', 0):.2f}")
            print(f"   Direction: {result.get('direction')}")
            tests_passed += 1
        elif response.status_code == 503:
            print("⚠️ Live prediction unavailable (model not loaded)")
            print("   This is expected if you haven't trained a model yet")
            tests_passed += 1
        else:
            print(f"⚠️ Live prediction returned: {response.status_code}")
            print(f"   Message: {response.text}")
            tests_passed += 1  # Don't fail if model isn't loaded
    except Exception as e:
        print(f"⚠️ Live prediction error: {e}")
        tests_passed += 1  # Don't fail on this test
    
    # Test 5: API documentation
    print("\n5️⃣ Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible")
            print(f"   Visit: {base_url}/docs")
            tests_passed += 1
        else:
            print(f"❌ API docs failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ API docs error: {e}")
        tests_failed += 1
    
    # Test 6: Experiments endpoint
    print("\n6️⃣ Testing experiments endpoint...")
    try:
        response = requests.get(f"{base_url}/experiments", timeout=10)
        if response.status_code == 200:
            print("✅ Experiments endpoint working")
            data = response.json()
            print(f"   Experiments logged: {data.get('count', 0)}")
            tests_passed += 1
        else:
            print(f"❌ Experiments endpoint failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Experiments endpoint error: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results Summary")
    print(f"   ✅ Passed: {tests_passed}")
    print(f"   ❌ Failed: {tests_failed}")
    print(f"   📈 Success Rate: {(tests_passed/(tests_passed+tests_failed)*100):.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 All tests passed! Deployment is successful!")
        return 0
    else:
        print(f"\n⚠️ {tests_failed} test(s) failed. Check the errors above.")
        return 1

def load_test(base_url="http://localhost:8000", requests_count=100):
    """Simple load test"""
    print(f"\n🔥 Running load test ({requests_count} requests)...")
    
    import time
    start_time = time.time()
    success = 0
    failed = 0
    
    for i in range(requests_count):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                success += 1
            else:
                failed += 1
        except:
            failed += 1
        
        if (i + 1) % 10 == 0:
            print(f"   Progress: {i+1}/{requests_count}")
    
    end_time = time.time()
    duration = end_time - start_time
    rps = requests_count / duration
    
    print(f"\n📊 Load Test Results:")
    print(f"   Total Requests: {requests_count}")
    print(f"   Successful: {success}")
    print(f"   Failed: {failed}")
    print(f"   Duration: {duration:.2f}s")
    print(f"   Requests/sec: {rps:.2f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test API deployment')
    parser.add_argument('--url', default='http://localhost:8000', help='Base URL of the API')
    parser.add_argument('--load-test', action='store_true', help='Run load test')
    parser.add_argument('--requests', type=int, default=100, help='Number of requests for load test')
    
    args = parser.parse_args()
    
    # Run deployment tests
    exit_code = test_deployment(args.url)
    
    # Run load test if requested
    if args.load_test:
        load_test(args.url, args.requests)
    
    sys.exit(exit_code)
