#!/usr/bin/env python3
"""
Simple test script for TA Worker endpoints
Replace 'YOUR_RAILWAY_URL' with your actual Railway URL
"""

import requests
import json
from datetime import datetime

# Replace with your actual Railway URL
BASE_URL = "https://ta-worker-ta-worker-ai.up.railway.app"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/v1/healthz", timeout=10)
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_ta_snapshot():
    """Test the TA snapshot endpoint"""
    try:
        params = {
            "symbol": "HYPEUSDT",
            "tfs": "15m,1h,4h,1d",
            "lookback": 300,
            "category": "spot"
        }
        response = requests.get(f"{BASE_URL}/v1/run", params=params, timeout=30)
        print(f"TA Snapshot Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Symbol: {data.get('symbol')}")
            print(f"Timestamp: {data.get('now')}")
            print(f"Timeframes: {list(data.get('features', {}).keys())}")
            
            # Show sample data for first timeframe
            if data.get('features'):
                first_tf = list(data['features'].keys())[0]
                sample = data['features'][first_tf]
                print(f"\nSample data for {first_tf}:")
                print(f"  Price: {sample.get('price')}")
                print(f"  RSI: {sample.get('rsi14')}")
                print(f"  EMA20: {sample.get('ema20')}")
                print(f"  MACD: {sample.get('macd', {}).get('val')}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"TA snapshot test failed: {e}")
        return False

def main():
    print("Testing TA Worker Endpoints")
    print("=" * 40)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint:")
    health_ok = test_health()
    
    # Test TA snapshot endpoint
    print("\n2. Testing TA Snapshot Endpoint:")
    snapshot_ok = test_ta_snapshot()
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"TA Snapshot: {'✅ PASS' if snapshot_ok else '❌ FAIL'}")
    
    if health_ok and snapshot_ok:
        print("\n🎉 All tests passed! Your TA Worker is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()
