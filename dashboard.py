import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import random
import time
import datetime

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title = "Uber Dynamic Pricing Engine",
    page_icon  = "U",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 10px 0;
        letter-spacing: 2px;
    }
    .hero-sub {
        text-align: center;
        color: #aaaaaa;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #00d4ff33;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 4px;
    }
    .feature-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #7b2ff733;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 5px;
        height: 160px;
    }
    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .feature-desc {
        font-size: 0.82rem;
        color: #999;
        line-height: 1.5;
    }
    .price-card {
        background: linear-gradient(135deg, #0d2137, #1a0d2e);
        border: 2px solid #00d4ff55;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
    }
    .price-big {
        font-size: 4rem;
        font-weight: 800;
        color: #00ff88;
    }
    .price-label {
        font-size: 1rem;
        color: #aaa;
    }
    .badge-surge    { background:#ff4444; color:white; padding:6px 18px; border-radius:20px; font-weight:600; font-size:0.9rem; display:inline-block; }
    .badge-moderate { background:#ff9900; color:white; padding:6px 18px; border-radius:20px; font-weight:600; font-size:0.9rem; display:inline-block; }
    .badge-normal   { background:#00aa55; color:white; padding:6px 18px; border-radius:20px; font-weight:600; font-size:0.9rem; display:inline-block; }
    .section-header { font-size:1.4rem; font-weight:700; color:#ffffff; border-left:4px solid #00d4ff; padding-left:12px; margin:20px 0 12px 0; }
    .custom-divider { height:1px; background:linear-gradient(90deg, transparent, #00d4ff44, transparent); margin:20px 0; }
    .live-badge     { background:#00aa55; color:white; padding:4px 12px; border-radius:12px; font-size:0.8rem; font-weight:600; display:inline-block; margin-left:10px; }
    .manual-badge   { background:#555; color:white; padding:4px 12px; border-radius:12px; font-size:0.8rem; font-weight:600; display:inline-block; margin-left:10px; }
    [data-testid="stSidebar"]       { background:linear-gradient(180deg, #0d0d1a, #1a0d2e); border-right:1px solid #00d4ff22; }
    [data-testid="metric-container"]{ background:linear-gradient(135deg, #1a1a2e, #16213e); border:1px solid #00d4ff22; border-radius:12px; padding:16px; }
</style>
""", unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================

st.markdown("""
<div style="text-align:center; padding:20px 0 10px 0;">
    <div class="hero-title">UBER DYNAMIC PRICING ENGINE</div>
    <div class="hero-sub">
        Real-time surge prediction — XGBoost + Reinforcement Learning (PPO)
    </div>
    <div style="color:#555; font-size:0.9rem; margin-top:4px;">
        Boston MA Dataset &nbsp;|&nbsp; AI-Powered &nbsp;|&nbsp;
        Less than 50ms Latency &nbsp;|&nbsp; 86MB Training Data
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# TOP STATS
# ============================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">86MB</div>
        <div class="stat-label">Training Dataset</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">0.023</div>
        <div class="stat-label">Model MAE Score</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">100K</div>
        <div class="stat-label">RL Training Steps</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">+25%</div>
        <div class="stat-label">Revenue Lift</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown("""<div class="stat-card">
        <div class="stat-number">&lt;50ms</div>
        <div class="stat-label">API Latency</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# FEATURE CARDS
# ============================================

f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown("""<div class="feature-card">
        <div class="feature-title">XGBoost Model</div>
        <div class="feature-desc">Gradient boosting trained on 80% ride data. Predicts surge with MAE of only 0.023.</div>
    </div>""", unsafe_allow_html=True)
with f2:
    st.markdown("""<div class="feature-card">
        <div class="feature-title">RL Agent PPO</div>
        <div class="feature-desc">Proximal Policy Optimization learns optimal pricing through 100K simulations.</div>
    </div>""", unsafe_allow_html=True)
with f3:
    st.markdown("""<div class="feature-card">
        <div class="feature-title">Real-time API</div>
        <div class="feature-desc">FastAPI backend serving predictions with under 50ms response latency.</div>
    </div>""", unsafe_allow_html=True)
with f4:
    st.markdown("""<div class="feature-card">
        <div class="feature-title">Smart Surge Logic</div>
        <div class="feature-desc">Peak hours, weather, and demand signals combined for fairest dynamic pricing.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.markdown("""
<div style='text-align:center; padding:10px 0'>
    <div style='font-size:1.1rem; font-weight:700; color:#00d4ff'>
        Ride Parameters
    </div>
    <div style='font-size:0.75rem; color:#666'>
        Manual or Auto Live Mode
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# AUTO MODE TOGGLE
auto_mode = st.sidebar.toggle("Auto Live Mode", value=False)

if auto_mode:
    # ── AUTO MODE ──────────────────────────────────
    st.sidebar.success("Live Mode Active — Auto updating")

    city     = st.sidebar.text_input("City Name", value="Karachi")
    distance = st.sidebar.slider("Distance (miles)", 0.5, 20.0, 3.5)
    refresh  = st.sidebar.selectbox(
        "Refresh Every",
        [10, 30, 60, 120],
        index=1,
        format_func=lambda x: f"{x} seconds"
    )

    # Import auto data module
    try:
        from auto_data import get_all_live_data
        live_data = get_all_live_data(city=city, distance=distance)

        # Show live data in sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Live Data Fetched**")
        st.sidebar.info(
            f"Time    : {live_data['hour']}:00\n\n"
            f"Temp    : {live_data['temp']}F\n\n"
            f"Rain    : {live_data['rain']}\n\n"
            f"Demand  : {live_data['demand_index']}"
        )

        if live_data.get('weather_success'):
            st.sidebar.success(f"Weather API connected for {city}")
        else:
            st.sidebar.warning("Weather API key not set — using defaults")

    except ImportError:
        st.sidebar.error("auto_data.py not found in folder")
        live_data = None

else:
    # ── MANUAL MODE ────────────────────────────────
    st.sidebar.markdown("**Trip Details**")

    distance    = st.sidebar.slider("Distance (miles)",  0.5,  20.0, 3.5)
    hour        = st.sidebar.slider("Hour of Day",       0,    23,   8)
    day_of_week = st.sidebar.selectbox(
        "Day of Week",
        [0,1,2,3,4,5,6],
        format_func=lambda x: [
            "Monday","Tuesday","Wednesday",
            "Thursday","Friday","Saturday","Sunday"][x]
    )
    is_weekend   = 1 if day_of_week >= 5 else 0
    is_peak_hour = 1 if (7 <= hour <= 9 or 17 <= hour <= 20) else 0

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Weather Conditions**")
    temp             = st.sidebar.slider("Temperature (F)",  10.0, 100.0, 55.0)
    rain             = st.sidebar.slider("Rain Intensity",    0.0,   1.0,  0.3)
    humidity         = st.sidebar.slider("Humidity (%)",      0.0, 100.0, 70.0)
    weather_severity = st.sidebar.slider("Weather Severity",  0.0,   1.0,  0.5)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Demand Signals**")
    demand_index = st.sidebar.slider("Demand Index",  0.0, 1.0,  0.85)
    route_demand = st.sidebar.slider("Route Demand", 100, 3000, 1200)

    st.sidebar.markdown("---")

    if is_peak_hour:
        st.sidebar.error("Peak Hour Active — Higher Surge")
    else:
        st.sidebar.success("Normal Hours — Standard Pricing")

    if is_weekend:
        st.sidebar.warning("Weekend — Elevated Demand")
    else:
        st.sidebar.info("Weekday")

    if rain > 0.5:
        st.sidebar.error("Heavy Rain — Surge Expected")
    elif rain > 0.2:
        st.sidebar.warning("Light Rain — Moderate Surge")
    else:
        st.sidebar.success("Clear Weather")

    live_data = None

st.sidebar.markdown("---")

if not auto_mode:
    predict_btn = st.sidebar.button(
        "Predict Price Now",
        use_container_width=True,
        type="primary"
    )
else:
    predict_btn = False

# ============================================
# API CALL FUNCTION
# ============================================

def get_prediction(distance, hour, day_of_week, is_weekend,
                   is_peak_hour, demand_index, temp, rain,
                   humidity, weather_severity, route_demand, **kwargs):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict-price",
            json={
                "distance"        : distance,
                "hour"            : hour,
                "day_of_week"     : day_of_week,
                "is_weekend"      : is_weekend,
                "is_peak_hour"    : is_peak_hour,
                "demand_index"    : demand_index,
                "temp"            : temp,
                "rain"            : rain,
                "humidity"        : humidity,
                "weather_severity": weather_severity,
                "route_demand"    : route_demand
            },
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ============================================
# RESULT DISPLAY FUNCTION
# ============================================

def show_results(result, input_data):
    if "error" in result:
        st.error(f"API Error: {result['error']}")
        st.info("Make sure FastAPI server is running: uvicorn main:app --reload")
        return

    # ── Price Cards ────────────────────────────────
    st.markdown('<div class="section-header">Price Prediction Result</div>',
                unsafe_allow_html=True)

    res1, res2, res3 = st.columns(3)

    with res1:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">Final Ride Price</div>
            <div class="price-big">${result['final_price']}</div>
            <div class="price-label" style="margin-top:8px">
                Base $10.00 + Surge ${result['final_price']-10:.2f}
            </div>
        </div>""", unsafe_allow_html=True)

    with res2:
        badge_class  = (
            "badge-surge"    if result['status'] == "High Surge"     else
            "badge-moderate" if result['status'] == "Moderate Surge" else
            "badge-normal"
        )
        status_color = (
            "HIGH SURGE"     if result['status'] == "High Surge"     else
            "MODERATE SURGE" if result['status'] == "Moderate Surge" else
            "NORMAL"
        )
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">Surge Status</div>
            <div style="font-size:1.6rem; font-weight:700;
                        color:#fff; margin:12px 0">
                {status_color}
            </div>
            <div class="{badge_class}">{result['status']}</div>
            <div class="price-label" style="margin-top:10px">
                Multiplier: {result['final_multiplier']}x
            </div>
        </div>""", unsafe_allow_html=True)

    with res3:
        st.markdown(f"""
        <div class="price-card">
            <div class="price-label">Recommended By</div>
            <div style="font-size:1.6rem; font-weight:700;
                        color:#7b2ff7; margin:12px 0">
                {result['recommended_by']}
            </div>
            <div class="price-label">
                XGBoost: {result['xgb_multiplier']}x &nbsp;|&nbsp;
                RL: {result['rl_multiplier']}x
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Metrics ────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Base Price",  "$10.00")
    m2.metric("XGBoost",     f"{result['xgb_multiplier']}x",
              f"${10*result['xgb_multiplier']:.2f}")
    m3.metric("RL Agent",    f"{result['rl_multiplier']}x",
              f"${10*result['rl_multiplier']:.2f}")
    m4.metric("Final Price", f"${result['final_price']}",
              f"+{((result['final_price']/10)-1)*100:.1f}% surge")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────
    st.markdown('<div class="section-header">Model Analysis</div>',
                unsafe_allow_html=True)

    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        fig_bar = go.Figure(go.Bar(
            x            = ["XGBoost", "RL Agent", "Final"],
            y            = [result['xgb_multiplier'],
                            result['rl_multiplier'],
                            result['final_multiplier']],
            marker_color = ["#00d4ff", "#7b2ff7", "#00ff88"],
            text         = [f"{result['xgb_multiplier']}x",
                            f"{result['rl_multiplier']}x",
                            f"{result['final_multiplier']}x"],
            textposition = "outside"
        ))
        fig_bar.update_layout(
            title         = "Model Comparison",
            yaxis_range   = [0, 3.5],
            height        = 320,
            paper_bgcolor = "rgba(0,0,0,0)",
            plot_bgcolor  = "rgba(0,0,0,0)",
            font          = dict(color="white"),
            showlegend    = False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with ch2:
        fig_donut = go.Figure(go.Pie(
            labels        = ["Base Price", "Surge Amount"],
            values        = [10, result['final_price'] - 10],
            marker_colors = ["#00d4ff", "#ff6b6b"],
            hole          = 0.55,
            textinfo      = "label+percent"
        ))
        fig_donut.update_layout(
            title         = "Price Breakdown",
            height        = 320,
            paper_bgcolor = "rgba(0,0,0,0)",
            font          = dict(color="white")
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with ch3:
        fig_gauge = go.Figure(go.Indicator(
            mode  = "gauge+number+delta",
            value = result['final_multiplier'],
            delta = {"reference": 1.0},
            title = {"text": "Surge Level",
                     "font": {"color": "white"}},
            gauge = {
                "axis"    : {"range": [0, 3],
                             "tickcolor": "white"},
                "bar"     : {"color": "#00ff88"},
                "steps"   : [
                    {"range": [0,    1.25], "color": "#1a2a1a"},
                    {"range": [1.25, 2.0],  "color": "#2a2a1a"},
                    {"range": [2.0,  3.0],  "color": "#2a1a1a"}
                ],
                "threshold": {
                    "line" : {"color": "red", "width": 4},
                    "value": 2.0
                }
            },
            number = {"suffix": "x", "font": {"color": "white"}}
        ))
        fig_gauge.update_layout(
            height        = 320,
            paper_bgcolor = "rgba(0,0,0,0)",
            font          = dict(color="white")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── 24 Hour Surge Chart ────────────────────────
    st.markdown('<div class="section-header">24-Hour Surge Pattern</div>',
                unsafe_allow_html=True)

    hours  = list(range(24))
    surges = []
    for h in hours:
        if 7 <= h <= 9:
            surges.append(round(1.8 + random.uniform(-0.1, 0.3), 2))
        elif 17 <= h <= 20:
            surges.append(round(2.0 + random.uniform(-0.1, 0.5), 2))
        elif 0 <= h <= 5:
            surges.append(round(1.5 + random.uniform(0, 0.5), 2))
        else:
            surges.append(round(1.0 + random.uniform(0, 0.2), 2))

    current_hour = input_data.get('hour', 8)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x         = hours,
        y         = surges,
        mode      = "lines+markers",
        name      = "Surge Multiplier",
        line      = dict(color="#00d4ff", width=3),
        fill      = "tozeroy",
        fillcolor = "rgba(0,212,255,0.1)"
    ))
    fig_line.add_trace(go.Scatter(
        x    = [current_hour, current_hour],
        y    = [0, max(surges)],
        mode = "lines",
        name = "Current Hour",
        line = dict(color="#ff6b6b", width=2, dash="dash")
    ))
    fig_line.update_layout(
        title         = f"Surge Pattern — Current Hour: {current_hour}:00",
        xaxis_title   = "Hour of Day",
        yaxis_title   = "Surge Multiplier",
        height        = 280,
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor  = "rgba(0,0,0,0)",
        font          = dict(color="white"),
        xaxis         = dict(
            tickvals  = list(range(0, 24, 2)),
            gridcolor = "rgba(255,255,255,0.07)"
        ),
        yaxis         = dict(
            gridcolor = "rgba(255,255,255,0.07)"
        )
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Summary Tables ─────────────────────────────
    st.markdown('<div class="section-header">Complete Trip Summary</div>',
                unsafe_allow_html=True)

    day_names = ["Monday","Tuesday","Wednesday",
                 "Thursday","Friday","Saturday","Sunday"]

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("**Trip Info**")
        st.dataframe(pd.DataFrame({
            "Parameter" : ["Distance","Hour","Day",
                           "Peak Hour","Weekend"],
            "Value"     : [
                f"{input_data.get('distance', 0)} miles",
                f"{input_data.get('hour', 0)}:00",
                day_names[input_data.get('day_of_week', 0)],
                "Yes" if input_data.get('is_peak_hour') else "No",
                "Yes" if input_data.get('is_weekend')   else "No"
            ]
        }), hide_index=True, use_container_width=True)

    with s2:
        st.markdown("**Weather Info**")
        st.dataframe(pd.DataFrame({
            "Parameter" : ["Temperature","Rain","Humidity",
                           "Severity","Demand Index"],
            "Value"     : [
                f"{input_data.get('temp', 0)} F",
                f"{input_data.get('rain', 0)}",
                f"{input_data.get('humidity', 0)}%",
                f"{input_data.get('weather_severity', 0)}",
                f"{input_data.get('demand_index', 0)}"
            ]
        }), hide_index=True, use_container_width=True)

    with s3:
        st.markdown("**Pricing Info**")
        st.dataframe(pd.DataFrame({
            "Parameter" : ["Base Price","XGBoost","RL Agent",
                           "Final Multiplier","Final Price","Status"],
            "Value"     : [
                "$10.00",
                f"{result['xgb_multiplier']}x",
                f"{result['rl_multiplier']}x",
                f"{result['final_multiplier']}x",
                f"${result['final_price']}",
                result['status']
            ]
        }), hide_index=True, use_container_width=True)

# ============================================
# MAIN LOGIC
# ============================================

if auto_mode and live_data:
    # AUTO MODE — automatic prediction
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(
        f'<div class="section-header">Live Auto Prediction'
        f'<span class="live-badge">LIVE — {now_str}</span></div>',
        unsafe_allow_html=True
    )

    with st.spinner("Fetching live data and predicting..."):
        result = get_prediction(**live_data)

    show_results(result, live_data)

    # Countdown and auto refresh
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    countdown = st.empty()
    for i in range(refresh, 0, -1):
        countdown.info(f"Next auto refresh in {i} seconds...")
        time.sleep(1)

    st.rerun()

elif predict_btn:
    # MANUAL MODE — button click prediction
    input_data = {
        "distance"        : distance,
        "hour"            : hour,
        "day_of_week"     : day_of_week,
        "is_weekend"      : is_weekend,
        "is_peak_hour"    : is_peak_hour,
        "demand_index"    : demand_index,
        "temp"            : temp,
        "rain"            : rain,
        "humidity"        : humidity,
        "weather_severity": weather_severity,
        "route_demand"    : route_demand
    }

    with st.spinner("Calculating optimal price..."):
        result = get_prediction(**input_data)

    show_results(result, input_data)

else:
    # DEFAULT LANDING VIEW
    st.markdown('<div class="section-header">How It Works</div>',
                unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        st.markdown("""<div class="feature-card" style="height:180px">
            <div class="feature-title">Step 1 — Input</div>
            <div class="feature-desc">Set ride distance, time, day, weather and demand using sidebar sliders.</div>
        </div>""", unsafe_allow_html=True)
    with h2:
        st.markdown("""<div class="feature-card" style="height:180px">
            <div class="feature-title">Step 2 — XGBoost</div>
            <div class="feature-desc">ML model predicts surge multiplier based on historical ride patterns.</div>
        </div>""", unsafe_allow_html=True)
    with h3:
        st.markdown("""<div class="feature-card" style="height:180px">
            <div class="feature-title">Step 3 — RL Agent</div>
            <div class="feature-desc">PPO agent decides optimal price to maximize revenue and minimize cancellations.</div>
        </div>""", unsafe_allow_html=True)
    with h4:
        st.markdown("""<div class="feature-card" style="height:180px">
            <div class="feature-title">Step 4 — Final Price</div>
            <div class="feature-desc">Best multiplier selected and final ride price returned in real-time.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.info("Adjust parameters in the sidebar and click Predict Price Now — or turn on Auto Live Mode!")

# ============================================
# FOOTER
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#444; font-size:0.8rem; padding:10px'>
    <b>Uber Dynamic Pricing Engine</b> &nbsp;|&nbsp;
    XGBoost + PPO Reinforcement Learning &nbsp;|&nbsp;
    FastAPI: <code>http://127.0.0.1:8000</code> &nbsp;|&nbsp;
    Dashboard: <code>http://localhost:8501</code>
</div>
""", unsafe_allow_html=True)
