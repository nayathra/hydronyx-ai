import streamlit as st
import random
import time
import requests
from datetime import datetime, timedelta

# ── Backend API ───────────────────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000/latest"

def fetch_backend_data():
    try:
        res = requests.get(API_URL, timeout=3)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            return {
                "water_level":  data.get("water_level",  0),
                "rain":         data.get("rain",         0),
                "temperature":  data.get("temperature",  0),
                "humidity":     data.get("humidity",     0),
            }
    except Exception as e:
        print("Backend error:", e)
    return None

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hydronyx · Coastal Risk Detection",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Root & Reset ── */
:root {
    --bg:       #060d18;
    --surface:  #0c1628;
    --border:   #1a2d4a;
    --text:     #e2ecf7;
    --muted:    #5a7a9a;
    --accent:   #00c8ff;
    --low:      #00e5a0;
    --med:      #ff9d2e;
    --high:     #ff3b5c;
    --glow-low: rgba(0,229,160,.25);
    --glow-med: rgba(255,157,46,.25);
    --glow-hig: rgba(255,59,92,.25);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Mono', monospace;
    color: var(--text);
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(0,200,255,.08) 0%, transparent 70%),
        radial-gradient(ellipse 60% 30% at 80% 110%, rgba(0,120,220,.06) 0%, transparent 70%),
        var(--bg) !important;
}

/* hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Typography ── */
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

/* ── Header ── */
.hdr {
    text-align: center;
    padding: 1.4rem 1rem 0.8rem;
    position: relative;
}
.hdr-wave {
    font-size: 3.4rem;
    display: block;
    margin-bottom: .4rem;
    animation: bob 3.2s ease-in-out infinite;
}
@keyframes bob {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
.hdr-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: .06em;
    color: var(--accent);
    text-shadow: 0 0 28px rgba(0,200,255,.45);
    margin: 0;
    line-height: 1.1;
}
.hdr-sub {
    font-size: .78rem;
    color: var(--muted);
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-top: .4rem;
}
.hdr-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), var(--accent), var(--border), transparent);
    margin: 1.4rem auto 0;
    max-width: 520px;
}

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem 1.2rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,200,255,.03) 0%, transparent 60%);
    pointer-events: none;
}
.card-label {
    font-family: 'Syne', sans-serif;
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: .45rem;
}

/* ── Risk badge ── */
.risk-wrap {
    text-align: center;
    padding: .8rem 0;
}
.risk-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: .12em;
    padding: .55rem 2.4rem;
    border-radius: 12px;
    border: 2px solid currentColor;
    margin-bottom: .7rem;
    transition: all .4s ease;
}
.risk-LOW  { color: var(--low);  box-shadow: 0 0 32px var(--glow-low), inset 0 0 24px rgba(0,229,160,.08); }
.risk-MED  { color: var(--med);  box-shadow: 0 0 32px var(--glow-med), inset 0 0 24px rgba(255,157,46,.08); }
.risk-HIGH { color: var(--high); box-shadow: 0 0 32px var(--glow-hig), inset 0 0 24px rgba(255,59,92,.08);  animation: pulse 1s ease-in-out infinite; }
@keyframes pulse {
    0%,100% { box-shadow: 0 0 32px var(--glow-hig), inset 0 0 24px rgba(255,59,92,.08); }
    50%      { box-shadow: 0 0 56px var(--glow-hig), inset 0 0 40px rgba(255,59,92,.14); }
}

/* ── Alert banner ── */
.alert {
    border-radius: 10px;
    padding: .9rem 1.2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: .04em;
    display: flex;
    align-items: center;
    gap: .7rem;
    margin-top: .6rem;
}
.alert-LOW  { background: rgba(0,229,160,.1);  border: 1px solid rgba(0,229,160,.35);  color: var(--low); }
.alert-MED  { background: rgba(255,157,46,.1); border: 1px solid rgba(255,157,46,.35); color: var(--med); }
.alert-HIGH { background: rgba(255,59,92,.12); border: 1px solid rgba(255,59,92,.45);  color: var(--high); animation: flash-border 1.2s ease-in-out infinite; }
@keyframes flash-border {
    0%,100% { border-color: rgba(255,59,92,.45); }
    50%      { border-color: rgba(255,59,92,.9); }
}

