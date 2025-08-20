# Bybit Position Checking Guide

## 🎯 Overview

Your TA Worker now includes **Bybit position checking endpoints** that allow you to:
- ✅ Check all open positions
- ✅ Check positions for specific symbols
- ✅ Get account information and wallet balance
- ✅ Integrate position data with Make.com workflows

## 🔑 Setup Required

### 1. Bybit API Credentials

**You need to add these environment variables to Railway:**

```
BYBIT_API_KEY=your_api_key_here
BYBIT_SECRET_KEY=your_secret_key_here
BYBIT_TESTNET=false
```

### 2. How to Get Bybit API Keys

1. **Log into Bybit**
2. **Go to API Management** (Account → API Management)
3. **Create New API Key**
4. **Set permissions:**
   - ✅ **Read** (required for position checking)
   - ❌ **Trade** (not needed for position checking)
   - ❌ **Transfer** (not needed for position checking)
5. **Copy API Key and Secret Key**
6. **Add to Railway environment variables**

## 📊 Available Endpoints

### 1. Get All Open Positions
```
GET /v1/positions?category=linear
```

**Response:**
```json
{
  "success": true,
  "total_open_positions": 2,
  "positions": [
    {
      "symbol": "HYPEUSDT",
      "side": "Buy",
      "size": 100.0,
      "entry_price": 42.50,
      "mark_price": 43.20,
      "unrealized_pnl": 70.0,
      "realized_pnl": 0.0,
      "leverage": 10.0,
      "margin_mode": "ISOLATED_MARGIN",
      "position_mode": "0",
      "stop_loss": 40.00,
      "take_profit": 45.00,
      "position_idx": "0",
      "category": "linear",
      "updated_time": "1703123456789"
    }
  ],
  "timestamp": "2025-08-20T16:35:15.792776+00:00",
  "category": "linear",
  "symbol_filter": "all"
}
```

### 2. Get Positions for Specific Symbol
```
GET /v1/positions?symbol=HYPEUSDT&category=linear
```

**Response:**
```json
{
  "success": true,
  "total_open_positions": 1,
  "positions": [
    {
      "symbol": "HYPEUSDT",
      "side": "Buy",
      "size": 100.0,
      "entry_price": 42.50,
      "mark_price": 43.20,
      "unrealized_pnl": 70.0,
      "realized_pnl": 0.0,
      "leverage": 10.0,
      "margin_mode": "ISOLATED_MARGIN",
      "position_mode": "0",
      "stop_loss": 40.00,
      "take_profit": 45.00,
      "position_idx": "0",
      "category": "linear",
      "updated_time": "1703123456789"
    }
  ],
  "timestamp": "2025-08-20T16:35:15.792776+00:00",
  "category": "linear",
  "symbol_filter": "HYPEUSDT"
}
```

### 3. Get Account Information
```
GET /v1/account
```

**Response:**
```json
{
  "success": true,
  "account_info": [
    {
      "accountType": "UNIFIED",
      "accountLTV": "0.8",
      "accountIMRate": "0.1",
      "accountMMRate": "0.05",
      "totalEquity": "10000.00",
      "totalWalletBalance": "9500.00",
      "totalMarginBalance": "10000.00",
      "totalAvailableBalance": "8000.00",
      "totalPerpUPL": "500.00",
      "totalInitialMargin": "1000.00",
      "totalMaintenanceMargin": "500.00",
      "coin": [
        {
          "coin": "USDT",
          "equity": "10000.00",
          "walletBalance": "9500.00",
          "availableToWithdraw": "8000.00",
          "availableToSend": "8000.00",
          "borrowAmount": "0.00",
          "accruedInterest": "0.00",
          "totalOrderIM": "0.00",
          "totalPositionIM": "1000.00",
          "totalPositionMM": "500.00",
          "unrealisedPnl": "500.00",
          "cumRealisedPnl": "0.00"
        }
      ]
    }
  ],
  "timestamp": "2025-08-20T16:35:15.792776+00:00"
}
```

## 🔧 Make.com Integration

### 1. Check All Positions

**HTTP Module Configuration:**
```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/positions
Parameters:
  category: linear
```

**Data Access in Make.com:**
```
Total Positions: {{1.total_open_positions}}
First Position Symbol: {{1.positions[0].symbol}}
First Position Side: {{1.positions[0].side}}
First Position Size: {{1.positions[0].size}}
First Position PnL: {{1.positions[0].unrealized_pnl}}
```

### 2. Check Specific Symbol Position

**HTTP Module Configuration:**
```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/positions
Parameters:
  symbol: HYPEUSDT
  category: linear
```

