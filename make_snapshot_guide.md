# How to Use TA Worker in Make.com to Get Snapshots

## 🚀 Quick Start Guide

### Step 1: Create New Scenario in Make.com

1. **Log into Make.com**
2. **Click "Create a new scenario"**
3. **Name it**: "TA Worker Snapshot"

### Step 2: Add HTTP Module

1. **Click the "+" button** to add your first module
2. **Search for "HTTP"** and select "HTTP" module
3. **Configure the HTTP module**:

```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: HYPEUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

### Step 3: Test the Connection

1. **Click "OK"** to save the HTTP module
2. **Click "Run once"** to test
3. **Check the output** - you should see JSON data

## 📊 Understanding the Snapshot Data

The TA Worker returns a JSON snapshot with this structure:

```json
{
  "symbol": "HYPEUSDT",
  "now": "2025-08-19T14:56:33.743190+00:00",
  "features": {
    "15m": {
      "price": 42.502,
      "ema20": 43.074,
      "ema50": 42.933,
      "ema200": 43.928,
      "rsi14": 41.324,
      "macd": {
        "val": 0.117,
        "signal": 0.228,
        "hist": -0.111
      },
      "atr14": 0.454,
      "bb": {
        "mid": 43.182,
        "up": 43.976,
        "dn": 42.388,
        "bw": 0.037
      },
      "adx14": 70.018,
      "di_plus": 15.183,
      "di_minus": 21.838,
      "obv": -1679025.15,
      "vwap": 44.515,
      "structure": {
        "hh": 0,
        "hl": 0,
        "lh": 1,
        "ll": 1
      },
      "order_blocks": {
        "bullish": [...],
        "bearish": [...]
      },
      "support_resistance": {
        "support": [47.39, 46.404, 43.803, 42.925, 41.564],
        "resistance": [42.869, 44.362, 47.126]
      },
      "fibonacci": {
        "retracements": {
          "0.0": 44.146,
          "0.236": 43.537,
          "0.382": 43.160,
          "0.5": 42.855,
          "0.618": 42.550,
          "0.786": 42.117,
          "1.0": 41.564
        },
        "recent_high": 44.146,
        "recent_low": 41.564
      },
      "elliott_waves": {
        "pattern": "corrective",
        "confidence": 0.0,
        "wave_count": 114,
        "current_wave": {...}
      }
    },
    "1h": { /* similar structure */ },
    "4h": { /* similar structure */ },
    "1d": { /* similar structure */ }
  }
}
```

## 🔧 Make.com Module Configuration Examples

### Example 1: Basic Snapshot Retrieval

**HTTP Module Configuration:**
```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: HYPEUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
Headers:
  Content-Type: application/json
```

### Example 2: Multiple Symbols

**HTTP Module 1 (HYPEUSDT):**
```
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: HYPEUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

**HTTP Module 2 (BTCUSDT):**
```
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: BTCUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

### Example 3: Different Timeframes

**HTTP Module 1 (15m only):**
```
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: HYPEUSDT
  tfs: 15m
  lookback: 300
  category: linear
```

**HTTP Module 2 (1h only):**
```
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: HYPEUSDT
  tfs: 1h
  lookback: 300
  category: linear
```

## 📱 Using Snapshot Data in Make.com

### Accessing Data in Make.com

Once you have the snapshot, you can access data using Make.com's mapping:

```
Symbol: {{1.symbol}}
Timestamp: {{1.now}}
15m Price: {{1.features.15m.price}}
15m RSI: {{1.features.15m.rsi14}}
15m MACD: {{1.features.15m.macd.val}}
15m Support: {{1.features.15m.support_resistance.support[0]}}
15m Resistance: {{1.features.15m.support_resistance.resistance[0]}}
```

### Example: Send Telegram Alert with Snapshot Data

**Telegram Module Configuration:**
```
Chat ID: YOUR_CHAT_ID
Message: |
  📊 TA Worker Snapshot: {{1.symbol}}
  
  🕐 Time: {{1.now}}
  
  📈 15m Analysis:
  - Price: ${{1.features.15m.price}}
  - RSI: {{1.features.15m.rsi14}}
  - MACD: {{1.features.15m.macd.val}}
  - Support: ${{1.features.15m.support_resistance.support[0]}}
  - Resistance: ${{1.features.15m.support_resistance.resistance[0]}}
  
  📊 1h Analysis:
  - Price: ${{1.features.1h.price}}
  - RSI: {{1.features.1h.rsi14}}
  - Support: ${{1.features.1h.support_resistance.support[0]}}
  - Resistance: ${{1.features.1h.support_resistance.resistance[0]}}
```

### Example: Save to Google Sheets

**Google Sheets Module Configuration:**
```
Spreadsheet ID: YOUR_SPREADSHEET_ID
Sheet Name: TA Snapshots
Data:
  Timestamp: {{1.now}}
  Symbol: {{1.symbol}}
  15m_Price: {{1.features.15m.price}}
  15m_RSI: {{1.features.15m.rsi14}}
  15m_MACD: {{1.features.15m.macd.val}}
  1h_Price: {{1.features.1h.price}}
  1h_RSI: {{1.features.1h.rsi14}}
  4h_Price: {{1.features.4h.price}}
  4h_RSI: {{1.features.4h.rsi14}}
  1d_Price: {{1.features.1d.price}}
  1d_RSI: {{1.features.1d.rsi14}}