/* ── Metric row ── */
.metrics {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 1.2rem;
}
.metric {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem .8rem;
    text-align: center;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-lbl {
    font-size: .65rem;
    color: var(--muted);
    letter-spacing: .15em;
    text-transform: uppercase;
    margin-top: .25rem;
}

/* ── Water level bar ── */
.wl-bar-wrap {
    background: rgba(0,0,0,.3);
    border-radius: 8px;
    height: 14px;
    margin: .6rem 0 .3rem;
    overflow: hidden;
    border: 1px solid var(--border);
}
.wl-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width .5s ease, background .5s ease;
}
.wl-bar-label {
    font-size: .7rem;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
    margin-top: .2rem;
}

/* ── Timeline chart ── */
.timeline-title {
    font-family: 'Syne', sans-serif;
    font-size: .68rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .9rem;
}
svg.chart { width: 100%; height: 100px; display: block; }

/* ── Streamlit widget overrides ── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}
[data-testid="stSlider"] > div > div > div {
    background: var(--border) !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    color: var(--muted) !important;
    font-size: .8rem !important;
    letter-spacing: .1em !important;
}
[data-testid="stCheckbox"] label p {
    font-family: 'DM Mono', monospace !important;
    color: var(--text) !important;
}
/* timestamp */
.ts {
    font-size: .68rem;
    color: var(--muted);
    text-align: right;
    margin-top: -.4rem;
    margin-bottom: .8rem;
    letter-spacing: .08em;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_risk(water_level: int, raining: bool, humidity: int = 0) -> str:
    score = water_level
    if raining:
        score += 20
    if humidity > 80:
        score += 10

    prev = st.session_state.get("last_risk", "LOW")

    # Stability thresholds (hysteresis — prevents flickering)
    if prev == "HIGH":
        new = "MEDIUM" if score < 75 else "HIGH"
    elif prev == "MEDIUM":
        if score >= 90:
            new = "HIGH"
        elif score < 45:
            new = "LOW"
        else:
            new = "MEDIUM"
    else:  # LOW
        new = "MEDIUM" if score >= 60 else "LOW"

    st.session_state.last_risk = new
    return new


def bar_color(level: int) -> str:
    if level >= 70:
        return "#ff3b5c"
    elif level >= 40:
        return "#ff9d2e"
    return "#00c8ff"


def sparkline_svg(points: list[int]) -> str:
    """Render a minimal SVG sparkline for the trend chart."""
    W, H, PAD = 500, 110, 10
    mn, mx = min(points), max(points)
    rng = max(mx - mn, 1)

    def px(i):
        x = PAD + i * (W - 2 * PAD) / max(len(points) - 1, 1)
        y = H - PAD - (points[i] - mn) / rng * (H - 2 * PAD)
        return x, y

    coords = [px(i) for i in range(len(points))]
    path_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    fill_d = path_d + f" L {coords[-1][0]:.1f},{H} L {coords[0][0]:.1f},{H} Z"

    # threshold lines
    threshold_med = H - PAD - (55 - mn) / rng * (H - 2 * PAD) if rng > 0 else H // 2
    threshold_hig = H - PAD - (70 - mn) / rng * (H - 2 * PAD) if rng > 0 else H // 3

    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#00c8ff" opacity=".9"/>'
        for x, y in coords[-1:]
    )

    svg = f"""
<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="lg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#00c8ff" stop-opacity=".28"/>
      <stop offset="100%" stop-color="#00c8ff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- grid lines -->
  <line x1="{PAD}" y1="{H-PAD}" x2="{W-PAD}" y2="{H-PAD}" stroke="#1a2d4a" stroke-width="1"/>
  <line x1="{PAD}" y1="{threshold_med:.1f}" x2="{W-PAD}" y2="{threshold_med:.1f}" stroke="#ff9d2e" stroke-width="1" stroke-dasharray="4 4" opacity=".5"/>
  <line x1="{PAD}" y1="{threshold_hig:.1f}" x2="{W-PAD}" y2="{threshold_hig:.1f}" stroke="#ff3b5c" stroke-width="1" stroke-dasharray="4 4" opacity=".5"/>
  <!-- labels -->
  <text x="{W-PAD+4}" y="{threshold_med:.1f}" fill="#ff9d2e" font-size="9" opacity=".7" dominant-baseline="middle">MED</text>
  <text x="{W-PAD+4}" y="{threshold_hig:.1f}" fill="#ff3b5c" font-size="9" opacity=".7" dominant-baseline="middle">HIGH</text>
  <!-- area -->
  <path d="{fill_d}" fill="url(#lg)"/>
  <!-- line -->
  <path d="{path_d}" fill="none" stroke="#00c8ff" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
  <!-- latest dot -->
  {dots}
</svg>
"""
    return svg