**Data Access in Make.com:**
```
Has Position: {{1.total_open_positions > 0}}
Position Side: {{1.positions[0].side}}
Position Size: {{1.positions[0].size}}
Entry Price: {{1.positions[0].entry_price}}
Current Price: {{1.positions[0].mark_price}}
Unrealized PnL: {{1.positions[0].unrealized_pnl}}
```

### 3. Get Account Balance

**HTTP Module Configuration:**
```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/account
```

**Data Access in Make.com:**
```
Total Equity: {{1.account_info[0].totalEquity}}
Wallet Balance: {{1.account_info[0].totalWalletBalance}}
Available Balance: {{1.account_info[0].totalAvailableBalance}}
Unrealized PnL: {{1.account_info[0].totalPerpUPL}}
```

## 📱 Complete Make.com Workflow Example

### Scenario: Position Monitoring with Alerts

```
1. Schedule (Every 5 minutes)
   ↓
2. HTTP GET /v1/positions?category=linear
   ↓
3. Router (Check if has positions)
   ↓
4. HTTP GET /v1/run?symbol=HYPEUSDT&tfs=5m,15m,1h,1d
   ↓
5. ChatGPT (Analyze position + TA data)
   ↓
6. Router (Based on ChatGPT recommendation)
   ↓
7. Telegram (Send alert with position info)
```

### Telegram Alert Example

**Message Template:**
```
📊 Position Alert: {{2.symbol}}

💰 Position Details:
   Side: {{1.positions[0].side}}
   Size: {{1.positions[0].size}}
   Entry: ${{1.positions[0].entry_price}}
   Current: ${{1.positions[0].mark_price}}
   PnL: ${{1.positions[0].unrealized_pnl}}

📈 Technical Analysis:
   5m RSI: {{3.features.5m.rsi14}}
   15m RSI: {{3.features.15m.rsi14}}
   1h RSI: {{3.features.1h.rsi14}}

🎯 Support: ${{3.features.15m.support_resistance.support[0]}}
🎯 Resistance: ${{3.features.15m.support_resistance.resistance[0]}}

🤖 AI Recommendation: {{4.recommendation}}
```

## 🎯 Advanced Use Cases

### 1. Position Risk Management

**Check position size vs account balance:**
```
Position Value: {{1.positions[0].size * 1.positions[0].mark_price}}
Account Equity: {{5.account_info[0].totalEquity}}
Risk Percentage: {{(1.positions[0].size * 1.positions[0].mark_price) / 5.account_info[0].totalEquity * 100}}
```

### 2. Multi-Symbol Position Monitoring

**Create separate scenarios for each symbol:**
```
Scenario 1: HYPEUSDT Position Monitor
Scenario 2: BTCUSDT Position Monitor
Scenario 3: ETHUSDT Position Monitor
```

### 3. Position Performance Tracking

**Track PnL over time:**
```
Daily PnL: {{1.positions[0].unrealized_pnl}}
Total PnL: {{1.positions[0].realized_pnl + 1.positions[0].unrealized_pnl}}
ROI: {{(1.positions[0].unrealized_pnl / (1.positions[0].size * 1.positions[0].entry_price)) * 100}}
```

## 🚨 Error Handling

### Common Error Responses

**No API Credentials:**
```json
{
  "error": "Bybit API credentials not configured",
  "message": "Please set BYBIT_API_KEY and BYBIT_SECRET_KEY environment variables"
}
```

**API Error:**
```json
{
  "error": "Bybit API error",
  "retCode": 10001,
  "retMsg": "Invalid API key",
  "data": {...}
}
```

**Network Error:**
```json
{
  "error": "Network error",
  "message": "Connection timeout"
}
```

### Make.com Error Handling

**Add Router after HTTP module:**
```
Condition: {{1.error}}
Route 1: Error notification (Telegram/Email)
Route 2: Continue with normal flow
```

## 🔒 Security Best Practices

1. **Use Read-Only API Keys** - Only enable "Read" permissions
2. **IP Whitelist** - Restrict API access to Railway IPs
3. **Regular Key Rotation** - Change API keys periodically
4. **Monitor Usage** - Check API usage in Bybit dashboard
5. **Test on Testnet** - Use `BYBIT_TESTNET=true` for testing

## 📞 Quick Reference

**Endpoints:**
- All Positions: `GET /v1/positions?category=linear`
- Symbol Positions: `GET /v1/positions?symbol=HYPEUSDT&category=linear`
- Account Info: `GET /v1/account`

**Required Environment Variables:**
- `BYBIT_API_KEY`
- `BYBIT_SECRET_KEY`
- `BYBIT_TESTNET` (optional, default: false)

**Data Access Examples:**
- Position Count: `{{1.total_open_positions}}`
- Position Side: `{{1.positions[0].side}}`
- Position PnL: `{{1.positions[0].unrealized_pnl}}`
- Account Balance: `{{1.account_info[0].totalEquity}}`
