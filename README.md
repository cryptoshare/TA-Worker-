
# TA Worker (FastAPI) — Multi‑TF OHLCV + Indicators for ChatGPT

Deploy this service on Railway. It exposes an HTTP endpoint that fetches candles
from Bybit, computes indicators across multiple timeframes, and returns a compact
snapshot JSON your Make.com scenario can pass to ChatGPT's Decision Engine.

## Endpoints

- `GET /v1/healthz` — simple health check
- `GET /v1/run` — builds and returns the snapshot
  - Query params (optional): `symbol`, `tfs` (comma list), `lookback`, `category`

Example:
```
GET /v1/run?symbol=HYPEUSDT&tfs=15m,1h,4h,1d&lookback=300&category=spot
```

## Deploy on Railway

1. Create a new service from this repository.
2. Start command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
3. Variables (Settings → Variables):
   - `SYMBOL` (default pair)
   - `TF_LIST` (e.g., `15m,1h,4h,1d`)
   - `LOOKBACK` (e.g., `300`)
   - `BYBIT_CATEGORY` (`spot` or `linear`)
   - Optional: `WRITE_SNAPSHOT_JSON=true`
   - Optional: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (if you want to upsert data)

## Make.com usage

- Add **HTTP → Make a request** to `GET https://<your‑railway‑url>/v1/run?...`
- Use the returned JSON `features` as input to your ChatGPT Decision Engine.
- If you later add Supabase, the service can upsert `ohlcv` and `ta_features` automatically.

## Notes
- Only closed candles are used; the last forming bar is ignored for features.
- Indicators: EMA(20/50/200), RSI(14), MACD(12/26/9), ATR(14), Bollinger(20,2)+bandwidth,
  ADX(14) with DI+/−, OBV, VWAP, and simple HH/HL/LH/LL flags.