# ── Session state init ─────────────────────────────────────────────────────────
if "history" not in st.session_state:
    seed = [random.randint(10, 45) for _ in range(11)]
    st.session_state.history = seed

if "reading_count" not in st.session_state:
    st.session_state.reading_count = len(st.session_state.history)

if "last_data" not in st.session_state:
    st.session_state.last_data = None

if "last_update" not in st.session_state:
    st.session_state.last_update = None


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
  <span class="hdr-wave">🌊</span>
  <h1 class="hdr-title">HYDRONYX</h1>
  <p class="hdr-sub">Coastal Risk Detection System · v2.2</p>
  <div class="hdr-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── System Status + Location ──────────────────────────────────────────────────
col_loc, col_stat = st.columns([1, 1])
with col_loc:
    st.markdown("📍 **Location:** Chennai Coastal Zone")
with col_stat:
    st.success("System Status: Active ✅")

# ── Timestamp ─────────────────────────────────────────────────────────────────
now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f'<p class="ts">⏱ Last updated: {now} UTC</p>', unsafe_allow_html=True)

# ── Mode Switch ───────────────────────────────────────────────────────────────
mode = st.radio("Mode", ["Simulation", "Live Sensor"], horizontal=True)

# ── Input card ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-label">💧 Sensor Input</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    if mode == "Live Sensor":
        fresh_data = fetch_backend_data()

        if fresh_data:
            # ✅ Got live data — cache it
            st.session_state.last_data = fresh_data
            st.session_state.last_update = datetime.now()
            data = fresh_data
            data_is_live = True
        elif st.session_state.last_data:
            # ⚠️ Backend failed but we have cached data — use it
            data = st.session_state.last_data
            data_is_live = False
            st.warning("⚠️ Data delayed (showing last update)")
        else:
            # ❌ No data ever received — use safe zeros, never crash
            st.warning("⚠️ Waiting for real-time data...")
            data = {"water_level": 0, "rain": 0, "temperature": 0, "humidity": 0}
            st.info("Initializing real-time data stream...")
            data_is_live = False

        raw_level    = data["water_level"]
        # ── Smooth water level (prevents sudden jumps) ──
        if "smooth_level" not in st.session_state:
            st.session_state.smooth_level = raw_level
        st.session_state.smooth_level = (
            0.7 * st.session_state.smooth_level +
            0.3 * raw_level
        )
        water_level  = int(st.session_state.smooth_level)
        rain_value   = data["rain"]
        raining      = rain_value > 0 or data.get("humidity", 0) > 85

        # ── Single clean status indicator (no duplicates) ──
        if "last_update" in st.session_state and st.session_state.last_update:
            st.caption(f"Last update: {st.session_state.last_update.strftime('%H:%M:%S')}")
            delay = (datetime.now() - st.session_state.last_update).seconds
            if delay < 5:
                st.success("🟢 Real-Time Data Active")
            elif delay < 15:
                st.warning("🟡 Slight delay")
            else:
                st.error("🔴 Data stale")

        st.markdown(f"""
        <div style="padding:.6rem 0 .2rem; font-size:.85rem; color:#5a7a9a;">
          🔴 Live Sensor Reading
        </div>
        <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:700; color:#00c8ff;">
          {water_level} cm
        </div>
        <div style="font-size:.68rem; color:#3a5070; margin-top:.2rem;">
          Auto-refreshes every 3 s · Buzzer will activate in real hardware
        </div>
        """, unsafe_allow_html=True)
    else:
        water_level = st.slider(
            "Water Level (cm)", min_value=0, max_value=100,
            value=30, step=1,
            help="Simulated coastal water level sensor reading"
        )
