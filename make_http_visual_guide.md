# Visual Guide: Make.com HTTP GET with TA Worker

## 🎯 Complete Setup Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Make.com Scenario                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              HTTP Module Setup                      │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │ Method: GET                                         │    │
│  │ URL: https://ta-worker-ta-worker-ai.up.railway.app │    │
│  │        /v1/run                                      │    │
│  │                                                     │    │
│  │ Parameters:                                         │    │
│  │ ├─ symbol: HYPEUSDT                                │    │
│  │ ├─ tfs: 5m,15m,1h,1d                              │    │
│  │ ├─ lookback: 300                                  │    │
│  │ └─ category: linear                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                              │
│                              ▼                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              TA Worker Response                     │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │ {                                                  │    │
│  │   "symbol": "HYPEUSDT",                           │    │
│  │   "now": "2025-08-20T16:35:15.792776+00:00",      │    │
│  │   "features": {                                    │    │
│  │     "5m": {                                        │    │
│  │       "price": 42.444,                            │    │
│  │       "rsi14": 53.541,                            │    │
│  │       "macd": {"val": 0.129, "signal": 0.034},    │    │
│  │       "support_resistance": {                      │    │
│  │         "support": [47.39, 46.404, 43.803],       │    │
│  │         "resistance": [42.869, 44.362, 47.126]    │    │
│  │       }                                            │    │
│  │     },                                             │    │
│  │     "15m": {                                       │    │
│  │       "price": 42.444,                            │    │
│  │       "rsi14": 53.541,                            │    │
│  │       "macd": {"val": 0.129, "signal": 0.034},    │    │
│  │       "support_resistance": {                      │    │
│  │         "support": [47.39, 46.404, 43.803],       │    │
│  │         "resistance": [42.869, 44.362, 47.126]    │    │
│  │       }                                            │    │
│  │     }                                              │    │
│  │   }                                                │    │
│  │ }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Step-by-Step Visual Guide

### Step 1: Add HTTP Module
```
┌─────────────────────────────────────────────────────────────┐
│                    Make.com Interface                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Search Modules] ──────────────────────────────────────┐   │
│  │ HTTP                                              │   │
│  │ Telegram                                         │   │
│  │ Google Sheets                                    │   │
│  │ ChatGPT                                          │   │
│  └───────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              HTTP Module                            │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │ Method: [GET ▼]                            │    │    │
│  │  │ URL: [https://ta-worker-ta-worker-ai...]   │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Configure Parameters
```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Module Configuration                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Method: GET                                               │
│  URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run │
│                                                             │
│  Parameters:                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Name: symbol    Value: HYPEUSDT                    │    │
│  │ Name: tfs       Value: 5m,15m,1h,1d               │    │
│  │ Name: lookback  Value: 300                         │    │
│  │ Name: category  Value: linear                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Headers:                                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Content-Type: application/json                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  [OK] [Cancel] [Test]                                      │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Test Connection
```
┌─────────────────────────────────────────────────────────────┐
│                    Test Results                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Status: 200 OK                                         │
│  ⏱️ Duration: 2.3 seconds                                  │
│                                                             │
│  Response:                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ {                                                  │    │
│  │   "symbol": "HYPEUSDT",                           │    │
│  │   "now": "2025-08-20T16:35:15.792776+00:00",      │    │
│  │   "features": {                                    │    │
│  │     "15m": {                                       │    │
│  │       "price": 42.444,                            │    │
│  │       "rsi14": 53.541,                            │    │
│  │       "macd": {"val": 0.129, "signal": 0.034}     │    │
│  │     }                                              │    │
│  │   }                                                │    │
│  │ }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Mapping Examples

### Basic Data Access
```
┌─────────────────────────────────────────────────────────────┐
│                    Data Mapping in Make.com                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Symbol: {{1.symbol}}                                      │
│  → Returns: "HYPEUSDT"                                     │
│                                                             │
│  Timestamp: {{1.now}}                                      │
│  → Returns: "2025-08-20T16:35:15.792776+00:00"             │
│                                                             │
│  5m Price: {{1.features.5m.price}}                         │
│  → Returns: 42.444                                         │
│                                                             │
│  15m Price: {{1.features.15m.price}}                       │
│  → Returns: 42.444                                         │
│                                                             │
│  1h Price: {{1.features.1h.price}}                         │
│  → Returns: 42.444                                         │
│                                                             │
│  1d Price: {{1.features.1d.price}}                         │
│  → Returns: 42.444                                         │
│                                                             │
│  5m RSI: {{1.features.5m.rsi14}}                           │
│  → Returns: 53.541                                         │
│                                                             │
│  15m RSI: {{1.features.15m.rsi14}}                         │
│  → Returns: 53.541                                         │
│                                                             │
│  1h RSI: {{1.features.1h.rsi14}}                           │
│  → Returns: 53.541                                         │
│                                                             │
│  1d RSI: {{1.features.1d.rsi14}}                           │
│  → Returns: 53.541                                         │
└─────────────────────────────────────────────────────────────┘
```

### Advanced Data Access
```
┌─────────────────────────────────────────────────────────────┐
│                    Advanced Data Mapping                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Support Level 1: {{1.features.15m.support_resistance.support[0]}} │
│  → Returns: 47.39                                          │
│                                                             │
│  Resistance Level 1: {{1.features.15m.support_resistance.resistance[0]}} │
│  → Returns: 42.869                                         │
│                                                             │
│  Fibonacci 0.618: {{1.features.15m.fibonacci.retracements.0.618}} │
│  → Returns: 42.550                                         │
│                                                             │
│  Elliott Pattern: {{1.features.15m.elliott_waves.pattern}} │
│  → Returns: "corrective"                                   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Complete Workflow Example

