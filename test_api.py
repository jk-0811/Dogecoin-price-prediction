"""
API Testing Script for Dogecoin Price Prediction
Run this script to test the prediction API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_model_info():
    """Test the model info endpoint"""
    print_section("TEST 1: Get Model Info")
    
    try:
        response = requests.get(f"{BASE_URL}/api/model-info/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Model Type: {data.get('model_type')}")
            print(f"✓ Trained: {data.get('trained')}")
            print(f"✓ Features: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Connection Error: {str(e)}")
        return False

def test_prediction(test_name, data):
    """Test the prediction endpoint"""
    print(f"\n  Test Case: {test_name}")
    print(f"  Input: {json.dumps(data, indent=4)}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/predict/", json=data)
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                price = result.get('predicted_price', 0)
                print(f"  ✓ Predicted Price: ${price:.6f}")
                print(f"  ✓ Timestamp: {result.get('timestamp')}")
                return True
            else:
                print(f"  ✗ Error: {result.get('error')}")
                return False
        else:
            print(f"  ✗ HTTP Error: {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Request Error: {str(e)}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("\n" + "█"*60)
    print("  DOGECOIN PRICE PREDICTION - API TEST SUITE")
    print("█"*60)
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Server: {BASE_URL}")
    
    results = []
    
    # Test 1: Model Info
    results.append(("Model Info", test_model_info()))
    
    # Test 2: Predictions with different scenarios
    print_section("TEST 2: Price Predictions")
    
    # Bullish scenario
    bullish_data = {
        "open": 0.150,
        "high": 0.160,
        "low": 0.145,
        "volume": 1250000000,
        "ma5": 0.152,
        "ma10": 0.151,
        "daily_return": 0.025,
        "volatility": 0.015
    }
    results.append(("Bullish Scenario", test_prediction("Bullish Market", bullish_data)))
    
    # Bearish scenario
    bearish_data = {
        "open": 0.100,
        "high": 0.105,
        "low": 0.095,
        "volume": 1000000000,
        "ma5": 0.098,
        "ma10": 0.102,
        "daily_return": -0.015,
        "volatility": 0.020
    }
    results.append(("Bearish Scenario", test_prediction("Bearish Market", bearish_data)))
    
    # High volatility scenario
    volatile_data = {
        "open": 0.200,
        "high": 0.220,
        "low": 0.180,
        "volume": 2000000000,
        "ma5": 0.200,
        "ma10": 0.195,
        "daily_return": 0.050,
        "volatility": 0.040
    }
    results.append(("High Volatility", test_prediction("High Volatility Market", volatile_data)))
    
    # Print Summary
    print_section("TEST SUMMARY")
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    failed_tests = total_tests - passed_tests
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n" + "█"*60)
    if failed_tests == 0:
        print("  ✓ ALL TESTS PASSED!")
    else:
        print(f"  ✗ {failed_tests} TEST(S) FAILED")
    print("█"*60 + "\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user.")
    except Exception as e:
        print(f"\n\nFatal Error: {str(e)}")