with col2:
    if mode == "Simulation":
        st.markdown("<br>", unsafe_allow_html=True)
        raining = st.checkbox("🌧 Rain Active", value=False)
    else:
        # rain comes from backend in Live Sensor mode — no manual checkbox
        st.markdown("<br><br>", unsafe_allow_html=True)
        rain_icon = "🌧" if raining else "☀️"
        st.markdown(f"<div style='text-align:center; font-size:1.4rem;'>{rain_icon}</div>",
                    unsafe_allow_html=True)

# water level visual bar
fill_pct = water_level
fill_col = bar_color(water_level)
st.markdown(f"""
<div class="wl-bar-wrap">
  <div class="wl-bar-fill" style="width:{fill_pct}%; background:{fill_col};"></div>
</div>
<div class="wl-bar-label"><span>0 cm</span><span style="color:{fill_col}; font-weight:600;">{water_level} cm</span><span>100 cm</span></div>
""", unsafe_allow_html=True)

# ── Update history ────────────────────────────────────────────────────────────
hist = st.session_state.history
hist.append(water_level)
if len(hist) > 20:
    hist.pop(0)
st.session_state.history = hist
st.session_state.reading_count += 1

# ── Risk calculation ─────────────────────────────────────────────────────────
humidity_val = data.get("humidity", 0) if mode == "Live Sensor" else 0
risk = get_risk(water_level, raining, humidity_val)
risk_icons = {"LOW": "🟢", "MEDIUM": "🟠", "HIGH": "🔴"}
risk_labels = {
    "LOW":    ("SAFE",               "All coastal parameters within normal bounds."),
    "MEDIUM": ("⚠ WARNING",          "Elevated water levels detected. Monitor closely."),
    "HIGH":   ("🚨 EMERGENCY ALERT", "Critical flood risk! Initiate evacuation protocol."),
}
badge_class = {"LOW": "risk-LOW", "MEDIUM": "risk-MED", "HIGH": "risk-HIGH"}
alert_class = {"LOW": "alert-LOW", "MEDIUM": "alert-MED", "HIGH": "alert-HIGH"}

# ── AI Prediction ─────────────────────────────────────────────────────────────
if risk == "HIGH":
    prediction = "🔺 Rapid Increase Expected"
elif risk == "MEDIUM":
    prediction = "📈 Possible Rise"
else:
    prediction = "✅ Normal Conditions"

# ── TWO-COLUMN LAYOUT: left = risk + alerts, right = metrics + chart ──────────
col_left, col_right = st.columns([1, 1])