```
┌─────────────────────────────────────────────────────────────┐
│                    Complete Make.com Workflow               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   Schedule      │───▶│   HTTP GET      │───▶│   Router    │ │
│  │  (Every 15min)  │    │  (TA Worker)    │    │ (Success?)  │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│                                                             │
│                                    │                        │
│                                    ▼                        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   Telegram      │◀───│   ChatGPT       │◀───│   Success   │ │
│  │  (Alert)        │    │  (Analysis)     │    │   Route     │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │   Google Sheets │◀───│   Error Route   │                  │
│  │  (Log Data)     │    │  (Notification) │                  │
│  └─────────────────┘    └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Quick Setup Checklist

```
┌─────────────────────────────────────────────────────────────┐
│                    Setup Checklist                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ☐ Create new Make.com scenario                            │
│  ☐ Add HTTP module                                         │
│  ☐ Set Method to GET                                       │
│  ☐ Enter TA Worker URL                                     │
│  ☐ Add symbol parameter (HYPEUSDT)                         │
│  ☐ Add tfs parameter (15m,1h,4h,1d)                       │
│  ☐ Add lookback parameter (300)                            │
│  ☐ Add category parameter (linear)                         │
│  ☐ Test with "Run once"                                    │
│  ☐ Verify JSON response                                    │
│  ☐ Add next module (Telegram/ChatGPT/etc.)                 │
│  ☐ Map data using {{1.field}} syntax                       │
│  ☐ Test full workflow                                      │
│  ☐ Schedule scenario                                       │
└─────────────────────────────────────────────────────────────┘
```

## 🚨 Common Issues & Solutions

```
┌─────────────────────────────────────────────────────────────┐
│                    Troubleshooting Guide                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ Issue: HTTP Timeout                                     │
│  ✅ Solution: Increase timeout to 30000ms                   │
│                                                             │
│  ❌ Issue: No Response                                      │
│  ✅ Solution: Check URL and parameters                      │
│                                                             │
│  ❌ Issue: JSON Parse Error                                 │
│  ✅ Solution: Add Content-Type header                       │
│                                                             │
│  ❌ Issue: Parameters Not Working                           │
│  ✅ Solution: Verify parameter names exactly                │
│                                                             │
│  ❌ Issue: Data Mapping Fails                               │
│  ✅ Solution: Use correct {{1.field}} syntax                │
└─────────────────────────────────────────────────────────────┘
```

## 📞 Quick Reference

**TA Worker URL**: `https://ta-worker-ta-worker-ai.up.railway.app/v1/run`

**Required Parameters**:
- `symbol`: HYPEUSDT, BTCUSDT, ETHUSDT, SOLUSDT
- `tfs`: 5m,15m,1h,1d
- `lookback`: 300
- `category`: linear

**Available Timeframes**: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w, 1M

**Data Access**: `{{1.features.5m.price}}`, `{{1.features.15m.price}}`, `{{1.features.1h.price}}`, `{{1.features.1d.price}}`
