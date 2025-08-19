
import os, math, json, uuid, datetime, requests
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Optional Supabase (not required)
SUPABASE = None
try:
    from supabase import create_client
except Exception:
    create_client = None

load_dotenv()

# ---- Environment defaults ----
ENV_SYMBOL = os.getenv("SYMBOL", "HYPEUSDT")
ENV_TFS = [s.strip() for s in os.getenv("TF_LIST", "15m,1h,4h,1d").split(",") if s.strip()]
ENV_LOOKBACK = int(os.getenv("LOOKBACK", "300"))
ENV_CATEGORY = os.getenv("BYBIT_CATEGORY", "spot")
WRITE_SNAPSHOT_JSON = os.getenv("WRITE_SNAPSHOT_JSON", "true").lower() == "true"

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def supabase_init():
    global SUPABASE
    if SUPABASE_URL and SUPABASE_KEY and create_client:
        try:
            SUPABASE = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("[supabase] connected")
        except Exception as e:
            print("[supabase] init failed:", e)

supabase_init()

app = FastAPI(title="TA Worker (FastAPI)", version="0.1.0")

# ---------- Helpers ----------

def map_tf_to_bybit(tf: str) -> str:
    mapping = {"1m":"1","3m":"3","5m":"5","15m":"15","30m":"30",
               "1h":"60","2h":"120","4h":"240","6h":"360","12h":"720",
               "1d":"D","1w":"W","1M":"M"}
    if tf in mapping:
        return mapping[tf]
    tf = tf.lower()
    if tf.endswith("m"):
        return tf[:-1]
    if tf.endswith("h"):
        return str(int(tf[:-1]) * 60)
    raise ValueError(f"Unsupported TF: {tf}")

def ts_ms_to_iso(ts_ms: int) -> str:
    return datetime.datetime.utcfromtimestamp(ts_ms/1000).replace(tzinfo=datetime.timezone.utc).isoformat()

def fetch_ohlcv_bybit(symbol: str, tf: str, limit: int = 300, category: str = "spot") -> pd.DataFrame:
    url = "https://api.bybit.com/v5/market/kline"
    interval = map_tf_to_bybit(tf)
    params = {"category": category, "symbol": symbol, "interval": interval, "limit": str(limit)}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("retCode") != 0:
        raise RuntimeError(f"Bybit API error: {data}")
    rows = data["result"]["list"]
    rows.sort(key=lambda x: int(x[0]))
    recs = []
    for start, o, h, l, c, v, _ in rows:
        recs.append({"ts": ts_ms_to_iso(int(start)),
                     "open": float(o), "high": float(h), "low": float(l),
                     "close": float(c), "volume": float(v)})
    return pd.DataFrame.from_records(recs)

# ---------- Advanced Technical Analysis Functions ----------

def find_order_blocks(df: pd.DataFrame, lookback: int = 20) -> Dict[str, List[Dict]]:
    """Find order blocks (liquidity zones)"""
    order_blocks = {"bullish": [], "bearish": []}
    
    for i in range(lookback, len(df) - 1):
        current = df.iloc[i]
        next_candle = df.iloc[i + 1]
        
        # Bullish order block (strong move up after consolidation)
        if (next_candle['close'] > next_candle['open'] and  # Next candle is bullish
            next_candle['close'] > current['high'] and      # Breaks above current high
            current['volume'] > df['volume'].rolling(10).mean().iloc[i]):  # High volume
            
            order_blocks["bullish"].append({
                "start_idx": i,
                "high": current['high'],
                "low": current['low'],
                "strength": (next_candle['close'] - current['high']) / current['high'],
                "volume_ratio": current['volume'] / df['volume'].rolling(10).mean().iloc[i]
            })
        
        # Bearish order block (strong move down after consolidation)
        elif (next_candle['close'] < next_candle['open'] and  # Next candle is bearish
              next_candle['close'] < current['low'] and       # Breaks below current low
              current['volume'] > df['volume'].rolling(10).mean().iloc[i]):  # High volume
            
            order_blocks["bearish"].append({
                "start_idx": i,
                "high": current['high'],
                "low": current['low'],
                "strength": (current['low'] - next_candle['close']) / current['low'],
                "volume_ratio": current['volume'] / df['volume'].rolling(10).mean().iloc[i]
            })
    
    return order_blocks

