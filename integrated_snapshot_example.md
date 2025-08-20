# Integrated Snapshot with Position Data

## 🎯 Overview

Your TA Worker now provides **integrated snapshots** that include both technical analysis data AND current position information in a single API call. This eliminates the need for separate HTTP requests and provides a complete trading context.

## 📊 New Snapshot Structure

### Example Response with Position Data

```json
{
  "symbol": "HYPEUSDT",
  "now": "2025-08-20T16:35:15.792776+00:00",
  "features": {
    "5m": {
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
      "atr14": 0.856,
      "bb": {
        "mid": 42.123,
        "up": 43.456,
        "dn": 40.789,
        "bw": 0.063
      },
      "adx14": 25.4,
      "di_plus": 28.7,
      "di_minus": 15.3,
      "obv": 1234567.89,
      "vwap": 42.156,
      "structure": {
        "hh": 1,
        "hl": 0,
        "lh": 0,
        "ll": 0
      },
      "order_blocks": {
        "bullish": [
          {
            "start": "2025-08-20T16:20:00+00:00",
            "end": "2025-08-20T16:25:00+00:00",
            "high": 42.8,
            "low": 42.1,
            "strength": 0.85
          }
        ],
        "bearish": []
      },
      "support_resistance": {
        "support": [41.564, 42.925, 43.803, 46.404, 47.39],
        "resistance": [42.869, 44.362, 47.126]
      },
      "fibonacci": {
        "retracements": {
          "0.236": 44.123,
          "0.382": 43.456,
          "0.5": 42.789,
          "0.618": 42.123,
          "0.786": 41.456
        },
        "recent_high": 47.39,
        "recent_low": 41.564
      },
      "elliott_waves": {
        "pattern": "corrective",
        "confidence": 0.75,
        "wave_count": 5,
        "current_wave": {
          "wave": 5,
          "start_price": 42.1,
          "current_price": 42.444,
          "direction": "up"
        }
      }
    },
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
      "atr14": 0.856,
      "bb": {
        "mid": 42.123,
        "up": 43.456,
        "dn": 40.789,
        "bw": 0.063
      },
      "adx14": 25.4,
      "di_plus": 28.7,
      "di_minus": 15.3,
      "obv": 1234567.89,
      "vwap": 42.156,
      "structure": {
        "hh": 1,
        "hl": 0,
        "lh": 0,
        "ll": 0
      },
      "order_blocks": {
        "bullish": [
          {
            "start": "2025-08-20T15:45:00+00:00",
            "end": "2025-08-20T16:00:00+00:00",
            "high": 42.8,
            "low": 42.1,
            "strength": 0.85
          }
        ],
        "bearish": []
      },
      "support_resistance": {
        "support": [41.564, 42.925, 43.803, 46.404, 47.39],
        "resistance": [42.869, 44.362, 47.126]
      },
      "fibonacci": {
        "retracements": {
          "0.236": 44.123,
          "0.382": 43.456,
          "0.5": 42.789,
          "0.618": 42.123,
          "0.786": 41.456
        },
        "recent_high": 47.39,
        "recent_low": 41.564
      },
      "elliott_waves": {
        "pattern": "corrective",
        "confidence": 0.75,
        "wave_count": 5,
        "current_wave": {
          "wave": 5,
          "start_price": 42.1,
          "current_price": 42.444,
          "direction": "up"
        }
      }
    },
    "1h": {
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
      "atr14": 0.856,
      "bb": {
        "mid": 42.123,
        "up": 43.456,
        "dn": 40.789,
        "bw": 0.063
      },
      "adx14": 25.4,
      "di_plus": 28.7,
      "di_minus": 15.3,
      "obv": 1234567.89,
      "vwap": 42.156,
      "structure": {
        "hh": 1,
        "hl": 0,
        "lh": 0,
        "ll": 0
      },
      "order_blocks": {
        "bullish": [
          {
            "start": "2025-08-20T14:00:00+00:00",
            "end": "2025-08-20T15:00:00+00:00",
            "high": 42.8,
            "low": 42.1,
            "strength": 0.85
          }
        ],
        "bearish": []
      },
      "support_resistance": {
        "support": [41.564, 42.925, 43.803, 46.404, 47.39],
        "resistance": [42.869, 44.362, 47.126]
      },
      "fibonacci": {
        "retracements": {
          "0.236": 44.123,
          "0.382": 43.456,
          "0.5": 42.789,
          "0.618": 42.123,
          "0.786": 41.456
        },
        "recent_high": 47.39,
        "recent_low": 41.564
      },
      "elliott_waves": {
        "pattern": "corrective",
        "confidence": 0.75,
        "wave_count": 5,
        "current_wave": {
          "wave": 5,
          "start_price": 42.1,
          "current_price": 42.444,
          "direction": "up"
        }
      }
    },
    "1d": {
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
      "atr14": 0.856,
      "bb": {
        "mid": 42.123,
        "up": 43.456,
        "dn": 40.789,
        "bw": 0.063
      },
      "adx14": 25.4,
      "di_plus": 28.7,
      "di_minus": 15.3,
      "obv": 1234567.89,
      "vwap": 42.156,
      "structure": {
        "hh": 1,
        "hl": 0,
        "lh": 0,
        "ll": 0
      },
      "order_blocks": {
        "bullish": [
          {
            "start": "2025-08-19T00:00:00+00:00",
            "end": "2025-08-20T00:00:00+00:00",
            "high": 42.8,
            "low": 42.1,
            "strength": 0.85
          }
        ],
        "bearish": []
      },
      "support_resistance": {
        "support": [41.564, 42.925, 43.803, 46.404, 47.39],
        "resistance": [42.869, 44.362, 47.126]
      },
      "fibonacci": {
        "retracements": {
          "0.236": 44.123,
          "0.382": 43.456,
          "0.5": 42.789,
          "0.618": 42.123,
          "0.786": 41.456
        },
        "recent_high": 47.39,
        "recent_low": 41.564
      },
      "elliott_waves": {
        "pattern": "corrective",
        "confidence": 0.75,
        "wave_count": 5,
        "current_wave": {
          "wave": 5,
          "start_price": 42.1,
          "current_price": 42.444,
          "direction": "up"
        }
      }
    }
  },
  "position": {
    "has_position": true,
    "total_positions": 1,
    "positions": [
      {
        "symbol": "HYPEUSDT",
        "side": "Buy",
        "size": 100.0,
        "entry_price": 42.50,
        "mark_price": 42.444,
        "unrealized_pnl": -5.6,
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
    "category": "linear"
  }
}
```

