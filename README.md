
# TA Worker (FastAPI) — Multi‑TF OHLCV + Advanced Indicators for Futures Trading

Deploy this service on Railway. It exposes an HTTP endpoint that fetches futures candles
from Bybit, computes advanced technical indicators across multiple timeframes, and returns a comprehensive
snapshot JSON your Make.com scenario can pass to ChatGPT's Decision Engine.

## 🚀 Advanced Features
- **Order Blocks Detection** - Identify liquidity zones and breakout points
- **Support & Resistance Levels** - Dynamic pivot point analysis
- **Fibonacci Retracements** - Standard and extension levels
- **Elliott Wave Analysis** - Pattern recognition and wave counting
- **Multi-timeframe Analysis** - 15m, 1h, 4h, 1d timeframes
- **Futures-focused** - Optimized for perpetual futures trading

## Endpoints

### Technical Analysis
- `GET /v1/healthz` — simple health check
- `GET /v1/run` — builds and returns the snapshot
  - Query params (optional): `symbol`, `tfs` (comma list), `lookback`, `category`

Example:
```
GET /v1/run?symbol=HYPEUSDT&tfs=5m,15m,1h,1d&lookback=300&category=linear
```

### Bybit Position Management
- `GET /v1/positions` — get all open positions
  - Query params (optional): `symbol`, `category`
- `GET /v1/positions/{symbol}` — get positions for specific symbol
  - Path param: `symbol` (e.g., HYPEUSDT)
  - Query params (optional): `category`
- `GET /v1/account` — get account information and wallet balance

Examples:
```
GET /v1/positions?category=linear
GET /v1/positions?symbol=HYPEUSDT&category=linear
GET /v1/positions/HYPEUSDT?category=linear
GET /v1/account
```

## Deploy on Railway

1. Create a new service from this repository.
2. Start command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
3. Variables (Settings → Variables):
   - `SYMBOL` (default pair)
   - `TF_LIST` (e.g., `5m,15m,1h,1d`)
   - `LOOKBACK` (e.g., `300`)
   - `BYBIT_CATEGORY` (`linear` for futures, `spot` for spot trading)
   - Optional: `WRITE_SNAPSHOT_JSON=true`
   - Optional: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (if you want to upsert data)
   - **Bybit API Credentials** (for position checking):
     - `BYBIT_API_KEY` (your Bybit API key)
     - `BYBIT_SECRET_KEY` (your Bybit secret key)
     - `BYBIT_TESTNET` (`true` for testnet, `false` for mainnet)

## Make.com usage

- Add **HTTP → Make a request** to `GET https://<your‑railway‑url>/v1/run?...`
- Use the returned JSON `features` as input to your ChatGPT Decision Engine.
- If you later add Supabase, the service can upsert `ohlcv` and `ta_features` automatically.

## Notes
- Only closed candles are used; the last forming bar is ignored for features.
- **Futures-focused**: Defaults to linear perpetual futures for better leverage and liquidity.
- **Advanced Indicators**: EMA(20/50/200), RSI(14), MACD(12/26/9), ATR(14), Bollinger(20,2)+bandwidth,
  ADX(14) with DI+/−, OBV, VWAP, Order Blocks, Support/Resistance, Fibonacci, Elliott Waves.
- **Smart Category Detection**: Automatically detects if symbol should use futures or spot.