def find_support_resistance_levels(df: pd.DataFrame, sensitivity: float = 0.02) -> Dict[str, List[float]]:
    """Find support and resistance levels using pivot points"""
    levels = {"support": [], "resistance": []}
    
    for i in range(2, len(df) - 2):
        current = df.iloc[i]
        
        # Resistance level (local high)
        if (current['high'] > df.iloc[i-1]['high'] and 
            current['high'] > df.iloc[i-2]['high'] and
            current['high'] > df.iloc[i+1]['high'] and
            current['high'] > df.iloc[i+2]['high']):
            
            # Check if level is significant (not too close to existing levels)
            is_significant = True
            for level in levels["resistance"]:
                if abs(current['high'] - level) / level < sensitivity:
                    is_significant = False
                    break
            
            if is_significant:
                levels["resistance"].append(current['high'])
        
        # Support level (local low)
        if (current['low'] < df.iloc[i-1]['low'] and 
            current['low'] < df.iloc[i-2]['low'] and
            current['low'] < df.iloc[i+1]['low'] and
            current['low'] < df.iloc[i+2]['low']):
            
            # Check if level is significant
            is_significant = True
            for level in levels["support"]:
                if abs(current['low'] - level) / level < sensitivity:
                    is_significant = False
                    break
            
            if is_significant:
                levels["support"].append(current['low'])
    
    # Sort levels
    levels["support"].sort(reverse=True)
    levels["resistance"].sort()
    
    return levels

def fibonacci_retracements(high: float, low: float) -> Dict[str, float]:
    """Calculate Fibonacci retracement levels"""
    diff = high - low
    return {
        "0.0": high,
        "0.236": high - 0.236 * diff,
        "0.382": high - 0.382 * diff,
        "0.5": high - 0.5 * diff,
        "0.618": high - 0.618 * diff,
        "0.786": high - 0.786 * diff,
        "1.0": low
    }

def fibonacci_extensions(high: float, low: float, retracement: float) -> Dict[str, float]:
    """Calculate Fibonacci extension levels"""
    diff = high - low
    retracement_level = high - retracement * diff
    extension_diff = high - retracement_level
    
    return {
        "1.0": retracement_level,
        "1.272": retracement_level - 1.272 * extension_diff,
        "1.618": retracement_level - 1.618 * extension_diff,
        "2.0": retracement_level - 2.0 * extension_diff,
        "2.618": retracement_level - 2.618 * extension_diff
    }

def identify_elliott_waves(df: pd.DataFrame, min_waves: int = 5) -> Dict[str, Any]:
    """Identify Elliott Wave patterns"""
    waves = []
    current_wave = 1
    wave_start_idx = 0
    wave_start_price = df.iloc[0]['low']
    
    # Find significant swing highs and lows
    swing_points = []
    for i in range(1, len(df) - 1):
        if (df.iloc[i]['high'] > df.iloc[i-1]['high'] and 
            df.iloc[i]['high'] > df.iloc[i+1]['high']):
            swing_points.append({"type": "high", "idx": i, "price": df.iloc[i]['high']})
        elif (df.iloc[i]['low'] < df.iloc[i-1]['low'] and 
              df.iloc[i]['low'] < df.iloc[i+1]['low']):
            swing_points.append({"type": "low", "idx": i, "price": df.iloc[i]['low']})
    
    # Identify wave patterns
    if len(swing_points) >= min_waves:
        for i, point in enumerate(swing_points):
            if i < len(swing_points) - 1:
                next_point = swing_points[i + 1]
                
                # Wave characteristics
                wave_length = abs(next_point['price'] - point['price'])
                wave_duration = next_point['idx'] - point['idx']
                
                waves.append({
                    "wave": current_wave,
                    "start_idx": point['idx'],
                    "end_idx": next_point['idx'],
                    "start_price": point['price'],
                    "end_price": next_point['price'],
                    "direction": "up" if next_point['price'] > point['price'] else "down",
                    "length": wave_length,
                    "duration": wave_duration
                })
                
                current_wave = (current_wave % 5) + 1
    
    # Analyze wave relationships
    wave_analysis = {
        "waves": waves,
        "pattern": "unknown",
        "confidence": 0.0
    }
    
    if len(waves) >= 5:
        # Basic Elliott Wave rules
        wave1_length = waves[0]['length'] if len(waves) > 0 else 0
        wave3_length = waves[2]['length'] if len(waves) > 2 else 0
        wave5_length = waves[4]['length'] if len(waves) > 4 else 0
        
        # Rule: Wave 3 is often the longest
        if wave3_length > wave1_length and wave3_length > wave5_length:
            wave_analysis["confidence"] += 0.3
        
        # Rule: Wave 4 should not overlap with Wave 1
        if len(waves) > 3:
            wave1_end = waves[0]['end_price']
            wave4_end = waves[3]['end_price']
            if (waves[0]['direction'] == 'up' and wave4_end > wave1_end) or \
               (waves[0]['direction'] == 'down' and wave4_end < wave1_end):
                wave_analysis["confidence"] += 0.2
        
        # Determine pattern
        if wave_analysis["confidence"] > 0.3:
            wave_analysis["pattern"] = "impulse"
        else:
            wave_analysis["pattern"] = "corrective"
    
    return wave_analysis

