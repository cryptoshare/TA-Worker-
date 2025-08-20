import time
import hmac
import hashlib
import requests
import json

def get_bybit_base_url():
    return "https://api.bybit.com"

def sign_bybit_request(secret_key: str, param_str: str) -> str:
    """Sign Bybit API request correctly"""
    signature = hmac.new(
        secret_key.encode('utf-8'),
        param_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def test_bybit_endpoints():
    api_key = "8ASH9Yxn0CJf93pRZb"
    secret_key = "GwHLhjJNcKTIwUVnhesAFN9J2jcVvcNhm0gI"
    
    # Test different endpoints
    endpoints_to_test = [
        "/v5/position/list",
        "/v5/position/list",
        "/v5/account/wallet-balance",
        "/v5/account/info",
        "/v5/position/list"
    ]
    
    for i, endpoint in enumerate(endpoints_to_test):
        print(f"\n=== Test {i+1}: {endpoint} ===")
        
        try:
            base_url = get_bybit_base_url()
            timestamp = str(int(time.time() * 1000))
            recv_window = "5000"
            
            # Different parameter sets for different endpoints
            if "position" in endpoint:
                params = {
                    "api_key": api_key,
                    "category": "linear",
                    "recv_window": recv_window,
                    "timestamp": timestamp
                }
            elif "account" in endpoint:
                params = {
                    "api_key": api_key,
                    "accountType": "UNIFIED",
                    "recv_window": recv_window,
                    "timestamp": timestamp
                }
            else:
                params = {
                    "api_key": api_key,
                    "recv_window": recv_window,
                    "timestamp": timestamp
                }
            
            # Convert params to query string for signature
            param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items()) if k != "api_key"])
            
            # Sign the request
            signature = sign_bybit_request(secret_key, param_str)
            params["sign"] = signature
            
            # Make the request
            url = f"{base_url}{endpoint}"
            headers = {"Content-Type": "application/json"}
            
            print(f"URL: {url}")
            print(f"Params: {json.dumps(params, indent=2)}")
            
            response = requests.post(url, json=params, headers=headers, timeout=30)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("retCode") == 0:
                    print("✅ SUCCESS!")
                else:
                    print(f"❌ API Error: {data.get('retMsg')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_public_endpoints():
    """Test public endpoints to verify API connectivity"""
    print("\n=== Testing Public Endpoints ===")
    
    try:
        # Test public ticker endpoint
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=HYPEUSDT"
        response = requests.get(url, timeout=10)
        print(f"Public ticker status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Public ticker result: {data.get('retCode')}")
        else:
            print(f"Public ticker error: {response.text}")
    except Exception as e:
        print(f"Public endpoint error: {str(e)}")

if __name__ == "__main__":
    test_public_endpoints()
    test_bybit_endpoints()