## 🔧 API Usage

### Include Position Data (Default)
```
GET /v1/run?symbol=HYPEUSDT&tfs=5m,15m,1h,1d&include_position=true
```

### Exclude Position Data
```
GET /v1/run?symbol=HYPEUSDT&tfs=5m,15m,1h,1d&include_position=false
```

### All Parameters
```
GET /v1/run?symbol=HYPEUSDT&tfs=5m,15m,1h,1d&lookback=300&category=linear&include_position=true
```

## 📱 Make.com Integration

### Single HTTP Request (Recommended)

**HTTP Module Configuration:**
```
Method: GET
URL: https://ta-worker-ta-worker-ai.up.railway.app/v1/run
Parameters:
  symbol: HYPEUSDT
  tfs: 5m,15m,1h,1d
  lookback: 300
  category: linear
  include_position: true
```

### Data Access in Make.com

**Technical Analysis Data:**
```
Symbol: {{1.symbol}}
5m Price: {{1.features.5m.price}}
5m RSI: {{1.features.5m.rsi14}}
15m RSI: {{1.features.15m.rsi14}}
1h RSI: {{1.features.1h.rsi14}}
1d RSI: {{1.features.1d.rsi14}}

5m Support: {{1.features.5m.support_resistance.support[0]}}
5m Resistance: {{1.features.5m.support_resistance.resistance[0]}}
15m Support: {{1.features.15m.support_resistance.support[0]}}
15m Resistance: {{1.features.15m.support_resistance.resistance[0]}}

Fibonacci 0.618: {{1.features.15m.fibonacci.retracements.0.618}}
Elliott Pattern: {{1.features.15m.elliott_waves.pattern}}
```

**Position Data:**
```
Has Position: {{1.position.has_position}}
Total Positions: {{1.position.total_positions}}
Position Side: {{1.position.positions[0].side}}
Position Size: {{1.position.positions[0].size}}
Entry Price: {{1.position.positions[0].entry_price}}
Current Price: {{1.position.positions[0].mark_price}}
Unrealized PnL: {{1.position.positions[0].unrealized_pnl}}
Leverage: {{1.position.positions[0].leverage}}
Stop Loss: {{1.position.positions[0].stop_loss}}
Take Profit: {{1.position.positions[0].take_profit}}
```

## 🎯 Complete Make.com Workflow

### Scenario: Integrated Analysis with Position Context

