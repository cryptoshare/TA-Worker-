#!/usr/bin/env python3
"""
Make.com Integration Setup Helper
This script helps you test and set up the TA Worker integration with Make.com
"""

import requests
import json
import time
from datetime import datetime

# Configuration
TA_WORKER_URL = "https://ta-worker-ta-worker-ai.up.railway.app"
SYMBOL = "HYPEUSDT"
TIMEFRAMES = "15m,1h,4h,1d"
LOOKBACK = 300
CATEGORY = "linear"

def test_ta_worker():
    """Test TA Worker API"""
    print("🔍 Testing TA Worker API...")
    
    url = f"{TA_WORKER_URL}/v1/run"
    params = {
        "symbol": SYMBOL,
        "tfs": TIMEFRAMES,
        "lookback": LOOKBACK,
        "category": CATEGORY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ TA Worker API is working!")
            print(f"📊 Symbol: {data['symbol']}")
            print(f"🕐 Timestamp: {data['now']}")
            print(f"📈 Timeframes: {list(data['features'].keys())}")
            
            # Show sample data
            first_tf = list(data['features'].keys())[0]
            sample = data['features'][first_tf]
            print(f"\n📋 Sample data for {first_tf}:")
            print(f"  Price: ${sample.get('price', 'N/A')}")
            print(f"  RSI: {sample.get('rsi14', 'N/A')}")
            print(f"  Support Levels: {sample.get('support_resistance', {}).get('support', [])[:3]}")
            print(f"  Resistance Levels: {sample.get('support_resistance', {}).get('resistance', [])[:3]}")
            
            return data
        else:
            print(f"❌ TA Worker API failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing TA Worker: {e}")
        return None

def generate_chatgpt_prompt(data):
    """Generate ChatGPT prompt for the data"""
    print("\n🤖 Generating ChatGPT prompt...")
    
    if not data:
        return None
    
    # Extract key data
    symbol = data['symbol']
    features = data['features']
    
    # Get 15m data for analysis
    tf_15m = features.get('15m', {})
    
    prompt = f"""
You are an expert cryptocurrency trading analyst. Analyze the following technical data for {symbol} and provide a comprehensive trading recommendation.

Technical Analysis Data:
- Price: ${tf_15m.get('price', 'N/A')}
- RSI (14): {tf_15m.get('rsi14', 'N/A')}
- MACD: {tf_15m.get('macd', {}).get('val', 'N/A')} (Signal: {tf_15m.get('macd', {}).get('signal', 'N/A')})
- Support Levels: {tf_15m.get('support_resistance', {}).get('support', [])[:3]}
- Resistance Levels: {tf_15m.get('support_resistance', {}).get('resistance', [])[:3]}
- Fibonacci Retracements: {tf_15m.get('fibonacci', {}).get('retracements', {})}
- Elliott Wave Pattern: {tf_15m.get('elliott_waves', {}).get('pattern', 'N/A')} (Confidence: {tf_15m.get('elliott_waves', {}).get('confidence', 'N/A')})
- Order Blocks: {len(tf_15m.get('order_blocks', {}).get('bullish', []))} bullish, {len(tf_15m.get('order_blocks', {}).get('bearish', []))} bearish

Please provide your analysis in the following JSON format:
{{
    "sentiment": "Bullish/Bearish/Neutral",
    "confidence_score": 1-10,
    "risk_level": "Low/Medium/High",
    "entry_price": "price",
    "stop_loss": "price",
    "take_profit_1": "price",
    "take_profit_2": "price",
    "support_level": "price",
    "resistance_level": "price",
    "reasoning": "brief explanation"
}}
"""
    
    print("✅ ChatGPT prompt generated!")
    return prompt

def create_make_scenario_config():
    """Create Make.com scenario configuration"""
    print("\n🔧 Creating Make.com scenario configuration...")
    
    config = {
        "scenario_name": "TA Worker + ChatGPT Trading Bot",
        "ta_worker_url": TA_WORKER_URL,
        "symbol": SYMBOL,
        "timeframes": TIMEFRAMES,
        "lookback": LOOKBACK,
        "category": CATEGORY,
        "schedule": "every_15_minutes",
        "modules": [
            {
                "name": "Get TA Worker Data",
                "type": "http",
                "url": f"{TA_WORKER_URL}/v1/run",
                "method": "GET",
                "parameters": {
                    "symbol": SYMBOL,
                    "tfs": TIMEFRAMES,
                    "lookback": LOOKBACK,
                    "category": CATEGORY
                }
            },
            {
                "name": "ChatGPT Analysis",
                "type": "chatgpt",
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 2000
            },
            {
                "name": "Telegram Notification",
                "type": "telegram",
                "chat_id": "YOUR_CHAT_ID"
            }
        ]
    }
    
    # Save configuration
    with open("make_scenario_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Make.com scenario configuration saved to 'make_scenario_config.json'")
    return config

def main():
    """Main setup function"""
    print("🚀 TA Worker + Make.com Integration Setup")
    print("=" * 50)
    
    # Test TA Worker
    data = test_ta_worker()
    
    if data:
        # Generate ChatGPT prompt
        prompt = generate_chatgpt_prompt(data)
        
        # Create Make.com config
        config = create_make_scenario_config()
        
        print("\n🎯 Next Steps:")
        print("1. Copy the TA Worker URL to Make.com")
        print("2. Use the generated ChatGPT prompt")
        print("3. Set up your Telegram bot and get chat ID")
        print("4. Configure the Make.com scenario")
        print("5. Test with a manual run")
        
        print(f"\n📋 Key Information:")
        print(f"TA Worker URL: {TA_WORKER_URL}")
        print(f"Symbol: {SYMBOL}")
        print(f"Category: {CATEGORY} (futures)")
        print(f"Timeframes: {TIMEFRAMES}")
        
        if prompt:
            print(f"\n🤖 ChatGPT Prompt (copy this to Make.com):")
            print("-" * 40)
            print(prompt)
            print("-" * 40)
    
    else:
        print("\n❌ Setup failed. Please check your TA Worker deployment.")

if __name__ == "__main__":
    main()
