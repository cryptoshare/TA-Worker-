# Make.com Integration Guide for TA Worker

## 🚀 Overview
This guide shows how to integrate your TA Worker with Make.com to create automated trading scenarios with ChatGPT Decision Engine.

## 📋 Prerequisites
- Make.com account
- TA Worker URL: `https://ta-worker-ta-worker-ai.up.railway.app`
- ChatGPT API access (for Decision Engine)

## 🔧 Step-by-Step Integration

### Step 1: Create New Scenario
1. **Log into Make.com**
2. **Click "Create a new scenario"**
3. **Name it**: "TA Worker + ChatGPT Trading Bot"

### Step 2: Add HTTP Module (Trigger)
1. **Add HTTP module** as the first step
2. **Configure as follows**:

```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  - symbol: HYPEUSDT
  - tfs: 15m,1h,4h,1d
  - lookback: 300
  - category: linear
```

### Step 3: Add ChatGPT Module (Decision Engine)
1. **Add ChatGPT module** after HTTP
2. **Configure as follows**:

```
Connection: Your ChatGPT API
Model: gpt-4
Temperature: 0.1
Max Tokens: 2000

System Message:
You are a professional cryptocurrency trading analyst. Analyze the technical data provided and give clear trading recommendations.

User Message:
Analyze this technical data for {symbol} and provide:
1. Overall market sentiment (Bullish/Bearish/Neutral)
2. Key support and resistance levels
3. Entry points with stop loss and take profit
4. Risk level (Low/Medium/High)
5. Confidence score (1-10)

Technical Data:
{JSON data from TA Worker}
```

### Step 4: Add Notification Module (Optional)
1. **Add Telegram/Email/Slack** module
2. **Send trading signals** based on ChatGPT analysis

### Step 5: Add Trading Bot Module (Optional)
1. **Add Bybit API** module for automated trading
2. **Execute trades** based on signals

## 📊 Example Scenario Structure

```
HTTP Request (TA Worker)
    ↓
ChatGPT Analysis
    ↓
Condition (Check confidence > 7)
    ↓
Telegram Notification
    ↓
Bybit Trading (if conditions met)
```

## 🔄 Scheduling Options

### Option 1: Manual Trigger
- Run scenario manually when needed

### Option 2: Scheduled Trigger
- **Add Schedule module** as first step
- **Set frequency**: Every 15 minutes, 1 hour, 4 hours, or daily

### Option 3: Webhook Trigger
- **Add Webhook module** as first step
- **Use webhook URL** to trigger from external sources

## 📈 Advanced Configuration

### Multiple Symbols
```
HTTP Request 1: HYPEUSDT
HTTP Request 2: BTCUSDT
HTTP Request 3: ETHUSDT
    ↓
Aggregator (Combine data)
    ↓
ChatGPT Analysis (Multi-symbol)
```

### Timeframe Analysis
```
HTTP Request 1: 15m data
HTTP Request 2: 1h data
HTTP Request 3: 4h data
HTTP Request 4: 1d data
    ↓
Aggregator (Combine timeframes)
    ↓
ChatGPT Analysis (Multi-timeframe)
```

## 🎯 Example ChatGPT Prompt

```
You are an expert cryptocurrency trading analyst. Analyze the following technical data for {symbol} and provide a comprehensive trading recommendation.

Technical Analysis Data:
- Price: ${price}
- RSI (14): {rsi14}
- MACD: {macd_val} (Signal: {macd_signal})
- Support Levels: {support_levels}
- Resistance Levels: {resistance_levels}
- Fibonacci Retracements: {fibonacci_levels}
- Elliott Wave Pattern: {elliott_pattern} (Confidence: {elliott_confidence})
- Order Blocks: {order_blocks_count} bullish, {order_blocks_count} bearish

Please provide:
1. **Market Sentiment**: Bullish/Bearish/Neutral
2. **Key Levels**: 
   - Strong Support: ${level}
   - Strong Resistance: ${level}
3. **Entry Strategy**:
   - Entry Price: ${price}
   - Stop Loss: ${price}
   - Take Profit 1: ${price}
   - Take Profit 2: ${price}
4. **Risk Assessment**: Low/Medium/High
5. **Confidence Score**: 1-10
6. **Reasoning**: Brief explanation of analysis

Format your response as JSON for easy parsing.
```

