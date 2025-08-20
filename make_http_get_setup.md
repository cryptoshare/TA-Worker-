# How to Link TA Worker with Make.com HTTP GET Module

## 🚀 Step-by-Step Setup Guide

### Step 1: Create New Scenario in Make.com

1. **Log into Make.com**
2. **Click "Create a new scenario"**
3. **Name it**: "TA Worker GET Request"

### Step 2: Add HTTP Module

1. **Click the "+" button** in the scenario builder
2. **Search for "HTTP"** in the module search
3. **Select "HTTP"** module from the results
4. **Click "Add"** to add it to your scenario

### Step 3: Configure HTTP Module

**In the HTTP module configuration panel, fill in exactly:**

```
🔧 HTTP Module Configuration:

Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run

📋 Parameters (Add each one):
  symbol: HYPEUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear

📋 Headers (Optional):
  Content-Type: application/json
  Accept: application/json

⏱️ Timeout: 30000 (30 seconds)
```

### Step 4: Add Parameters

**To add parameters in Make.com:**

1. **Click "Add"** next to Parameters section
2. **Add each parameter one by one:**

```
Parameter 1:
  Name: symbol
  Value: HYPEUSDT

Parameter 2:
  Name: tfs
  Value: 15m,1h,4h,1d

Parameter 3:
  Name: lookback
  Value: 300

Parameter 4:
  Name: category
  Value: linear
```

### Step 5: Test the Connection

1. **Click "OK"** to save the HTTP module
2. **Click "Run once"** button (play icon)
3. **Wait for execution** (should take 5-10 seconds)
4. **Check the output** in the module

### Step 6: Verify the Response

**You should see a successful response like:**

```json
{
  "symbol": "HYPEUSDT",
  "now": "2025-08-20T16:35:15.792776+00:00",
  "features": {
    "15m": {
      "price": 42.444,
      "ema20": 41.942,
      "ema50": 41.903,
      "ema200": 42.686,
      "rsi14": 53.541,
      "macd": {
        "val": 0.129,
        "signal": 0.034,
        "hist": 0.094
      },
      "support_resistance": {
        "support": [47.39, 46.404, 43.803, 42.925, 41.564],
        "resistance": [42.869, 44.362, 47.126]
      }
    }
  }
}
```

## 🔧 Alternative Configuration Methods

### Method 1: Direct URL with Parameters

**Instead of separate parameters, you can use:**

```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run?symbol=HYPEUSDT&tfs=15m,1h,4h,1d&lookback=300&category=linear
```

### Method 2: Using Variables

**Create variables in Make.com:**

```
Variable 1: SYMBOL = HYPEUSDT
Variable 2: TIMEFRAMES = 15m,1h,4h,1d
Variable 3: LOOKBACK = 300
Variable 4: CATEGORY = linear
```

**Then use in HTTP module:**

```
Parameters:
  symbol: {{SYMBOL}}
  tfs: {{TIMEFRAMES}}
  lookback: {{LOOKBACK}}
  category: {{CATEGORY}}
```

## 📊 Accessing Data in Make.com

### Basic Data Access

Once the HTTP module runs successfully, you can access data using:

```
Symbol: {{1.symbol}}
Timestamp: {{1.now}}
15m Price: {{1.features.15m.price}}
15m RSI: {{1.features.15m.rsi14}}
15m MACD: {{1.features.15m.macd.val}}
```

### Advanced Data Access

```
Support Level 1: {{1.features.15m.support_resistance.support[0]}}
Resistance Level 1: {{1.features.15m.support_resistance.resistance[0]}}
Fibonacci 0.618: {{1.features.15m.fibonacci.retracements.0.618}}
Elliott Pattern: {{1.features.15m.elliott_waves.pattern}}
```

## 🔄 Adding More Modules

### Example: Add Telegram Alert

1. **Click "+" after HTTP module**
2. **Search for "Telegram"**
3. **Configure Telegram module:**

```
Chat ID: YOUR_CHAT_ID
Message: |
  📊 TA Worker Data: {{1.symbol}}
  
  🕐 Time: {{1.now}}
  💰 Price: ${{1.features.15m.price}}
  📈 RSI: {{1.features.15m.rsi14}}
  🎯 Support: ${{1.features.15m.support_resistance.support[0]}}
  🎯 Resistance: ${{1.features.15m.support_resistance.resistance[0]}}
```

### Example: Add Google Sheets

1. **Click "+" after HTTP module**
2. **Search for "Google Sheets"**
3. **Configure Google Sheets module:**

```
Spreadsheet ID: YOUR_SPREADSHEET_ID
Sheet Name: TA Data
Data:
  Timestamp: {{1.now}}
  Symbol: {{1.symbol}}
  Price: {{1.features.15m.price}}
  RSI: {{1.features.15m.rsi14}}
  MACD: {{1.features.15m.macd.val}}
```

## 🎯 Different Symbol Examples

### For BTCUSDT:
```
Parameters:
  symbol: BTCUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

### For ETHUSDT:
```
Parameters:
  symbol: ETHUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

### For Different Timeframes:
```
Parameters:
  symbol: HYPEUSDT
  tfs: 5m,15m,1h  (only 3 timeframes)
  lookback: 300
  category: linear
```

## 🛠️ Troubleshooting

### Issue 1: HTTP Timeout
**Solution:**
- Increase timeout to 30000 (30 seconds)
- Check TA Worker status

### Issue 2: No Response
**Solution:**
- Verify URL is correct
- Check parameters are properly set
- Test URL in browser first

### Issue 3: JSON Parsing Error
**Solution:**
- Add Content-Type header: `application/json`
- Check response format

### Issue 4: Parameters Not Working
**Solution:**
- Make sure parameter names are exactly: `symbol`, `tfs`, `lookback`, `category`
- Check parameter values are correct

## 🔍 Testing Your Setup

### Test 1: Basic Connection
1. **Run HTTP module once**
2. **Check status code is 200**
3. **Verify JSON response**

### Test 2: Data Access
1. **Add a simple module** (like Text Aggregator)
2. **Map some data**: `{{1.symbol}}`
3. **Run and verify** you see "HYPEUSDT"

### Test 3: Full Workflow
1. **Add Telegram/Email module**
2. **Map data to message**
3. **Run full scenario**

## 📱 Complete Example Workflow

```
1. HTTP Module (GET TA Worker data)
   ↓
2. Router Module (Check if successful)
   ↓
3. Telegram Module (Send alert)
   ↓
4. Google Sheets Module (Log data)
```

## 🎯 Pro Tips

1. **Always test with "Run once"** before scheduling
2. **Use variables** for easy symbol changes
3. **Add error handling** with Router modules
4. **Monitor execution logs** for issues
5. **Start simple** and add complexity gradually

## 📞 Quick Reference

**TA Worker URL**: `https://ta-worker-ta-worker-ai.up.railway.app/v1/run`

**Required Parameters**:
- `symbol`: Trading pair (e.g., HYPEUSDT)
- `tfs`: Timeframes (e.g., 15m,1h,4h,1d)
- `lookback`: Number of candles (e.g., 300)
- `category`: Market type (linear for futures)

**Response Format**: JSON with technical analysis data