with col_left:
    # Risk output card
    label, detail = risk_labels[risk]
    rain_indicator = "  ·  🌧 Rain Active" if raining else ""
    st.markdown(f"""
<div class="card">
  <div class="card-label">📡 Risk Assessment</div>
  <div class="risk-wrap">
    <div class="risk-badge {badge_class[risk]}">{risk}</div>
    <div class="alert {alert_class[risk]}">
      <span>{risk_icons[risk]}</span>
      <span>{label}{rain_indicator}</span>
    </div>
    <p style="font-size:.78rem; color:#5a7a9a; margin-top:.8rem; margin-bottom:0;">{detail}</p>
  </div>
</div>
""", unsafe_allow_html=True)
    st.caption(f"Score based on water level, rainfall, and humidity = {water_level}")

    # HIGH risk: error banner + GSM simulation
    if risk == "HIGH":
        st.error("🚨 HIGH FLOOD RISK — ALERT TRIGGERED · Buzzer activated")
        st.markdown("""
<div style='margin-top:10px; padding:12px 16px; background:#111827;
     border-radius:10px; border:1px solid #2a3a2a; font-size:0.82rem; color:#00e5a0;
     font-family:monospace; line-height:1.7;'>
  <div style='color:#5a7a9a; font-size:.68rem; letter-spacing:.15em; text-transform:uppercase;
       margin-bottom:6px;'>📡 GSM MODULE · SIM800L</div>
  📨 <strong>SMS Sent:</strong><br>
  "Flood Alert! Water level critical in Chennai Coastal Zone. Evacuate immediately."<br>
  <span style='color:#3a6a4a; font-size:.72rem;'>→ Recipient: +91-XXXX-XXXXX &nbsp;·&nbsp; Status: DELIVERED ✅</span>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"🔮 **Prediction:** {prediction}")
    st.markdown("🔌 **Sensors:** Ultrasonic ✅ &nbsp;|&nbsp; Water Level ✅ &nbsp;|&nbsp; GSM ✅")

with col_right:
    # Metric tiles
    avg_level = round(sum(hist) / len(hist), 1)
    peak = max(hist)
    rain_str = "YES" if raining else "NO"
    temp_val  = data.get("temperature", 0) if mode == "Live Sensor" and 'data' in dir() else 30
    st.markdown(f"""
<div class="metrics" style="flex-wrap:wrap;">
  <div class="metric">
    <div class="metric-val">{water_level}</div>
    <div class="metric-lbl">💧 Current (cm)</div>
  </div>
  <div class="metric">
    <div class="metric-val">{avg_level}</div>
    <div class="metric-lbl">📊 Avg (cm)</div>
  </div>
  <div class="metric">
    <div class="metric-val">{peak}</div>
    <div class="metric-lbl">📈 Peak (cm)</div>
  </div>
  <div class="metric">
    <div class="metric-val" style="{'color: #ff9d2e' if raining else ''}">{rain_str}</div>
    <div class="metric-lbl">🌧 Rainfall</div>
  </div>
  <div class="metric">
    <div class="metric-val" style="color:#ff9d2e;">{temp_val}</div>
    <div class="metric-lbl">🌡️ Temp (°C)</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Trend chart inside expander
    svg = sparkline_svg(hist)
    times = [(datetime.now() - timedelta(minutes=(len(hist) - 1 - i))).strftime("%H:%M")
             for i in range(len(hist))]
    t_start, t_end = times[0], times[-1]

    with st.expander("📊 Water Level Trend", expanded=True):
        st.markdown(f"""
<div style="font-family:'Syne',sans-serif; font-size:.65rem; letter-spacing:.18em;
     text-transform:uppercase; color:#5a7a9a; margin-bottom:.6rem;">
  Reading history · {t_start} — {t_end}
</div>
{svg}
<div style="display:flex; justify-content:space-between; font-size:.62rem; color:#3a5070; margin-top:.3rem;">
  <span>{t_start}</span><span>← last {len(hist)} readings →</span><span>{t_end}</span>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1.4rem 0 2rem; color: #2a4060; font-size:.68rem; letter-spacing:.15em; text-transform:uppercase;">
  Hydronyx · Coastal Risk Detection System · Demo Build
</div>
""", unsafe_allow_html=True)

# ── Auto-refresh hint ─────────────────────────────────────────────────────────
st.markdown("""
---
<div style="font-size:.72rem; color:#3a5070; text-align:center; margin-top:-.6rem;">
Simulation mode: move the slider · Live Sensor mode: fetches real data from backend API
</div>
""", unsafe_allow_html=True)

# ── Auto-refresh in Live Sensor mode ─────────────────────────────────────────
if mode == "Live Sensor":
    time.sleep(3)
    st.rerun()