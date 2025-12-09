import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from modules.nav import SideBarLinks

st.set_page_config(
    page_title="FitFlow | Client Portal",
    page_icon="💪",
    layout="wide"
)
SideBarLinks()

# Get client info from session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = 1
if 'client_name' not in st.session_state:
    st.session_state.client_name = "Chester Stone"

st.markdown(
    """
    <style>
        :root {
            --fit-primary: #ff4d4f;
            --fit-secondary: #05d5ff;
            --fit-bg: #ffffff;
            --fit-card: rgba(0,0,0,0.02);
            --fit-stroke: rgba(0,0,0,0.08);
        }
        [data-testid="stAppViewContainer"] {
            background: #ffffff;
            color: #111827;
        }
        .fit-hero {
            position: relative;
            padding: 26px 26px 22px;
            border-radius: 16px;
            overflow: hidden;
            background: linear-gradient(120deg, rgba(255,77,79,0.16), rgba(5,213,255,0.12), #ffffff);
            border: 1px solid rgba(0,0,0,0.05);
            box-shadow: 0 16px 40px rgba(0,0,0,0.12);
            backdrop-filter: blur(12px);
        }
        .fit-hero:before, .fit-hero:after {
            content: "";
            position: absolute;
            inset: -20% auto auto -10%;
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, rgba(255,77,79,0.22), transparent 60%);
            filter: blur(6px);
            transform: rotate(-12deg);
        }
        .fit-hero:after {
            inset: auto -20% -20% auto;
            background: radial-gradient(circle, rgba(5,213,255,0.18), transparent 58%);
            transform: rotate(18deg);
        }
        .fit-grid {
            display: grid;
            gap: 14px;
        }
        .fit-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border-radius: 30px;
            border: 1px solid var(--fit-stroke);
            background: rgba(255,77,79,0.08);
            font-size: 0.9rem;
            color: #0f172a;
        }
        .fit-card {
            border-radius: 14px;
            padding: 16px 18px;
            background: linear-gradient(160deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01));
            border: 1px solid var(--fit-stroke);
            box-shadow: 0 16px 40px rgba(0,0,0,0.35);
        }
        .fit-metric {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .fit-metric span.label { color: #6b7280; font-size: 0.95rem; }
        .fit-metric span.value { font-size: 1.8rem; font-weight: 700; color: #0f172a; }
        .fit-glow {
            position: relative;
            overflow: hidden;
        }
        .fit-glow:after {
            content: "";
            position: absolute;
            inset: -40%;
            background: conic-gradient(from 120deg, rgba(255,77,79,0.18), rgba(5,213,255,0.16), rgba(255,77,79,0.18));
            filter: blur(80px);
            z-index: 0;
        }
        .fit-glow > * { position: relative; z-index: 1; }
        .fit-actions button {
            background: linear-gradient(135deg, #ff4d4f, #ff6b6d);
            color: #fff;
            border: none;
            box-shadow: 0 10px 25px rgba(255,77,79,0.35);
            transition: transform 120ms ease, box-shadow 120ms ease;
        }
        .fit-actions button:hover { transform: translateY(-2px) scale(1.01); }
        .fit-actions button:focus { outline: 2px solid rgba(255,77,79,0.35); }
        .fit-quick-btn button {
            border: 1px solid var(--fit-stroke);
            background: rgba(255,255,255,0.05);
            color: #f5f5f5;
            transition: border-color 120ms ease, transform 120ms ease;
        }
        .fit-quick-btn button:hover {
            border-color: rgba(255,77,79,0.45);
            transform: translateY(-1px);
        }
        .fit-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .fit-chip {
            padding: 6px 10px;
            border-radius: 10px;
            background: rgba(5,213,255,0.08);
            border: 1px solid rgba(5,213,255,0.2);
            font-size: 0.88rem;
            color: #0f172a;
        }
        @keyframes floaty {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }
        .fit-floating { animation: floaty 6s ease-in-out infinite; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="fit-hero fit-glow">
        <div style="display:flex; justify-content:space-between; gap:18px; align-items:flex-start;">
            <div>
                <p class="fit-pill">Client Mode • Personalized</p>
                <h1 style="margin: 6px 0 8px; font-size: 2rem; color: #0f172a;">
                    Hey {st.session_state.client_name}, let's make today count 👋
                </h1>
                <p style="margin:0; color:#1f2937; max-width:720px; font-size:1rem;">
                    This is your command center for workouts, progress, and coach programming. 
                    Keep up the streak and celebrate the small wins—they stack up fast.
                </p>
                <div class="fit-chip-row">
                    <span class="fit-chip">🔥 Consistency beats perfection</span>
                    <span class="fit-chip">🎯 Micro-wins every session</span>
                    <span class="fit-chip">📈 Progress you can feel</span>
                </div>
            </div>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown("---")

col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown("### Your Training Hub")
    st.markdown(
        """
        Step into a sharper, more cinematic FitFlow. Use the quick actions to jump in, or scroll to explore.
        """)
    st.markdown(
        """
        - 📊 **Dashboard** Keep tabs on wins, streaks, and trends  
        - 📝 **Log Workouts** Capture every session with context  
        - 🎯 **Coach Program** Follow the exact plan set for you  
        """)
    st.info("💡 Tip: Log right after each session to keep the momentum alive.")

with col2:
    st.markdown("### Quick Pulse")
    logs = []
    try:
        response = requests.get(
            f"http://web-api:4000/client/client_workout_log",
            params={"client_id": st.session_state.client_id}
        )
        if response.status_code == 200:
            logs = response.json()
        else:
            st.warning("Unable to load stats")
    except:
        st.warning("API connection unavailable")

    total_logged = len(logs)
    avg_duration = 0
    last_status = "n/a"

    if logs:
        df = pd.DataFrame(logs)
        avg_duration = df['duration_minutes'].mean()
        last_status = df.iloc[0].get('completion_status', 'n/a')

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(
            f"""
            <div class="fit-card fit-metric">
                <span class="label">Workouts logged</span>
                <span class="value">{total_logged}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with stat_col2:
        st.markdown(
            f"""
            <div class="fit-card fit-metric">
                <span class="label">Avg session</span>
                <span class="value">{avg_duration:.0f} min</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown(
        f"""
        <div class="fit-pill" style="margin-top:10px;">
            Latest status • <b>{last_status}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Feature cards
st.markdown("### ⚡ Quick Access")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        #### 📊 Dashboard
        See your recent workout history and trends over time.
        """
    )
    if st.button("Go to Dashboard →", use_container_width=True, key="dash_btn"):
        st.switch_page("pages/22_client_dashboard.py")

with col2:
    st.markdown(
        """
        #### 📝 Log Workout
        Record a new training session with duration, notes, and completion status.
        """
    )
    if st.button("Log Workout →", use_container_width=True, key="log_btn"):
        st.switch_page("pages/23_client_log_workout.py")

with col3:
    st.markdown(
        """
        #### 🎯 My Program
        View your coach-assigned workout program with all exercise details.
        """
    )
    if st.button("View Program →", use_container_width=True, key="program_btn"):
        st.switch_page("pages/24_client_my_program.py")

st.markdown("---")

# Celebrate and momentum block
celebrate_col, streak_col = st.columns([1.1, 1])
with celebrate_col:
    st.markdown("### 🎈 Celebrate a micro-win")
    if st.button("Launch balloons", type="primary", use_container_width=True, key="celebrate_btn"):
        st.balloons()
        st.success("Mini win logged—keep stacking them up!")

with streak_col:
    st.markdown("### 🔥 Momentum meter")
    streak_value = min(total_logged, 12)
    st.progress(streak_value / 12.0, text=f"{streak_value}/12 target sessions")
    st.caption("Demo-friendly meter to showcase progress energy.")

st.markdown("---")

st.markdown("### 🔥 Stay Consistent, Stay Strong!")
st.markdown(
    """
    Track your progress, celebrate your wins, and keep pushing toward your goals.  
    Remember: **consistency beats perfection** — small efforts every day add up.
    """
)
