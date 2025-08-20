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
  tfs: 5m,15m,1h,1d
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
  Value: 5m,15m,1h,1d

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
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run?symbol=HYPEUSDT&tfs=5m,15m,1h,1d&lookback=300&category=linear
```

### Method 2: Using Variables

**Create variables in Make.com:**

```
Variable 1: SYMBOL = HYPEUSDT
Variable 2: TIMEFRAMES = 5m,15m,1h,1d
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
5m Price: {{1.features.5m.price}}
15m Price: {{1.features.15m.price}}
1h Price: {{1.features.1h.price}}
1d Price: {{1.features.1d.price}}
5m RSI: {{1.features.5m.rsi14}}
15m RSI: {{1.features.15m.rsi14}}
1h RSI: {{1.features.1h.rsi14}}
1d RSI: {{1.features.1d.rsi14}}
```

### Advanced Data Access

```
Support Level 1: {{1.features.15m.support_resistance.support[0]}}
Resistance Level 1: {{1.features.15m.support_resistance.resistance[0]}}
Fibonacci 0.618: {{1.features.15m.fibonacci.retracements.0.618}}
Elliott Pattern: {{1.features.15m.elliott_waves.pattern}}

5m Support: {{1.features.5m.support_resistance.support[0]}}
5m Resistance: {{1.features.5m.support_resistance.resistance[0]}}
1h Support: {{1.features.1h.support_resistance.support[0]}}
1h Resistance: {{1.features.1h.support_resistance.resistance[0]}}
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
  💰 5m Price: ${{1.features.5m.price}}
  💰 15m Price: ${{1.features.15m.price}}
  💰 1h Price: ${{1.features.1h.price}}
  💰 1d Price: ${{1.features.1d.price}}
  📈 5m RSI: {{1.features.5m.rsi14}}
  📈 15m RSI: {{1.features.15m.rsi14}}
  📈 1h RSI: {{1.features.1h.rsi14}}
  📈 1d RSI: {{1.features.1d.rsi14}}
  🎯 5m Support: ${{1.features.5m.support_resistance.support[0]}}
  🎯 5m Resistance: ${{1.features.5m.support_resistance.resistance[0]}}
  🎯 15m Support: ${{1.features.15m.support_resistance.support[0]}}
  🎯 15m Resistance: ${{1.features.15m.support_resistance.resistance[0]}}
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
  5m Price: {{1.features.5m.price}}
  15m Price: {{1.features.15m.price}}
  1h Price: {{1.features.1h.price}}
  1d Price: {{1.features.1d.price}}
  5m RSI: {{1.features.5m.rsi14}}
  15m RSI: {{1.features.15m.rsi14}}
  1h RSI: {{1.features.1h.rsi14}}
  1d RSI: {{1.features.1d.rsi14}}
```

## 🎯 Different Symbol Examples

## 🪙 Multiple Coin Pairs Setup

### Method 1: Individual Scenarios (Recommended)

**Create separate scenarios for each coin pair:**

#### Scenario 1: HYPEUSDT
```
Parameters:
  symbol: HYPEUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

#### Scenario 2: BTCUSDT
```
Parameters:
  symbol: BTCUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

#### Scenario 3: ETHUSDT
```
Parameters:
  symbol: ETHUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

#### Scenario 4: SOLUSDT
```
Parameters:
  symbol: SOLUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

### Method 2: Single Scenario with Variables

**Create variables in Make.com:**

```
Variable 1: SYMBOL_LIST = HYPEUSDT,BTCUSDT,ETHUSDT,SOLUSDT
Variable 2: TIMEFRAMES = 5m,15m,1h,1d
Variable 3: LOOKBACK = 300
Variable 4: CATEGORY = linear
```

**Use Iterator module to loop through symbols:**

1. **Add Iterator module** after HTTP
2. **Set Collection**: `{{SYMBOL_LIST}}`
3. **Add HTTP module inside Iterator**
4. **Use variable**: `{{item}}` for symbol

### Method 3: Different Timeframes for Different Pairs

#### For Scalping (5m focus):
```
Parameters:
  symbol: HYPEUSDT
  tfs: 1m,5m,15m,1h
  lookback: 300
  category: linear
