import time
import hmac
import hashlib
import requests
from typing import Dict, Any

def get_bybit_base_url() -> str:
    """Get Bybit API base URL"""
    return "https://api.bybit.com"

def sign_bybit_request(secret_key: str, param_str: str) -> str:
    """Sign Bybit API request correctly"""
    signature = hmac.new(
        secret_key.encode('utf-8'),
        param_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def get_bybit_positions_fixed(api_key: str, secret_key: str, symbol: str = None, category: str = "linear") -> Dict[str, Any]:
    """Get current open positions from Bybit with correct signature"""
    
    try:
        base_url = get_bybit_base_url()
        endpoint = "/v5/position/list"
        
        # Prepare parameters
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        
        params = {
            "api_key": api_key,
            "category": category,
            "recv_window": recv_window,
            "timestamp": timestamp
        }
        
        # Add symbol filter if provided
        if symbol:
            params["symbol"] = symbol
        
        # Convert params to query string for signature (excluding api_key)
        param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items()) if k != "api_key"])
        
        # Sign the request
        signature = sign_bybit_request(secret_key, param_str)
        params["sign"] = signature
        
        # Make the request using POST for Bybit API v5
        url = f"{base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("retCode") != 0:
            return {
                "error": "Bybit API error",
                "retCode": data.get("retCode"),
                "retMsg": data.get("retMsg"),
                "data": data
            }
        
        # Process positions
        positions = data.get("result", {}).get("list", [])
        open_positions = []
        
        for pos in positions:
            # Only include positions with size > 0 (open positions)
            if float(pos.get("size", "0")) > 0:
                open_positions.append({
                    "symbol": pos.get("symbol"),
                    "side": pos.get("side"),  # Buy/Sell
                    "size": float(pos.get("size", "0")),
                    "entry_price": float(pos.get("avgPrice", "0")),
                    "mark_price": float(pos.get("markPrice", "0")),
                    "unrealized_pnl": float(pos.get("unrealisedPnl", "0")),
                    "realized_pnl": float(pos.get("realisedPnl", "0")),
                    "leverage": float(pos.get("leverage", "0")),
                    "margin_mode": pos.get("marginMode"),  # REGULAR_MARGIN/ISOLATED_MARGIN
                    "position_mode": pos.get("positionMode"),  # 0: Merged Single, 3: Both Sides
                    "stop_loss": float(pos.get("stopLoss", "0")),
                    "take_profit": float(pos.get("takeProfit", "0")),
                    "position_idx": pos.get("positionIdx"),  # 0: One-Way Mode, 1: Buy Side, 2: Sell Side
                    "category": pos.get("category"),
                    "updated_time": pos.get("updatedTime")
                })
        
        return {
            "success": True,
            "total_open_positions": len(open_positions),
            "positions": open_positions,
            "timestamp": time.time(),
            "category": category,
            "symbol_filter": symbol if symbol else "all"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": "Network error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e)
        }

def get_bybit_account_info_fixed(api_key: str, secret_key: str) -> Dict[str, Any]:
    """Get Bybit account information with correct signature"""
    
    try:
        base_url = get_bybit_base_url()
        endpoint = "/v5/account/wallet-balance"
        
        # Prepare parameters
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        
        params = {
            "api_key": api_key,
            "accountType": "UNIFIED",
            "recv_window": recv_window,
            "timestamp": timestamp
        }
        
        # Convert params to query string for signature (excluding api_key)
        param_str = "&".join([f"{k}={v}" for k, v in sorted(params.items()) if k != "api_key"])
        
        # Sign the request
        signature = sign_bybit_request(secret_key, param_str)
        params["sign"] = signature
        
        # Make the request using POST for Bybit API v5
        url = f"{base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("retCode") != 0:
            return {
                "error": "Bybit API error",
                "retCode": data.get("retCode"),
                "retMsg": data.get("retMsg"),
                "data": data
            }
        
        # Process account info
        account_info = data.get("result", {}).get("list", [])
        
        return {
            "success": True,
            "account_info": account_info,
            "timestamp": time.time()
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": "Network error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e)
        }

# Test the functions
if __name__ == "__main__":
    api_key = "8ASH9Yxn0CJf93pRZb"
    secret_key = "GwHLhjJNcKTIwUVnhesAFN9J2jcVvcNhm0gI"
    
    print("Testing position endpoint...")
    result = get_bybit_positions_fixed(api_key, secret_key, "HYPEUSDT", "linear")
    print(result)
    
    print("\nTesting account endpoint...")
    result = get_bybit_account_info_fixed(api_key, secret_key)
    print(result)