```

## 🔄 Scheduling Options

### Option 1: Manual Trigger
- Run scenario manually when needed

### Option 2: Scheduled Trigger
**Schedule Module Configuration:**
```
Frequency: Every 15 minutes
Timezone: UTC
```

### Option 3: Webhook Trigger
**Webhook Module Configuration:**
```
Webhook URL: [Generated by Make.com]
Method: POST
```

## 🎯 Advanced Usage Examples

### Example 1: Conditional Alerts

**Router Module (after HTTP):**
```
Route 1: RSI Oversold
Condition: {{1.features.15m.rsi14}} < 30

Route 2: RSI Overbought
Condition: {{1.features.15m.rsi14}} > 70

Route 3: Normal
Condition: {{1.features.15m.rsi14}} >= 30 && {{1.features.15m.rsi14}} <= 70
```

### Example 2: Price Breakout Detection

**Router Module:**
```
Route 1: Breakout Above Resistance
Condition: {{1.features.15m.price}} > {{1.features.15m.support_resistance.resistance[0]}}

Route 2: Breakdown Below Support
Condition: {{1.features.15m.price}} < {{1.features.15m.support_resistance.support[0]}}

Route 3: Within Range
Condition: [Default route]
```

### Example 3: Multi-Timeframe Analysis

**Aggregator Module (combine multiple HTTP calls):**
```
HTTP 1: 15m data
HTTP 2: 1h data
HTTP 3: 4h data
HTTP 4: 1d data

Aggregator combines all timeframes for analysis
```

## 📊 Data Mapping Reference

### Basic Indicators
```
Price: {{1.features.15m.price}}
EMA20: {{1.features.15m.ema20}}
EMA50: {{1.features.15m.ema50}}
EMA200: {{1.features.15m.ema200}}
RSI: {{1.features.15m.rsi14}}
ATR: {{1.features.15m.atr14}}
VWAP: {{1.features.15m.vwap}}
```

### MACD
```
MACD Value: {{1.features.15m.macd.val}}
MACD Signal: {{1.features.15m.macd.signal}}
MACD Histogram: {{1.features.15m.macd.hist}}
```

### Bollinger Bands
```
BB Middle: {{1.features.15m.bb.mid}}
BB Upper: {{1.features.15m.bb.up}}
BB Lower: {{1.features.15m.bb.dn}}
BB Bandwidth: {{1.features.15m.bb.bw}}
```

### Support & Resistance
```
Support Level 1: {{1.features.15m.support_resistance.support[0]}}
Support Level 2: {{1.features.15m.support_resistance.support[1]}}
Resistance Level 1: {{1.features.15m.support_resistance.resistance[0]}}
Resistance Level 2: {{1.features.15m.support_resistance.resistance[1]}}
```

### Fibonacci Levels
```
Fib 0.0: {{1.features.15m.fibonacci.retracements.0.0}}
Fib 0.236: {{1.features.15m.fibonacci.retracements.0.236}}
Fib 0.382: {{1.features.15m.fibonacci.retracements.0.382}}
Fib 0.5: {{1.features.15m.fibonacci.retracements.0.5}}
Fib 0.618: {{1.features.15m.fibonacci.retracements.0.618}}
Fib 0.786: {{1.features.15m.fibonacci.retracements.0.786}}
Fib 1.0: {{1.features.15m.fibonacci.retracements.1.0}}
```

### Elliott Waves
```
Pattern: {{1.features.15m.elliott_waves.pattern}}
Confidence: {{1.features.15m.elliott_waves.confidence}}
Wave Count: {{1.features.15m.elliott_waves.wave_count}}
Current Wave: {{1.features.15m.elliott_waves.current_wave.wave}}
```

## 🛠️ Troubleshooting

### Common Issues

1. **HTTP Timeout**
   - Increase timeout to 30 seconds
   - Check TA Worker status

2. **Data Not Loading**
   - Verify URL is correct
   - Check parameters
   - Test with curl first

3. **JSON Parsing Errors**
   - Use JSON parser module
   - Check data structure

### Testing Your Setup

1. **Test HTTP module** with "Run once"
2. **Check response** in Make.com logs
3. **Verify data mapping** works correctly
4. **Test full scenario** end-to-end

## 🎯 Best Practices

1. **Start Simple**: Begin with basic snapshot retrieval
2. **Test Thoroughly**: Use "Run once" to test each module
3. **Monitor Performance**: Check execution logs regularly
4. **Error Handling**: Add error routes for failed requests
5. **Data Validation**: Verify data before processing

## 📞 Support

If you encounter issues:
1. **Check TA Worker status**: Test the URL directly
2. **Review Make.com logs**: Look for error messages
3. **Verify parameters**: Ensure all required parameters are set
4. **Test with curl**: Verify the API works outside Make.com