```

#### For Swing Trading (1h focus):
```
Parameters:
  symbol: BTCUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

#### For Long-term (1d focus):
```
Parameters:
  symbol: ETHUSDT
  tfs: 1h,4h,1d,1w
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
- `symbol`: Trading pair (e.g., HYPEUSDT, BTCUSDT, ETHUSDT)
- `tfs`: Timeframes (e.g., 5m,15m,1h,1d)
- `lookback`: Number of candles (e.g., 300)
- `category`: Market type (linear for futures)

**Available Timeframes**:
- `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `12h`, `1d`, `1w`, `1M`

**Popular Coin Pairs**:
- `HYPEUSDT`, `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `ADAUSDT`, `DOTUSDT`, `LINKUSDT`, `MATICUSDT`

**Response Format**: JSON with technical analysis data

## ⚙️ How to Change Timeframes

### Remove 4h and Add 5m (Current Setup)
**Current configuration:**
```
Parameters:
  symbol: HYPEUSDT
  tfs: 5m,15m,1h,1d  (removed 4h, added 5m)
  lookback: 300
  category: linear
```

### Other Timeframe Combinations

#### For Scalping (Short-term):
```
Parameters:
  symbol: HYPEUSDT
  tfs: 1m,5m,15m,1h
  lookback: 300
  category: linear
```

#### For Day Trading:
```
Parameters:
  symbol: HYPEUSDT
  tfs: 5m,15m,1h,4h
  lookback: 300
  category: linear
```

#### For Swing Trading:
```
Parameters:
  symbol: HYPEUSDT
  tfs: 1h,4h,1d,1w
  lookback: 300
  category: linear
```

#### For Long-term Analysis:
```
Parameters:
  symbol: HYPEUSDT
  tfs: 4h,1d,1w,1M
  lookback: 300
  category: linear
```

## 🪙 Multiple Coin Pairs - Complete Guide

### Method 1: Individual Scenarios (Easiest)

**Create separate scenarios for each coin pair:**

#### Scenario 1: HYPEUSDT Analysis
```
Scenario Name: "HYPEUSDT TA Analysis"
Parameters:
  symbol: HYPEUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

#### Scenario 2: BTCUSDT Analysis
```
Scenario Name: "BTCUSDT TA Analysis"
Parameters:
  symbol: BTCUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

#### Scenario 3: ETHUSDT Analysis
```
Scenario Name: "ETHUSDT TA Analysis"
Parameters:
  symbol: ETHUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

#### Scenario 4: SOLUSDT Analysis
```
Scenario Name: "SOLUSDT TA Analysis"
Parameters:
  symbol: SOLUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
```

### Method 2: Single Scenario with Iterator (Advanced)

**Step 1: Create Variables**
```
Variable 1: SYMBOL_LIST = HYPEUSDT,BTCUSDT,ETHUSDT,SOLUSDT
Variable 2: TIMEFRAMES = 5m,15m,1h,1d
Variable 3: LOOKBACK = 300
Variable 4: CATEGORY = linear
```

**Step 2: Add Iterator Module**
1. **Click "+" after HTTP module**
2. **Search for "Iterator"**
3. **Add Iterator module**
4. **Configure:**
   ```
   Collection: {{SYMBOL_LIST}}
   Delimiter: ,
   ```

**Step 3: Add HTTP Module Inside Iterator**
1. **Click "+" inside Iterator**
2. **Add HTTP module**
3. **Configure:**
   ```
   Method: GET
   URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
   Parameters:
     symbol: {{item}}
     tfs: {{TIMEFRAMES}}
     lookback: {{LOOKBACK}}
     category: {{CATEGORY}}
   ```

### Method 3: Different Strategies for Different Pairs