```
1. Schedule (Every 5 minutes)
   ↓
2. HTTP GET /v1/run (with position data)
   ↓
3. Router (Check if has position)
   ↓
4. ChatGPT (Analyze TA + Position data together)
   ↓
5. Router (Based on ChatGPT recommendation)
   ↓
6. Telegram (Send comprehensive alert)
```

### ChatGPT Prompt Example

**Enhanced prompt with position context:**
```
Analyze the following trading data for {{1.symbol}}:

TECHNICAL ANALYSIS:
- Current Price: ${{1.features.15m.price}}
- 5m RSI: {{1.features.5m.rsi14}}
- 15m RSI: {{1.features.15m.rsi14}}
- 1h RSI: {{1.features.1h.rsi14}}
- 1d RSI: {{1.features.1d.rsi14}}
- Support Level: ${{1.features.15m.support_resistance.support[0]}}
- Resistance Level: ${{1.features.15m.support_resistance.resistance[0]}}
- Elliott Wave Pattern: {{1.features.15m.elliott_waves.pattern}}

CURRENT POSITION:
- Has Position: {{1.position.has_position}}
- Position Side: {{1.position.positions[0].side}}
- Position Size: {{1.position.positions[0].size}}
- Entry Price: ${{1.position.positions[0].entry_price}}
- Current Price: ${{1.position.positions[0].mark_price}}
- Unrealized PnL: ${{1.position.positions[0].unrealized_pnl}}
- Stop Loss: ${{1.position.positions[0].stop_loss}}
- Take Profit: ${{1.position.positions[0].take_profit}}

Based on the technical analysis and current position, provide:
1. Market sentiment (bullish/bearish/neutral)
2. Position recommendation (hold/add/reduce/close)
3. Risk assessment
4. Key levels to watch
5. Confidence level (1-10)
```

### Telegram Alert Example

**Comprehensive alert with both TA and position data:**
```
📊 {{1.symbol}} Analysis + Position Update

💰 Current Position:
   Side: {{1.position.positions[0].side}}
   Size: {{1.position.positions[0].size}}
   Entry: ${{1.position.positions[0].entry_price}}
   Current: ${{1.position.positions[0].mark_price}}
   PnL: ${{1.position.positions[0].unrealized_pnl}}
   SL: ${{1.position.positions[0].stop_loss}}
   TP: ${{1.position.positions[0].take_profit}}

📈 Technical Analysis:
   5m RSI: {{1.features.5m.rsi14}}
   15m RSI: {{1.features.15m.rsi14}}
   1h RSI: {{1.features.1h.rsi14}}
   1d RSI: {{1.features.1d.rsi14}}

🎯 Key Levels:
   Support: ${{1.features.15m.support_resistance.support[0]}}
   Resistance: ${{1.features.15m.support_resistance.resistance[0]}}
   Fibonacci 0.618: ${{1.features.15m.fibonacci.retracements.0.618}}

🌊 Elliott Wave: {{1.features.15m.elliott_waves.pattern}}

🤖 AI Recommendation: {{4.recommendation}}
🎯 Action: {{4.action}}
⚠️ Risk Level: {{4.risk_level}}
```

## 🎯 Benefits of Integrated Snapshots

### ✅ **Single API Call**
- No need for multiple HTTP requests
- Faster execution
- Reduced complexity

### ✅ **Complete Context**
- Technical analysis + position data
- Better decision making
- Comprehensive risk assessment

### ✅ **Real-time Position Monitoring**
- Current position status
- PnL tracking
- Stop loss and take profit monitoring

### ✅ **Enhanced AI Analysis**
- Position-aware recommendations
- Risk-adjusted suggestions
- Context-aware alerts

## 🚨 Error Handling

### Position Data Not Available
```json
{
  "position": {
    "has_position": false,
    "message": "Position checking not enabled or API credentials not configured"
  }
}
```

### API Error
```json
{
  "position": {
    "has_position": false,
    "error": "Bybit API error",
    "message": "Invalid API key"
  }
}
```

## 📞 Quick Reference

**Endpoint:** `GET /v1/run`

**Parameters:**
- `symbol`: Trading pair (e.g., HYPEUSDT)
- `tfs`: Timeframes (e.g., 5m,15m,1h,1d)
- `lookback`: Number of candles (e.g., 300)
- `category`: Market type (linear for futures)
- `include_position`: Include position data (true/false, default: true)

**Data Access:**
- TA Data: `{{1.features.5m.price}}`
- Position Data: `{{1.position.positions[0].side}}`
- Combined Analysis: Use both in ChatGPT prompts