def ema(series, length):
    """Calculate Exponential Moving Average"""
    return series.ewm(span=length, adjust=False).mean()

def rsi(series, length=14):
    """Calculate Relative Strength Index"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def atr(high, low, close, length=14):
    """Calculate Average True Range"""
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=length).mean()

def bollinger_bands(series, length=20, std_dev=2):
    """Calculate Bollinger Bands"""
    sma = series.rolling(window=length).mean()
    std = series.rolling(window=length).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return sma, upper_band, lower_band

def adx(high, low, close, length=14):
    """Calculate Average Directional Index"""
    # True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Directional Movement
    dm_plus = high - high.shift()
    dm_minus = low.shift() - low
    dm_plus = dm_plus.where((dm_plus > dm_minus) & (dm_plus > 0), 0)
    dm_minus = dm_minus.where((dm_minus > dm_plus) & (dm_minus > 0), 0)
    
    # Smoothed values
    tr_smooth = tr.rolling(window=length).mean()
    dm_plus_smooth = dm_plus.rolling(window=length).mean()
    dm_minus_smooth = dm_minus.rolling(window=length).mean()
    
    # DI+ and DI-
    di_plus = 100 * (dm_plus_smooth / tr_smooth)
    di_minus = 100 * (dm_minus_smooth / tr_smooth)
    
    # DX and ADX
    dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
    adx = dx.rolling(window=length).mean()
    
    return adx, di_plus, di_minus

def obv(close, volume):
    """Calculate On Balance Volume"""
    obv = pd.Series(index=close.index, dtype=float)
    obv.iloc[0] = volume.iloc[0]
    
    for i in range(1, len(close)):
        if close.iloc[i] > close.iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] + volume.iloc[i]
        elif close.iloc[i] < close.iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] - volume.iloc[i]
        else:
            obv.iloc[i] = obv.iloc[i-1]
    
    return obv

def vwap(high, low, close, volume):
    """Calculate Volume Weighted Average Price"""
    typical_price = (high + low + close) / 3
    return (typical_price * volume).cumsum() / volume.cumsum()

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # EMAs
    df["ema_20"] = ema(df["close"], 20)
    df["ema_50"] = ema(df["close"], 50)
    df["ema_200"] = ema(df["close"], 200)
    
    # RSI
    df["rsi_14"] = rsi(df["close"], 14)
    
    # MACD
    macd_line, signal_line, histogram = macd(df["close"], 12, 26, 9)
    df["macd"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_hist"] = histogram
    
    # ATR
    df["atr_14"] = atr(df["high"], df["low"], df["close"], 14)
    
    # Bollinger Bands
    bb_mid, bb_up, bb_dn = bollinger_bands(df["close"], 20, 2.0)
    df["bb_mid"] = bb_mid
    df["bb_up"] = bb_up
    df["bb_dn"] = bb_dn
    df["bb_bw"] = (df["bb_up"] - df["bb_dn"]) / df["bb_mid"]
    
    # ADX (+DI/-DI)
    adx_val, di_plus, di_minus = adx(df["high"], df["low"], df["close"], 14)
    df["adx_14"] = adx_val
    df["di_plus"] = di_plus
    df["di_minus"] = di_minus
    
    # OBV
    df["obv"] = obv(df["close"], df["volume"])
    
    # VWAP
    try:
        df["vwap"] = vwap(df["high"], df["low"], df["close"], df["volume"])
    except Exception:
        df["vwap"] = None
    
    # Simple structure flags based on last two closed candles
    df["structure_hh"] = 0
    df["structure_hl"] = 0
    df["structure_lh"] = 0
    df["structure_ll"] = 0
    if len(df) >= 3:
        last = df.iloc[-2]
        prev = df.iloc[-3]
        if last["high"] > prev["high"]:
            df.loc[df.index[-2], "structure_hh"] = 1
        else:
            df.loc[df.index[-2], "structure_lh"] = 1
        if last["low"] > prev["low"]:
            df.loc[df.index[-2], "structure_hl"] = 1
        else:
            df.loc[df.index[-2], "structure_ll"] = 1
    
    return df

def last_closed_row(df: pd.DataFrame) -> pd.Series:
    if len(df) >= 2:
        return df.iloc[-2]
    return df.iloc[-1]

def build_snapshot(symbol: str, feature_map: Dict[str, pd.Series], dataframes: Dict[str, pd.DataFrame] = None) -> Dict[str, Any]:
    feat: Dict[str, Any] = {}
    def n(x):
        if x is None: return None
        if isinstance(x, float) and math.isnan(x): return None
        return float(x)
    
    for tf, s in feature_map.items():
        # Get the dataframe for this timeframe to calculate advanced indicators
        df = dataframes.get(tf) if dataframes else None
        
        if df is not None and len(df) > 0:
            # Calculate advanced indicators
            order_blocks = find_order_blocks(df)
            support_resistance = find_support_resistance_levels(df)
            
            # Find recent swing high and low for Fibonacci
            recent_high = df['high'].tail(50).max()
            recent_low = df['low'].tail(50).min()
            fib_retracements = fibonacci_retracements(recent_high, recent_low)
            
            # Elliott Wave analysis
            elliott_waves = identify_elliott_waves(df)
            
            feat[tf] = {
                "price": n(s.get("close")),
                "ema20": n(s.get("ema_20")), "ema50": n(s.get("ema_50")), "ema200": n(s.get("ema_200")),
                "rsi14": n(s.get("rsi_14")),
                "macd": {"val": n(s.get("macd")), "signal": n(s.get("macd_signal")), "hist": n(s.get("macd_hist"))},
                "atr14": n(s.get("atr_14")),
                "bb": {"mid": n(s.get("bb_mid")), "up": n(s.get("bb_up")), "dn": n(s.get("bb_dn")), "bw": n(s.get("bb_bw"))},
                "adx14": n(s.get("adx_14")),
                "di_plus": n(s.get("di_plus")),
                "di_minus": n(s.get("di_minus")),
                "obv": n(s.get("obv")),
                "vwap": n(s.get("vwap")),
                "structure": {
                    "hh": int(s.get("structure_hh") or 0),
                    "hl": int(s.get("structure_hl") or 0),
                    "lh": int(s.get("structure_lh") or 0),
                    "ll": int(s.get("structure_ll") or 0),
                },
                # Advanced indicators
                "order_blocks": {
                    "bullish": order_blocks["bullish"][-3:] if order_blocks["bullish"] else [],  # Last 3
                    "bearish": order_blocks["bearish"][-3:] if order_blocks["bearish"] else []   # Last 3
                },
                "support_resistance": {
                    "support": [float(x) for x in support_resistance["support"][:5]],  # Top 5 support levels
                    "resistance": [float(x) for x in support_resistance["resistance"][:5]]  # Top 5 resistance levels
                },
                "fibonacci": {
                    "retracements": {k: float(v) for k, v in fib_retracements.items()},
                    "recent_high": float(recent_high),
                    "recent_low": float(recent_low)
                },
                "elliott_waves": {
                    "pattern": elliott_waves["pattern"],
                    "confidence": float(elliott_waves["confidence"]),
                    "wave_count": len(elliott_waves["waves"]),
                    "current_wave": elliott_waves["waves"][-1] if elliott_waves["waves"] else None
                }
            }
        else:
            # Fallback to basic indicators if dataframe not available
            feat[tf] = {
                "price": n(s.get("close")),
                "ema20": n(s.get("ema_20")), "ema50": n(s.get("ema_50")), "ema200": n(s.get("ema_200")),
                "rsi14": n(s.get("rsi_14")),
                "macd": {"val": n(s.get("macd")), "signal": n(s.get("macd_signal")), "hist": n(s.get("macd_hist"))},
                "atr14": n(s.get("atr_14")),
                "bb": {"mid": n(s.get("bb_mid")), "up": n(s.get("bb_up")), "dn": n(s.get("bb_dn")), "bw": n(s.get("bb_bw"))},
                "adx14": n(s.get("adx_14")),
                "di_plus": n(s.get("di_plus")),
                "di_minus": n(s.get("di_minus")),
                "obv": n(s.get("obv")),
                "vwap": n(s.get("vwap")),
                "structure": {
                    "hh": int(s.get("structure_hh") or 0),
                    "hl": int(s.get("structure_hl") or 0),
                    "lh": int(s.get("structure_lh") or 0),
                    "ll": int(s.get("structure_ll") or 0),
                }
            }
    
    snapshot = {
        "symbol": symbol,
        "now": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
        "features": feat
    }
    return snapshot

def upsert_tables(symbol: str, tf: str, df_raw: pd.DataFrame, df_ind: pd.DataFrame):
    if not SUPABASE:
        return
    # Create tables if you want (not part of service to run DDL)
    # Upserts (chunked)
    rows_raw = []
    for _, r in df_raw.iterrows():
        rows_raw.append({
            "symbol": symbol, "tf": tf, "ts": r["ts"],
            "open": float(r["open"]), "high": float(r["high"]),
            "low": float(r["low"]), "close": float(r["close"]),
            "volume": float(r["volume"])
        })
    for i in range(0, len(rows_raw), 200):
        SUPABASE.table("ohlcv").upsert(rows_raw[i:i+200], on_conflict="symbol,tf,ts").execute()

    cols = ["ema_20","ema_50","ema_200","rsi_14","macd","macd_signal","macd_hist",
            "atr_14","bb_mid","bb_up","bb_dn","bb_bw","adx_14","di_plus","di_minus",
            "obv","vwap","structure_hh","structure_hl","structure_lh","structure_ll"]
    rows_ta = []
    for _, r in df_ind.iterrows():
        rec = {"symbol": symbol, "tf": tf, "ts": r["ts"]}
        for c in cols:
            val = r.get(c, None)
            if isinstance(val, float) and math.isnan(val):
                val = None
            if isinstance(val, (int,float)) and val is not None:
                val = float(val)
            rec[c] = val
        rows_ta.append(rec)
    for i in range(0, len(rows_ta), 200):
        SUPABASE.table("ta_features").upsert(rows_ta[i:i+200], on_conflict="symbol,tf,ts").execute()

# ---------- API ----------

@app.get("/v1/healthz")
def health():
    return {"ok": True, "ts": datetime.datetime.utcnow().isoformat() + "Z"}

@app.get("/v1/run")
def run(
    symbol: Optional[str] = Query(default=None),
    tfs: Optional[str] = Query(default=None, description="comma-separated TFs, e.g. 15m,1h,4h,1d"),
    lookback: Optional[int] = Query(default=None),
    category: Optional[str] = Query(default=None, description="bybit category: spot|linear|inverse")
):
    sym = symbol or ENV_SYMBOL
    tf_list = [s.strip() for s in (tfs or ",".join(ENV_TFS)).split(",") if s.strip()]
    lb = lookback or ENV_LOOKBACK
    cat = (category or ENV_CATEGORY).lower()

    feature_map: Dict[str, Any] = {}
    dataframes: Dict[str, pd.DataFrame] = {}

    for tf in tf_list:
        df = fetch_ohlcv_bybit(sym, tf, lb, cat)
        # compute indicators
        df_ind = df.copy()
        df_ind.index = pd.to_datetime(df_ind["ts"])
        df_ind = compute_indicators(df_ind)

        # Store dataframe for advanced analysis
        dataframes[tf] = df_ind

        # optional upsert to Supabase
        try:
            upsert_tables(sym, tf, df, df_ind)
        except Exception as e:
            print("[supabase] upsert failed:", e)

        # last closed row for snapshot
        s = df_ind.iloc[-2] if len(df_ind) >= 2 else df_ind.iloc[-1]
        feature_map[tf] = s

    snapshot = build_snapshot(sym, feature_map, dataframes)

    if WRITE_SNAPSHOT_JSON:
        try:
            with open("snapshot.json", "w") as f:
                json.dump(snapshot, f, indent=2)
        except Exception:
            pass

    return JSONResponse(snapshot)
