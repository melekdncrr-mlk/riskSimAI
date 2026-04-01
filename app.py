import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(
    page_title="RiskSim AI · Profesyonel Yatırım Platformu",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
#  PREMIUM CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Backgrounds ── */
.stApp { background: #080C14 !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1321 0%, #0A0F1E 100%) !important;
    border-right: 1px solid rgba(56,139,253,0.15) !important;
}
[data-testid="stSidebar"] * { color: #A8B2C1 !important; }
[data-testid="stSidebar"] .stMarkdown h3 { color: #E2E8F0 !important; }

/* ── Typography ── */
h1 { font-size: 40px !important; font-weight: 900 !important; color: #F0F6FF !important; letter-spacing: -2px !important; }
h2 { font-size: 22px !important; font-weight: 700 !important; color: #E2E8F0 !important; letter-spacing: -0.5px !important; }
h3 { font-size: 16px !important; font-weight: 600 !important; color: #94A3B8 !important; }
p, span, div { color: #A8B2C1; }

/* ── Ticker Bar ── */
.ticker-bar {
    background: linear-gradient(90deg, #0D1321, #0F172A, #0D1321);
    border: 1px solid rgba(56,139,253,0.2);
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 24px;
    display: flex;
    gap: 28px;
    overflow-x: auto;
    scrollbar-width: none;
    align-items: center;
}
.ticker-bar::-webkit-scrollbar { display: none; }
.ticker-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 90px;
    gap: 2px;
}
.ticker-name { font-size: 10px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
.ticker-price { font-size: 14px; font-weight: 700; color: #F0F6FF; font-family: 'JetBrains Mono', monospace; }
.ticker-up { color: #10B981; font-size: 11px; font-weight: 600; }
.ticker-down { color: #EF4444; font-size: 11px; font-weight: 600; }
.ticker-flat { color: #64748B; font-size: 11px; font-weight: 600; }
.ticker-sep { width: 1px; height: 32px; background: rgba(56,139,253,0.15); flex-shrink: 0; }

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, rgba(56,139,253,0.08) 0%, rgba(16,185,129,0.04) 100%);
    border: 1px solid rgba(56,139,253,0.15);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(56,139,253,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,139,253,0.12);
    border: 1px solid rgba(56,139,253,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    color: #388BFD;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.subtitle {
    color: #64748B;
    font-size: 15px;
    font-weight: 400;
    margin-top: 6px;
}

/* ── Cards ── */
.glass-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(13,19,33,0.95) 100%);
    border: 1px solid rgba(56,139,253,0.12);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 14px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.glass-card:hover {
    border-color: rgba(56,139,253,0.3);
    transform: translateY(-1px);
    box-shadow: 0 8px 32px rgba(56,139,253,0.08);
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,139,253,0.3), transparent);
}

.winner-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(13,19,33,0.95) 80%);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.winner-card::after {
    content: '🏆';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 48px;
    opacity: 0.15;
}
.winner-label { font-size: 11px; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 1.5px; }
.winner-name { font-size: 28px; font-weight: 800; color: #F0F6FF; margin: 6px 0 4px; letter-spacing: -1px; }
.winner-stats { font-size: 13px; color: #64748B; }
.winner-stats b { color: #10B981; }

.insight-card {
    background: rgba(13,19,33,0.8);
    border: 1px solid rgba(56,139,253,0.1);
    border-left: 3px solid #388BFD;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 14px;
    color: #A8B2C1;
    line-height: 1.65;
}
.insight-card.green { border-left-color: #10B981; }
.insight-card.red   { border-left-color: #EF4444; }
.insight-card.gold  { border-left-color: #F59E0B; }

.section-label {
    font-size: 10px;
    font-weight: 700;
    color: #388BFD;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 16px 0 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(56,139,253,0.15);
}

/* ── Metric Cards ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(10,15,30,0.9));
    border: 1px solid rgba(56,139,253,0.12);
    border-radius: 12px;
    padding: 18px 20px;
    transition: all 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(56,139,253,0.35);
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(56,139,253,0.1);
}
div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    color: #F0F6FF !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: #64748B !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* ── Pulse Table ── */
.pulse-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px 0;
    border-bottom: 1px solid rgba(56,139,253,0.06);
}
.pulse-row:last-child { border-bottom: none; }
.pulse-name { font-weight: 600; font-size: 14px; color: #E2E8F0; display: flex; align-items: center; gap: 8px; }
.pulse-price { font-weight: 700; font-size: 15px; color: #F0F6FF; font-family: 'JetBrains Mono', monospace; }
.pulse-chg-up   { color: #10B981; font-size: 12px; font-weight: 600; background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 10px; }
.pulse-chg-down { color: #EF4444; font-size: 12px; font-weight: 600; background: rgba(239,68,68,0.1); padding: 2px 8px; border-radius: 10px; }
.pulse-chg-flat { color: #64748B; font-size: 12px; font-weight: 600; background: rgba(100,116,139,0.1); padding: 2px 8px; border-radius: 10px; }

/* ── Score Badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}
.score-pos { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.25); }
.score-neg { background: rgba(239,68,68,0.12); color: #EF4444; border: 1px solid rgba(239,68,68,0.2); }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: rgba(13,19,33,0.8);
    border: 1px solid rgba(56,139,253,0.12);
    border-radius: 10px;
    padding: 4px;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748B !important;
    font-size: 13px;
    font-weight: 600;
    padding: 10px 20px;
    border-radius: 7px;
    border: none !important;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: rgba(56,139,253,0.15) !important;
    color: #388BFD !important;
    border: none !important;
}

/* ── Button ── */
div.stButton > button {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(56,139,253,0.3) !important;
    padding: 14px 28px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    transition: all 0.25s ease !important;
    margin-top: 10px;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    box-shadow: 0 0 24px rgba(56,139,253,0.35) !important;
    transform: translateY(-2px) !important;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(56,139,253,0.15) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(56,139,253,0.5) !important;
    box-shadow: 0 0 0 2px rgba(56,139,253,0.1) !important;
}

hr { border-color: rgba(56,139,253,0.1) !important; margin: 24px 0; }
.stAlert { border-radius: 10px !important; border: 1px solid rgba(56,139,253,0.15) !important; }

/* ── Rec Comparison ── */
.rec-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.rec-card {
    background: rgba(13,19,33,0.9);
    border: 1px solid rgba(56,139,253,0.1);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    transition: all 0.2s;
}
.rec-card:hover { border-color: rgba(56,139,253,0.3); transform: translateY(-2px); }
.rec-card.best { border-color: rgba(16,185,129,0.4); background: rgba(16,185,129,0.05); }
.rec-card.worst { border-color: rgba(239,68,68,0.3); background: rgba(239,68,68,0.04); }
.rec-icon { font-size: 28px; margin-bottom: 6px; }
.rec-asset { font-size: 13px; font-weight: 700; color: #E2E8F0; }
.rec-pct { font-size: 20px; font-weight: 800; margin: 4px 0; font-family: 'JetBrains Mono', monospace; }
.rec-pct.pos { color: #10B981; }
.rec-pct.neg { color: #EF4444; }
.rec-meta { font-size: 11px; color: #64748B; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ASSET REGISTRY
# ══════════════════════════════════════════════════════════════
PULSE_ASSETS = [
    {"label": "Gram Altın",  "ticker": "_GRAMGOLD", "suffix": " ₺", "icon": "🥇"},
    {"label": "Ons Altın",   "ticker": "GC=F",      "suffix": " $", "icon": "✨"},
    {"label": "Gümüş",       "ticker": "SI=F",       "suffix": " $", "icon": "🥈"},
    {"label": "USD/TRY",     "ticker": "USDTRY=X",   "suffix": " ₺", "icon": "💵"},
    {"label": "EUR/TRY",     "ticker": "EURTRY=X",   "suffix": " ₺", "icon": "💶"},
    {"label": "BIST 100",    "ticker": "XU100.IS",   "suffix": "",   "icon": "📈"},
    {"label": "ASELSAN",     "ticker": "ASELS.IS",   "suffix": " ₺", "icon": "🎯"},
    {"label": "THY",         "ticker": "THYAO.IS",   "suffix": " ₺", "icon": "✈️"},
    {"label": "Garanti",     "ticker": "GARAN.IS",   "suffix": " ₺", "icon": "🏦"},
    {"label": "S&P 500",     "ticker": "^GSPC",      "suffix": "",   "icon": "🇺🇸"},
    {"label": "Bitcoin",     "ticker": "BTC-USD",    "suffix": " $", "icon": "₿"},
]

SIM_ASSETS = {
    "Gram Altın":   "_GRAMGOLD",
    "Ons Altın":    "GC=F",
    "Gümüş":        "SI=F",
    "USD/TRY":      "USDTRY=X",
    "EUR/TRY":      "EURTRY=X",
    "BIST 100":     "XU100.IS",
    "ASELSAN":      "ASELS.IS",
    "THY":          "THYAO.IS",
    "Garanti":      "GARAN.IS",
    "S&P 500":      "^GSPC",
    "Bitcoin":      "BTC-USD",
    "Ethereum":     "ETH-USD",
}

COMPARE_SET = ["_GRAMGOLD","GC=F","SI=F","USDTRY=X","EURTRY=X",
               "XU100.IS","ASELS.IS","THYAO.IS","GARAN.IS","BTC-USD"]

QUICK_COMPARE = [
    ("Gram Altın", "_GRAMGOLD", "🥇"),
    ("USD/TRY",    "USDTRY=X",  "💵"),
    ("ASELSAN",    "ASELS.IS",  "🎯"),
    ("BIST 100",   "XU100.IS",  "📈"),
    ("Bitcoin",    "BTC-USD",   "₿"),
]

def ticker_label(t: str) -> str:
    for a in PULSE_ASSETS:
        if a["ticker"] == t:
            return a["label"]
    for n, tick in SIM_ASSETS.items():
        if tick == t:
            return n
    return t

# ══════════════════════════════════════════════════════════════
#  DATA LAYER
# ══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False, ttl=1800)
def get_pulse():
    raw = [a["ticker"] for a in PULSE_ASSETS if a["ticker"] != "_GRAMGOLD"]
    result = {}
    for t in raw:
        try:
            fi = yf.Ticker(t).fast_info
            result[t] = {"price": fi["last_price"], "prev": fi.get("previous_close", fi["last_price"])}
        except Exception:
            result[t] = {"price": 0.0, "prev": 0.0}
    ons   = result.get("GC=F",     {}).get("price", 0)
    usd   = result.get("USDTRY=X", {}).get("price", 0)
    op    = result.get("GC=F",     {}).get("prev",  ons)
    up    = result.get("USDTRY=X", {}).get("prev",  usd)
    gram  = (ons*usd)/31.1034768      if ons and usd else 0
    gramp = (op*up)/31.1034768        if op  and up  else gram
    result["_GRAMGOLD"] = {"price": gram, "prev": gramp}
    return result

@st.cache_data(show_spinner=False, ttl=1800)
def fetch_history(tickers: list, years: int = 3):
    end   = datetime.today()
    start = end - timedelta(days=years*365)
    frames = {}
    real   = [t for t in tickers if t != "_GRAMGOLD"]
    for t in real:
        try:
            h = yf.Ticker(t).history(start=start, end=end)
            if "Close" in h.columns and not h.empty:
                # Normalize index to date-only (remove timezone)
                h.index = pd.to_datetime(h.index).tz_localize(None).normalize()
                frames[t] = h["Close"]
        except Exception:
            pass

    if not frames:
        return pd.DataFrame()

    # Align on common business-day index; forward-fill gaps up to 5 days
    data = pd.DataFrame(frames)
    data = data.ffill(limit=5)          # fill weekend/holiday gaps
    data = data.dropna(how="all")       # drop rows where EVERY column is NaN

    # Gram gold derived series
    if "_GRAMGOLD" in tickers and "GC=F" in data.columns and "USDTRY=X" in data.columns:
        gold_usd  = data["GC=F"].ffill()
        usd_try   = data["USDTRY=X"].ffill()
        data["_GRAMGOLD"] = (gold_usd * usd_try) / 31.1034768

    return data

# ══════════════════════════════════════════════════════════════
#  SMART ADVISOR ENGINE
# ══════════════════════════════════════════════════════════════
def score_assets(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if len(df) < 63:
        return pd.DataFrame()
    for col in df.columns:
        s = df[col].dropna()
        if len(s) < 63:
            continue
        ret_1m = (s.iloc[-1]/s.iloc[-21] - 1)*100
        ret_3m = (s.iloc[-1]/s.iloc[-63] - 1)*100
        ret_6m = (s.iloc[-1]/s.iloc[max(0,len(s)-126)] - 1)*100 if len(s)>=126 else ret_3m
        daily  = s.pct_change().dropna()
        vol    = daily.std() * np.sqrt(252) * 100
        mu_ann = daily.mean() * 252 * 100
        sharpe = mu_ann/vol if vol > 0 else 0
        max_dd = 0.0
        roll_max = s.cummax()
        dd_series = (s - roll_max)/roll_max * 100
        max_dd = dd_series.min()
        score  = 0.35*ret_1m + 0.30*ret_3m + 0.15*ret_6m + 20*sharpe
        rows.append({
            "Varlık":   ticker_label(col),
            "ticker":   col,
            "ret_1m":   ret_1m,
            "ret_3m":   ret_3m,
            "ret_6m":   ret_6m,
            "vol_ann":  vol,
            "sharpe":   sharpe,
            "max_dd":   max_dd,
            "score":    score,
        })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)

def advice_text(scores: pd.DataFrame, deposit_rate: float) -> list:
    if scores.empty:
        return [("blue", "Yeterli veri toplanamadı.")]
    out  = []
    best = scores.iloc[0]
    worst= scores.iloc[-1]
    out.append(("green",
        f"🏆 **{best['Varlık']}** bileşik skoruyla öne çıkıyor. "
        f"Son 1 ay **%{best['ret_1m']:.1f}** · Son 3 ay **%{best['ret_3m']:.1f}** getiri."
    ))
    out.append(("red",
        f"⚠️ **{worst['Varlık']}** en düşük performansı gösterdi "
        f"(1A: %{worst['ret_1m']:.1f} | 3A: %{worst['ret_3m']:.1f})."
    ))
    monthly_bench = deposit_rate/12
    beat = scores[scores["ret_1m"] > monthly_bench]
    if not beat.empty:
        names = ", ".join(beat["Varlık"].tolist()[:4])
        out.append(("gold", f"💰 Aylık mevduat faizini (%{monthly_bench:.1f}) geçen varlıklar: **{names}**."))
    else:
        out.append(("blue", f"🏦 Bu dönemde hiçbir varlık aylık mevduat faizini (%{monthly_bench:.1f}) geçemedi."))

    has_usd  = "USDTRY=X" in scores["ticker"].values
    has_gold = scores["ticker"].isin(["_GRAMGOLD","GC=F"]).any()
    has_asel = "ASELS.IS" in scores["ticker"].values
    if has_usd and has_gold:
        ur = scores[scores["ticker"]=="USDTRY=X"].iloc[0]
        gr = scores[scores["ticker"].isin(["_GRAMGOLD","GC=F"])].iloc[0]
        if gr["ret_1m"] > ur["ret_1m"]:
            out.append(("gold", f"🥇 Altın, Dolar'ı geride bıraktı: Altın %{gr['ret_1m']:.1f} vs Dolar/TL %{ur['ret_1m']:.1f}."))
        else:
            out.append(("blue", f"💵 Dolar, Altın'ı geride bıraktı: USD/TRY %{ur['ret_1m']:.1f} vs Altın %{gr['ret_1m']:.1f}."))
    if has_asel:
        ar = scores[scores["ticker"]=="ASELS.IS"].iloc[0]
        rank = int(scores[scores["ticker"]=="ASELS.IS"].index[0]) + 1
        out.append(("blue", f"🎯 **ASELSAN** {len(scores)} varlık arasında **{rank}. sıraya** girdi (1A: %{ar['ret_1m']:.1f})."))

    high_vol = scores[scores["vol_ann"] > 60]
    if not high_vol.empty:
        names = ", ".join(high_vol["Varlık"].tolist())
        out.append(("red", f"🌊 Yüksek volatilite uyarısı: **{names}** — yıllık %{high_vol['vol_ann'].mean():.0f}+ oynaklık."))
    return out

# ══════════════════════════════════════════════════════════════
#  MONTE CARLO
# ══════════════════════════════════════════════════════════════
def run_monte_carlo(capital, years, mu, sigma, profile):
    mult = {"Defansif": (0.90, 0.82), "Dengeli": (1.0, 1.0), "Agresif": (1.15, 1.25)}
    rm, rs = mult.get(profile, (1.0, 1.0))
    mu *= rm; sigma *= rs
    N = 10_000
    paths = np.zeros((years+1, N))
    paths[0] = capital
    for t in range(1, years+1):
        Z = np.random.standard_normal(N)
        paths[t] = paths[t-1] * np.exp((mu - 0.5*sigma**2) + sigma*Z)
    return paths, paths[-1], mu, sigma

# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():

    # ── HEADER ──
    st.markdown("""
    <div class="main-header">
        <div class="brand-badge">⚡ LIVE · AI-POWERED</div>
        <h1>RiskSim AI</h1>
        <div class="subtitle">Gerçek Zamanlı Piyasa Analizi &nbsp;·&nbsp; Akıllı Karar Motoru &nbsp;·&nbsp; Monte Carlo Simülasyonu</div>
    </div>
    """, unsafe_allow_html=True)

    # ── LIVE TICKER BAR ──
    with st.spinner(""):
        pulse = get_pulse()

    bar_items = ""
    for i, a in enumerate(PULSE_ASSETS):
        t = a["ticker"]
        info = pulse.get(t, {"price": 0, "prev": 0})
        price = info["price"]
        prev  = info["prev"]
        chg   = ((price-prev)/prev*100) if prev else 0
        if chg > 0.05:
            chg_cls, arrow = "ticker-up", "▲"
        elif chg < -0.05:
            chg_cls, arrow = "ticker-down", "▼"
        else:
            chg_cls, arrow = "ticker-flat", "—"
        bar_items += f"""
        <div class="ticker-item">
            <span class="ticker-name">{a['icon']} {a['label']}</span>
            <span class="ticker-price">{price:,.2f}{a['suffix']}</span>
            <span class="{chg_cls}">{arrow} {abs(chg):.2f}%</span>
        </div>
        """
        if i < len(PULSE_ASSETS)-1:
            bar_items += '<div class="ticker-sep"></div>'

    st.markdown(f'<div class="ticker-bar">{bar_items}</div>', unsafe_allow_html=True)

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown("<div class='section-label'>Yatırımcı Profili</div>", unsafe_allow_html=True)
        age = st.number_input("Yaşınız", 18, 100, 30)
        risk_profile = st.selectbox(
            "Risk Profili", ["Defansif","Dengeli","Agresif"], index=1,
            help="Defansif: Sermaye koruma öncelikli. Dengeli: Orta yol. Agresif: Büyüme öncelikli."
        )
        capital = st.number_input("Başlangıç Sermayesi (₺)", 1_000, 1_000_000_000, 100_000, step=10_000)
        duration = st.slider("Yatırım Vadesi (Yıl)", 1, 30, 5)
        deposit_rate = st.slider("Yıllık Mevduat Faizi (%)", 10, 70, 45,
                                 help="Risksiz getiri karşılaştırması için referans oran.")
        hist_years = st.slider("Gerçek Veri Geçmişi (Yıl)", 1, 10, 3)

        st.markdown("<div class='section-label'>Portföy Dağılımı</div>", unsafe_allow_html=True)
        selected = st.multiselect(
            "Simülasyon Varlıkları", list(SIM_ASSETS.keys()),
            default=["Gram Altın","BIST 100","USD/TRY","ASELSAN"]
        )
        custom_raw = st.text_input("Özel Sembol Ekle", placeholder="Örn: NVDA, GARAN.IS, SASA.IS")

        active_tickers = [SIM_ASSETS[n] for n in selected]
        if custom_raw.strip():
            for s in custom_raw.split(","):
                s = s.strip().upper()
                if s: active_tickers.append(s)
        active_tickers = list(dict.fromkeys(active_tickers))

        weights = []
        if active_tickers:
            st.markdown("<div class='section-label' style='margin-top:14px;'>Ağırlıklar (%)</div>", unsafe_allow_html=True)
            total_w = 0.0
            def_w = round(100.0/len(active_tickers), 1)
            for t in active_tickers:
                lbl = ticker_label(t)
                w = st.number_input(lbl, 0.0, 100.0, def_w, 1.0, key=f"w_{t}")
                weights.append(w); total_w += w
            if abs(total_w - 100.0) > 0.1:
                st.error(f"Toplam %100 olmalı. Şu an: %{total_w:.1f}")
                st.stop()
        else:
            st.warning("En az bir varlık seçiniz.")
            st.stop()

        run_btn = st.button("🚀  SİMÜLASYONU BAŞLAT")

    # ── TABS ──
    tab_pulse, tab_advisor, tab_sim = st.tabs([
        "📡  Canlı Piyasa Nabzı",
        "🧠  Akıllı Karar Tavsiyesi",
        "📈  Portföy Simülasyonu",
    ])

    # ══════════════════════════════════════════
    #  TAB 1 — MARKET PULSE
    # ══════════════════════════════════════════
    with tab_pulse:
        st.markdown("<h2>Güncel Piyasa Fiyatları</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B;margin-top:-6px;margin-bottom:20px;'>Yahoo Finance · Otomatik Güncelleme</p>", unsafe_allow_html=True)

        priority_order = ["_GRAMGOLD","USDTRY=X","EURTRY=X","GC=F","XU100.IS","BTC-USD"]
        top5 = [a for a in PULSE_ASSETS if a["ticker"] in priority_order][:6]
        cols = st.columns(len(top5))
        for col, asset in zip(cols, top5):
            t = asset["ticker"]
            info  = pulse.get(t, {"price":0,"prev":0})
            price = info["price"]; prev = info["prev"]
            delta = ((price-prev)/prev*100) if prev else 0
            col.metric(f"{asset['icon']} {asset['label']}", f"{price:,.2f}{asset['suffix']}", f"{delta:+.2f}%")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2>Tüm İzlenen Varlıklar</h2>", unsafe_allow_html=True)

        rows_html = ""
        for asset in PULSE_ASSETS:
            t = asset["ticker"]
            info = pulse.get(t, {"price":0,"prev":0})
            price = info["price"]; prev = info["prev"]
            chg = ((price-prev)/prev*100) if prev else 0
            if chg > 0.05:
                cls, arrow = "pulse-chg-up",   f"▲ {chg:+.2f}%"
            elif chg < -0.05:
                cls, arrow = "pulse-chg-down", f"▼ {chg:.2f}%"
            else:
                cls, arrow = "pulse-chg-flat", f"— {chg:.2f}%"
            rows_html += f"""
            <div class="pulse-row">
                <span class="pulse-name">{asset['icon']} {asset['label']}</span>
                <span class="pulse-price">{price:,.2f}{asset['suffix']}</span>
                <span class="{cls}">{arrow}</span>
            </div>"""

        st.markdown(f'<div class="glass-card">{rows_html}</div>', unsafe_allow_html=True)

        # Mini performance chart (30-day)
        st.markdown("<h2>30 Günlük Performans Karşılaştırması</h2>", unsafe_allow_html=True)
        with st.spinner("Grafik yükleniyor..."):
            chart_tickers = ["_GRAMGOLD","USDTRY=X","XU100.IS","BTC-USD","ASELS.IS"]
            df_chart = fetch_history(chart_tickers, years=1)
        if not df_chart.empty:
            df30 = df_chart.tail(30)
            norm = (df30 / df30.iloc[0] * 100)
            ren  = {t: ticker_label(t) for t in norm.columns}
            norm = norm.rename(columns=ren)
            fig = px.line(norm, labels={"value":"Başlangıç=100","index":"Tarih","variable":"Varlık"})
            fig.update_layout(
                template="plotly_dark", height=380,
                paper_bgcolor="#0A0F1E", plot_bgcolor="#080C14",
                margin=dict(l=10,r=10,t=10,b=10),
                legend=dict(font=dict(color="#A8B2C1",size=12), bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                yaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
            )
            fig.update_traces(line=dict(width=2.5))
            st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════
    #  TAB 2 — SMART ADVISOR
    # ══════════════════════════════════════════
    with tab_advisor:
        st.markdown("<h2>Akıllı Karşılaştırma & Tavsiye Motoru</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B;margin-top:-6px;margin-bottom:20px;'>Altın mı, Dolar mı, ASELSAN mı? Gerçek verilerle puanlı analiz.</p>", unsafe_allow_html=True)

        with st.spinner("Varlıklar analiz ediliyor..."):
            df_adv = fetch_history(COMPARE_SET, years=hist_years)

        if df_adv.empty:
            st.error("Yeterli veri alınamadı.")
        else:
            scores = score_assets(df_adv)

            if not scores.empty:
                # ── Quick Comparison: Gold vs USD vs ASELSAN ──
                st.markdown("<div class='section-label'>Hızlı Karşılaştırma</div>", unsafe_allow_html=True)

                qc_html = '<div class="rec-grid">'
                for i, (name, tick, icon) in enumerate(QUICK_COMPARE[:3]):
                    row = scores[scores["ticker"]==tick]
                    if row.empty:
                        continue
                    r = row.iloc[0]
                    rank = int(row.index[0]) + 1
                    is_best  = rank == 1
                    is_worst = rank == len(scores)
                    cls = "rec-card best" if is_best else ("rec-card worst" if is_worst else "rec-card")
                    pct_cls = "pos" if r["ret_1m"] >= 0 else "neg"
                    crown = " 👑" if is_best else ""
                    qc_html += f"""
                    <div class="{cls}">
                        <div class="rec-icon">{icon}</div>
                        <div class="rec-asset">{name}{crown}</div>
                        <div class="rec-pct {pct_cls}">{r['ret_1m']:+.1f}%</div>
                        <div class="rec-meta">Son 1 ay · Skor: {r['score']:.1f}</div>
                        <div class="rec-meta">Volatilite: %{r['vol_ann']:.1f}</div>
                    </div>"""
                qc_html += '</div>'
                st.markdown(qc_html, unsafe_allow_html=True)

                # ── Winner Card ──
                w = scores.iloc[0]
                st.markdown(f"""
                <div class="winner-card">
                    <div class="winner-label">📊 Şu An En Güçlü Varlık</div>
                    <div class="winner-name">{w['Varlık']}</div>
                    <div class="winner-stats">
                        1 Aylık: <b>%{w['ret_1m']:.1f}</b> &nbsp;|&nbsp;
                        3 Aylık: <b>%{w['ret_3m']:.1f}</b> &nbsp;|&nbsp;
                        Sharpe: <b>{w['sharpe']:.2f}</b> &nbsp;|&nbsp;
                        Bileşik Puan: <b>{w['score']:.1f}</b>
                    </div>
                </div>""", unsafe_allow_html=True)

                # ── AI Insights ──
                st.markdown("<div class='section-label'>Analist Görüşleri</div>", unsafe_allow_html=True)
                for color, text in advice_text(scores, deposit_rate):
                    st.markdown(f'<div class="insight-card {color}">{text}</div>', unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)

                # ── Full Ranking Table ──
                st.markdown("<h2>Tam Karşılaştırma Tablosu</h2>", unsafe_allow_html=True)
                disp = scores[["Varlık","ret_1m","ret_3m","ret_6m","vol_ann","sharpe","max_dd","score"]].copy()
                disp.columns = ["Varlık","1A Getiri (%)","3A Getiri (%)","6A Getiri (%)","Yıllık Vol (%)","Sharpe","Max DD (%)","Bileşik Puan"]
                disp = disp.set_index("Varlık")

                styled = (
                    disp.style
                        .format("{:.2f}")
                        .background_gradient(subset=["1A Getiri (%)", "3A Getiri (%)", "Bileşik Puan"], cmap="RdYlGn")
                )
                st.dataframe(styled, width="stretch", height=min(55+38*len(disp), 550))

                st.markdown("<hr>", unsafe_allow_html=True)

                # ── Normalized chart ──
                st.markdown("<h2>Tarihsel Performans Kıyaslaması</h2>", unsafe_allow_html=True)
                cols_in = [t for t in COMPARE_SET if t in df_adv.columns]
                norm = (df_adv[cols_in] / df_adv[cols_in].iloc[0] * 100)
                norm = norm.rename(columns={t: ticker_label(t) for t in cols_in})
                fig2 = px.line(norm, labels={"value":"Başlangıç=100","index":"Tarih","variable":"Varlık"})
                fig2.update_layout(
                    template="plotly_dark", height=460,
                    paper_bgcolor="#0A0F1E", plot_bgcolor="#080C14",
                    margin=dict(l=10,r=10,t=10,b=10),
                    legend=dict(font=dict(color="#A8B2C1",size=12), bgcolor="rgba(0,0,0,0)"),
                    xaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                    yaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                )
                fig2.update_traces(line=dict(width=2))
                st.plotly_chart(fig2, use_container_width=True)

    # ══════════════════════════════════════════
    #  TAB 3 — MONTE CARLO
    # ══════════════════════════════════════════
    with tab_sim:
        st.markdown("<h2>Portföy Simülasyonu (Monte Carlo)</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:#64748B;margin-top:-6px;margin-bottom:20px;'>"
            f"10.000 paralel senaryo · Geometrik Brownian Hareketi · Gerçek {hist_years} yıllık veri</p>",
            unsafe_allow_html=True
        )

        if run_btn:
            with st.spinner("Tarihsel veriler çekiliyor ve simülasyon hesaplanıyor..."):
                df_sim = fetch_history(active_tickers, years=hist_years)

                # ── Fallback defaults when no real data is available ──
                FALLBACK_PARAMS = {
                    "_GRAMGOLD": (0.35, 0.25), "GC=F": (0.12, 0.15),
                    "SI=F":      (0.10, 0.28), "USDTRY=X": (0.40, 0.10),
                    "EURTRY=X": (0.38, 0.10), "XU100.IS": (0.55, 0.30),
                    "ASELS.IS": (0.60, 0.35), "THYAO.IS": (0.50, 0.40),
                    "GARAN.IS": (0.45, 0.35), "^GSPC":    (0.12, 0.18),
                    "BTC-USD":  (0.50, 0.80), "ETH-USD":  (0.45, 0.90),
                }

                w_arr     = np.array(weights) / 100.0
                available = [t for t in active_tickers if t in df_sim.columns]
                missing   = [t for t in active_tickers if t not in df_sim.columns]

                if missing:
                    st.warning(f"Şu semboller için gerçek veri bulunamadı, tahmini parametreler kullanılıyor: {[ticker_label(m) for m in missing]}")

                if not available:
                    # Full fallback — no real data at all
                    st.info("Bağlantı sorunu nedeniyle gerçek veri çekilemedi. Sektör ortalaması parametreleriyle simülasyon çalıştırılıyor.")
                    mu_parts    = [FALLBACK_PARAMS.get(t, (0.20, 0.25))[0] for t in active_tickers]
                    sig_parts   = [FALLBACK_PARAMS.get(t, (0.20, 0.25))[1] for t in active_tickers]
                    mu_p  = float(np.dot(w_arr, mu_parts))
                    sig_p = float(np.dot(w_arr, sig_parts))
                else:
                    df_av = df_sim[available].copy()
                    # Make sure we don't drop everything if overlaps are sparse
                    # For metrics calculation, we use the available returns per asset
                    rets_all = df_av.pct_change().dropna(how="all")

                    # Weights for available tickers only
                    idx_avail = [active_tickers.index(t) for t in available]
                    w_av      = w_arr[idx_avail]
                    w_av      = w_av / w_av.sum()

                    # Portfolio Mu & Sig
                    # Use individual means instead of dropping entire rows for mu
                    mu_v  = rets_all.mean() * 252
                    # Covariance needs overlapping pairs - we ffill slightly for more stable cov estimation
                    cov_m = df_av.ffill(limit=3).pct_change().cov() * 252

                    mu_p  = float(np.dot(w_av, mu_v.values))
                    var_p = float(np.dot(w_av, np.dot(cov_m.values, w_av)))
                    sig_p = float(np.sqrt(max(var_p, 1e-8)))

                    # Blend in fallback mu/sigma for missing tickers
                    if missing:
                        miss_w   = w_arr[[active_tickers.index(t) for t in missing]].sum()
                        fb_mu    = np.mean([FALLBACK_PARAMS.get(t,(0.20,0.25))[0] for t in missing])
                        fb_sig   = np.mean([FALLBACK_PARAMS.get(t,(0.20,0.25))[1] for t in missing])
                        mu_p     = (1-miss_w)*mu_p  + miss_w*fb_mu
                        sig_p    = (1-miss_w)*sig_p + miss_w*fb_sig

                paths, final_w, mu_adj, sig_adj = run_monte_carlo(capital, duration, mu_p, sig_p, risk_profile)

            # Portfolio params
            st.markdown("<div class='section-label'>Gerçek Veri Tabanlı Portföy Parametreleri</div>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Beklenen Yıllık Getiri", f"%{mu_p*100:.2f}")
            c2.metric("Yıllık Volatilite",      f"%{sig_p*100:.2f}")
            c3.metric("Sharpe (tahmini)",        f"{(mu_p/sig_p if sig_p>0 else 0):.2f}")
            c4.metric("Risk Profili",             risk_profile)

            st.markdown("<hr>", unsafe_allow_html=True)

            # Results
            avg_w          = np.mean(final_w)
            p5,p10,p50,p90 = (np.percentile(final_w,q) for q in [5,10,50,90])
            var95          = max(0, capital-p5)
            loss_p         = np.mean(final_w < capital)*100
            dep_value      = capital * ((1+deposit_rate/100)**duration)

            st.markdown(f"<h2>{duration} Yıllık Projeksiyon Sonuçları</h2>", unsafe_allow_html=True)
            r1,r2,r3,r4 = st.columns(4)
            r1.metric("Medyan Senaryo",     f"{p50:,.0f} ₺", f"{(p50/capital-1)*100:+.1f}%")
            r2.metric("Ortalama Beklenti",  f"{avg_w:,.0f} ₺", f"{(avg_w/capital-1)*100:+.1f}%")
            r3.metric("Kötü Senaryo (%10)", f"{p10:,.0f} ₺", f"{(p10/capital-1)*100:+.1f}%")
            r4.metric("İyi Senaryo (%90)",  f"{p90:,.0f} ₺", f"{(p90/capital-1)*100:+.1f}%")

            vs = "üzerinde" if p50 > dep_value else "altında"
            st.info(
                f"**Risk Özeti:** Zarar ihtimali **%{loss_p:.1f}** · VaR %95 → **{var95:,.0f} ₺** potansiyel kayıp · "
                f"Medyan beklenti mevduat değerinin (**{dep_value:,.0f} ₺**) **{vs}**."
            )

            st.markdown("<hr>", unsafe_allow_html=True)

            col_h, col_p = st.columns([1,1])

            with col_h:
                st.markdown("<h2>Nihai Servet Dağılımı</h2>", unsafe_allow_html=True)
                fig_h = go.Figure()
                fig_h.add_trace(go.Histogram(
                    x=final_w, nbinsx=120,
                    marker_color="#1D4ED8", opacity=0.75,
                    marker=dict(line=dict(width=0))
                ))
                fig_h.add_vline(x=capital,   line_width=1.5, line_dash="dash", line_color="#EF4444",
                                annotation_text="Başlangıç", annotation_font_color="#EF4444")
                fig_h.add_vline(x=p50,       line_width=1.5, line_dash="dash", line_color="#10B981",
                                annotation_text="Medyan",    annotation_font_color="#10B981")
                fig_h.add_vline(x=dep_value, line_width=1.5, line_dash="dot",  line_color="#F59E0B",
                                annotation_text="Mevduat",   annotation_font_color="#F59E0B")
                fig_h.update_layout(
                    template="plotly_dark", height=380, bargap=0.04,
                    paper_bgcolor="#0A0F1E", plot_bgcolor="#080C14",
                    margin=dict(l=10,r=10,t=20,b=10),
                    xaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                    yaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                )
                st.plotly_chart(fig_h, use_container_width=True)

            with col_p:
                st.markdown("<h2>200 Örnek Senaryo</h2>", unsafe_allow_html=True)
                df_paths = pd.DataFrame(paths[:,:200], index=range(duration+1))
                fig_p    = px.line(df_paths, labels={"index":"Yıl","value":"Servet (₺)","variable":"Senaryo"})
                fig_p.update_traces(line=dict(color="#1D4ED8", width=1), opacity=0.06)
                fig_p.add_hline(y=capital,   line_width=1.5, line_dash="dash", line_color="#EF4444")
                fig_p.add_hline(y=dep_value, line_width=1.2, line_dash="dot",  line_color="#F59E0B")
                fig_p.update_layout(
                    template="plotly_dark", height=380, showlegend=False,
                    paper_bgcolor="#0A0F1E", plot_bgcolor="#080C14",
                    margin=dict(l=10,r=10,t=20,b=10),
                    xaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                    yaxis=dict(gridcolor="rgba(56,139,253,0.06)"),
                )
                st.plotly_chart(fig_p, use_container_width=True)

            # Percentile fan
            st.markdown("<h2>Güven Bantları (Senaryo Aralıkları)</h2>", unsafe_allow_html=True)
            fig_fan = go.Figure()
            years_arr = np.arange(duration+1)
            for q_lo, q_hi, alpha, name in [(5,95,0.12,"P5–P95"),(10,90,0.18,"P10–P90"),(25,75,0.28,"P25–P75")]:
                y_lo = np.percentile(paths, q_lo, axis=1)
                y_hi = np.percentile(paths, q_hi, axis=1)
                fig_fan.add_trace(go.Scatter(
                    x=np.concatenate([years_arr, years_arr[::-1]]),
                    y=np.concatenate([y_hi, y_lo[::-1]]),
                    fill='toself', fillcolor=f'rgba(29,78,216,{alpha})',
                    line=dict(color='rgba(0,0,0,0)'), name=name
                ))
            fig_fan.add_trace(go.Scatter(
                x=years_arr, y=np.percentile(paths, 50, axis=1),
                line=dict(color="#10B981", width=2.5), name="Medyan"
            ))
            fig_fan.add_hline(y=capital, line_width=1.5, line_dash="dash", line_color="#EF4444",
                              annotation_text="Başlangıç", annotation_font_color="#EF4444")
            fig_fan.update_layout(
                template="plotly_dark", height=420,
                paper_bgcolor="#0A0F1E", plot_bgcolor="#080C14",
                margin=dict(l=10,r=10,t=20,b=10),
                legend=dict(font=dict(color="#A8B2C1"), bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(title="Yıl", gridcolor="rgba(56,139,253,0.06)"),
                yaxis=dict(title="Servet (₺)", gridcolor="rgba(56,139,253,0.06)"),
            )
            st.plotly_chart(fig_fan, use_container_width=True)

        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding: 70px 40px;">
                <div style="font-size:56px; margin-bottom:16px; opacity:0.7;">📊</div>
                <h2 style="color:#E2E8F0; font-size:24px !important; margin-bottom:12px;">Simülasyona hazır.</h2>
                <p style="color:#64748B; max-width:520px; margin:0 auto; line-height:1.7; font-size:15px;">
                    Sol menüden parametrelerinizi ve varlık ağırlıklarınızı belirleyin, ardından
                    <b style='color:#388BFD;'>Simülasyonu Başlat</b> butonuna tıklayın.<br><br>
                    Sistem gerçek tarihsel korelasyon matrislerini kullanarak
                    <b style='color:#388BFD;'>10.000 paralel senaryoyu</b> hesaplayacak.
                </p>
            </div>""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
