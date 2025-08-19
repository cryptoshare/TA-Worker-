
import os, math, json, uuid, datetime, requests
from typing import Dict, Any, List, Optional
import pandas as pd
import pandas_ta as ta
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

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # EMAs
    df["ema_20"] = ta.ema(df["close"], length=20)
    df["ema_50"] = ta.ema(df["close"], length=50)
    df["ema_200"] = ta.ema(df["close"], length=200)
    # RSI
    df["rsi_14"] = ta.rsi(df["close"], length=14)
    # MACD
    macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
    if macd is not None and not macd.empty:
        df["macd"] = macd["MACD_12_26_9"]
        df["macd_signal"] = macd["MACDs_12_26_9"]
        df["macd_hist"] = macd["MACDh_12_26_9"]
    # ATR
    df["atr_14"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    # Bollinger
    bb = ta.bbands(df["close"], length=20, std=2.0)
    if bb is not None and not bb.empty:
        df["bb_mid"] = bb["BBM_20_2.0"]
        df["bb_up"] = bb["BBU_20_2.0"]
        df["bb_dn"] = bb["BBL_20_2.0"]
        df["bb_bw"] = (df["bb_up"] - df["bb_dn"]) / df["bb_mid"]
    # ADX (+DI/-DI)
    adx = ta.adx(df["high"], df["low"], df["close"], length=14)
    if adx is not None and not adx.empty:
        df["adx_14"] = adx["ADX_14"]
        df["di_plus"] = adx["DMP_14"]
        df["di_minus"] = adx["DMN_14"]
    # OBV
    df["obv"] = ta.obv(df["close"], df["volume"])
    # VWAP (may be rolling if multi-day)
    try:
        df["vwap"] = ta.vwap(df["high"], df["low"], df["close"], df["volume"])
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

def build_snapshot(symbol: str, feature_map: Dict[str, pd.Series]) -> Dict[str, Any]:
    feat: Dict[str, Any] = {}
    def n(x):
        if x is None: return None
        if isinstance(x, float) and math.isnan(x): return None
        return float(x)
    for tf, s in feature_map.items():
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

    for tf in tf_list:
        df = fetch_ohlcv_bybit(sym, tf, lb, cat)
        # compute indicators
        df_ind = df.copy()
        df_ind.index = pd.to_datetime(df_ind["ts"])
        df_ind = compute_indicators(df_ind)

        # optional upsert to Supabase
        try:
            upsert_tables(sym, tf, df, df_ind)
        except Exception as e:
            print("[supabase] upsert failed:", e)

        # last closed row for snapshot
        s = df_ind.iloc[-2] if len(df_ind) >= 2 else df_ind.iloc[-1]
        feature_map[tf] = s

    snapshot = build_snapshot(sym, feature_map)

    if WRITE_SNAPSHOT_JSON:
        try:
            with open("snapshot.json", "w") as f:
                json.dump(snapshot, f, indent=2)
        except Exception:
            pass

    return JSONResponse(snapshot)