## 🔧 Make.com Module Configuration

### HTTP Module Settings
```
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Method: GET
Parameters:
  symbol: {{1.symbol}}
  tfs: 15m,1h,4h,1d
  lookback: 300
  category: linear
Headers:
  Content-Type: application/json
```

### ChatGPT Module Settings
```
Model: gpt-4
Temperature: 0.1
Max Tokens: 2000
System Message: [Use the prompt above]
User Message: Analyze this data: {{1.body}}
```

### Router Module (for different conditions)
```
Route 1: Confidence > 7 (High confidence trades)
Route 2: Confidence 5-7 (Medium confidence trades)
Route 3: Confidence < 5 (Low confidence - just monitor)
```

## 📱 Notification Examples

### Telegram Message Format
```
🚨 TRADING SIGNAL: {symbol}

📊 Analysis:
- Sentiment: {sentiment}
- Confidence: {confidence}/10
- Risk Level: {risk}

💰 Entry Strategy:
- Entry: ${entry_price}
- Stop Loss: ${stop_loss}
- Take Profit 1: ${tp1}
- Take Profit 2: ${tp2}

📈 Key Levels:
- Support: ${support}
- Resistance: ${resistance}

⚠️ Risk: {risk_level}
```

### Email Format
```
Subject: Trading Signal - {symbol} - {sentiment}

Dear Trader,

Technical analysis for {symbol} indicates a {sentiment} opportunity.

Key Details:
- Entry Price: ${entry_price}
- Stop Loss: ${stop_loss}
- Take Profit: ${take_profit}
- Confidence: {confidence}/10

Please review and execute according to your risk management rules.

Best regards,
Your Trading Bot
```

## 🔄 Automation Workflows

### Workflow 1: Daily Analysis
```
Schedule (Daily 9 AM UTC)
    ↓
TA Worker (Multiple symbols)
    ↓
ChatGPT Analysis
    ↓
Email Report
```

### Workflow 2: Real-time Monitoring
```
Schedule (Every 15 minutes)
    ↓
TA Worker (HYPEUSDT)
    ↓
ChatGPT Analysis
    ↓
Condition (Confidence > 8)
    ↓
Telegram Alert
```

### Workflow 3: Portfolio Management
```
Schedule (Every hour)
    ↓
TA Worker (Portfolio symbols)
    ↓
ChatGPT Analysis
    ↓
Risk Assessment
    ↓
Position Sizing
    ↓
Trading Execution
```

## 🛡️ Risk Management

### Stop Loss Rules
- **Conservative**: 2% stop loss
- **Moderate**: 3% stop loss
- **Aggressive**: 5% stop loss

### Position Sizing
- **Low Risk**: 1% of portfolio
- **Medium Risk**: 2% of portfolio
- **High Risk**: 3% of portfolio

### Confidence Thresholds
- **Execute Trade**: Confidence > 7
- **Monitor Only**: Confidence 5-7
- **Ignore**: Confidence < 5

## 📊 Performance Tracking

### Add Google Sheets Module
```
Track in spreadsheet:
- Date/Time
- Symbol
- Entry Price
- Exit Price
- P&L
- Confidence Score
- Strategy Used
```

## 🔧 Troubleshooting

### Common Issues
1. **HTTP Timeout**: Increase timeout to 30 seconds
2. **Rate Limits**: Add delays between requests
3. **Data Parsing**: Use JSON parser module
4. **API Errors**: Add error handling routes

### Error Handling
```
HTTP Request
    ↓
Router (Success/Error)
    ↓
Success: Continue to ChatGPT
Error: Send error notification
```

## 🎯 Best Practices

1. **Start Small**: Test with one symbol first
2. **Monitor Performance**: Track success rate
3. **Risk Management**: Always use stop losses
4. **Regular Review**: Adjust parameters monthly
5. **Backup Plans**: Have manual override options

## 📞 Support

For issues with:
- **TA Worker**: Check Railway logs
- **Make.com**: Check scenario execution logs
- **ChatGPT**: Verify API key and quotas
- **Trading**: Review risk management rules