#### Scalping Strategy (HYPEUSDT):
```
Parameters:
  symbol: HYPEUSDT
  tfs: 1m,5m,15m,1h
  lookback: 300
  category: linear
```

#### Swing Trading Strategy (BTCUSDT):
```
Parameters:
  symbol: BTCUSDT
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
```

#### Long-term Strategy (ETHUSDT):
```
Parameters:
  symbol: ETHUSDT
  tfs: 1h,4h,1d,1w
  lookback: 300
  category: linear
```

## 📊 Data Access for Multiple Timeframes

### All Timeframe Data Access
```
5m Price: {{1.features.5m.price}}
5m RSI: {{1.features.5m.rsi14}}
5m Support: {{1.features.5m.support_resistance.support[0]}}
5m Resistance: {{1.features.5m.support_resistance.resistance[0]}}

15m Price: {{1.features.15m.price}}
15m RSI: {{1.features.15m.rsi14}}
15m Support: {{1.features.15m.support_resistance.support[0]}}
15m Resistance: {{1.features.15m.support_resistance.resistance[0]}}

1h Price: {{1.features.1h.price}}
1h RSI: {{1.features.1h.rsi14}}
1h Support: {{1.features.1h.support_resistance.support[0]}}
1h Resistance: {{1.features.1h.support_resistance.resistance[0]}}

1d Price: {{1.features.1d.price}}
1d RSI: {{1.features.1d.rsi14}}
1d Support: {{1.features.1d.support_resistance.support[0]}}
1d Resistance: {{1.features.1d.support_resistance.resistance[0]}}
```

### Advanced Indicators for All Timeframes
```
5m MACD: {{1.features.5m.macd.val}}
5m MACD Signal: {{1.features.5m.macd.signal}}
5m MACD Histogram: {{1.features.5m.macd.hist}}

15m MACD: {{1.features.15m.macd.val}}
15m MACD Signal: {{1.features.15m.macd.signal}}
15m MACD Histogram: {{1.features.15m.macd.hist}}

1h MACD: {{1.features.1h.macd.val}}
1h MACD Signal: {{1.features.1h.macd.signal}}
1h MACD Histogram: {{1.features.1h.macd.hist}}

1d MACD: {{1.features.1d.macd.val}}
1d MACD Signal: {{1.features.1d.macd.signal}}
1d MACD Histogram: {{1.features.1d.macd.hist}}
```

## 🎯 Quick Timeframe Change Reference

### To Change from Current Setup (5m,15m,1h,1d):

**Remove 5m, Add 4h:**
```
tfs: 15m,1h,4h,1d
```

**Remove 1d, Add 30m:**
```
tfs: 5m,15m,30m,1h
```

**Remove 15m, Add 2h:**
```
tfs: 5m,1h,2h,1d
```

**Remove 1h, Add 6h:**
```
tfs: 5m,15m,6h,1d
```

### Popular Timeframe Combinations:

**Scalping**: `1m,5m,15m,1h`
**Day Trading**: `5m,15m,1h,4h`
**Swing Trading**: `1h,4h,1d,1w`
**Long-term**: `4h,1d,1w,1M`
**Current**: `5m,15m,1h,1d`

## 🔄 Scheduling Multiple Scenarios

### Option 1: Same Schedule for All
```
HYPEUSDT: Every 5 minutes
BTCUSDT: Every 5 minutes
ETHUSDT: Every 5 minutes
SOLUSDT: Every 5 minutes
```

### Option 2: Different Schedules
```
HYPEUSDT: Every 1 minute (scalping)
BTCUSDT: Every 15 minutes (swing)
ETHUSDT: Every 1 hour (long-term)
SOLUSDT: Every 5 minutes (day trading)
```

### Option 3: Market-Based Scheduling
```
HYPEUSDT: Every 5 minutes (24/7)
BTCUSDT: Every 15 minutes (24/7)
ETHUSDT: Every 1 hour (24/7)
SOLUSDT: Every 5 minutes (24/7)
```
