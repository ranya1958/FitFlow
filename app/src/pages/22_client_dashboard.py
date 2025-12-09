import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from modules.nav import SideBarLinks
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Your Dashboard", page_icon="📊", layout="wide")
SideBarLinks()

# ---------- BASIC SESSION SETUP ----------
if "client_id" not in st.session_state:
    st.session_state.client_id = 1

BASE_URL = "http://web-api:4000"

# Preload workout logs for highlights and reuse across sections
logs_data = []
data_error = None
try:
    resp = requests.get(
        f"{BASE_URL}/client/client_workout_log",
        params={"client_id": st.session_state.client_id},
        timeout=5,
    )
    if resp.status_code == 200:
        logs_data = resp.json()
    else:
        data_error = "Failed to load workouts from API"
except Exception as e:
    data_error = f"Error connecting to API: {str(e)}"

# Base dataframe + quick stats
df = pd.DataFrame(logs_data) if logs_data else pd.DataFrame()
completed_count = (df["completion_status"] == "completed").sum() if not df.empty else 0
total_sessions = len(df)
avg_duration = df["duration_minutes"].mean() if not df.empty else 0
total_time = df["duration_minutes"].sum() if not df.empty else 0
latest_status_raw = (
    df.iloc[0]["completion_status"] if not df.empty and "completion_status" in df else "n/a"
)
latest_status = str(latest_status_raw).replace("_", " ").title()

# ---------- GLOBAL STYLING / THEME ----------
st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(circle at 20% 20%, rgba(255,77,79,0.05), transparent 25%), radial-gradient(circle at 80% 0%, rgba(16,185,129,0.05), transparent 24%), linear-gradient(135deg, #fdfefe 0%, #f4f6fb 48%, #eef4fb 100%); }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    .stat-card { padding: 0.85rem 1rem; border-radius: 0.85rem; background: rgba(255, 255, 255, 0.92); border: 1px solid rgba(0, 0, 0, 0.05); box-shadow: 0 8px 28px rgba(0,0,0,0.08); }
    .section-card { padding: 1.2rem 1.4rem; border-radius: 1rem; background: rgba(255, 255, 255, 0.95); border: 1px solid rgba(0, 0, 0, 0.06); box-shadow: 0 12px 32px rgba(0,0,0,0.08); margin-bottom: 1.2rem; }
    .hero-title { font-size: 1.9rem; font-weight: 800; margin-bottom: 0.1rem; color: #0f172a; }
    .hero-subtitle { font-size: 1rem; color: #374151; }
    .accent-pill { display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; font-weight:600; color:#0f172a; background: linear-gradient(120deg, rgba(255,77,79,0.16), rgba(251,191,36,0.16)); border:1px solid rgba(255,77,79,0.22); }
    .highlight-card { padding: 0.95rem 1rem; border-radius: 0.85rem; color: #0f172a; border: 1px solid rgba(0,0,0,0.04); box-shadow: 0 10px 24px rgba(0,0,0,0.08); }
    .highlight-red { background: linear-gradient(135deg, rgba(255,77,79,0.15), rgba(255,77,79,0.05)); }
    .highlight-amber { background: linear-gradient(135deg, rgba(251,191,36,0.18), rgba(251,191,36,0.05)); }
    .highlight-green { background: linear-gradient(135deg, rgba(16,185,129,0.16), rgba(16,185,129,0.05)); }
    .highlight-label { font-size: 0.9rem; color: #374151; }
    .highlight-value { font-size: 1.6rem; font-weight: 800; }
    .highlight-sub { font-size: 0.9rem; color: #0f172a; }
    .stMetric label, .stMetric span { color: #0f172a !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HERO HEADER ----------
with st.container():
    st.markdown(
        """
        <div class="section-card">
            <div class="hero-title">📊 Your Workout Dashboard</div>
            <div class="hero-subtitle">
                Track your training history, see trends, and celebrate your progress.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Little “welcome back” toast style message
st.info("💪 Welcome back! Here’s a quick pulse on your training.")

# Colorful highlight row to add energy and remove empty space
h1, h2, h3 = st.columns(3)
with h1:
    st.markdown(
        f"""
        <div class="highlight-card highlight-red">
            <div class="highlight-label">Completed Sessions</div>
            <div class="highlight-value">{completed_count}</div>
            <div class="highlight-sub">Red means reps in the bank.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with h2:
    st.markdown(
        f"""
        <div class="highlight-card highlight-amber">
            <div class="highlight-label">Avg Duration</div>
            <div class="highlight-value">{avg_duration:.0f} min</div>
            <div class="highlight-sub">Steady burn. Yellow for focus.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with h3:
    st.markdown(
        f"""
        <div class="highlight-card highlight-green">
            <div class="highlight-label">Latest Status</div>
            <div class="highlight-value">{latest_status}</div>
            <div class="highlight-sub">Green keeps the momentum.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# =========================================================
# SECTION 1: RECENT WORKOUT LOGS + DURATION TRENDS
# =========================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📋 Recent Completed Workouts")

    if data_error:
        st.error(data_error)
        st.info("Make sure your Flask API is running on http://localhost:4000")
    elif not df.empty:
        df["workout_date"] = pd.to_datetime(df["workout_date"]).dt.strftime(
            "%Y-%m-%d"
        )

        # Display table
        st.dataframe(
            df[
                [
                    "workout_date",
                    "workout_name",
                    "duration_minutes",
                    "completion_status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "workout_date": "Date",
                "workout_name": "Workout",
                "duration_minutes": "Duration (min)",
                "completion_status": "Status",
            },
        )

        # Quick stats below table
        st.markdown("#### Quick Statistics")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

        with stat_col1:
            st.markdown('<div class="stat-card" style="border-left:4px solid #ff4d4f;">', unsafe_allow_html=True)
            st.metric("Total Workouts", total_sessions)
            st.markdown("</div>", unsafe_allow_html=True)

        with stat_col2:
            st.markdown('<div class="stat-card" style="border-left:4px solid #fbbf24;">', unsafe_allow_html=True)
            st.metric("Avg Duration", f"{avg_duration:.0f} min")
            st.markdown("</div>", unsafe_allow_html=True)

        with stat_col3:
            st.markdown('<div class="stat-card" style="border-left:4px solid #10b981;">', unsafe_allow_html=True)
            st.metric("Total Time", f"{total_time:.0f} min")
            st.markdown("</div>", unsafe_allow_html=True)

        with stat_col4:
            st.markdown('<div class="stat-card" style="border-left:4px solid #3b82f6;">', unsafe_allow_html=True)
            st.metric("Completed", completed_count)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No completed workouts yet. Start logging to see your progress!")

    # Little celebration button (non-destructive, fun for demo)
    if completed_count > 0:
        if st.button("🎉 Celebrate my consistency!", key="celebrate_consistency"):
            st.success(f"Nice work! You've completed {completed_count} workouts! 🙌")
            st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 Duration Trends")

    # Create a simple chart of workout durations
    if not df.empty:
        # Only use last 10 sessions
        chart_df = df.sort_values("workout_date").tail(10)

        fig = px.line(
            chart_df,
            x="workout_date",
            y="duration_minutes",
            title="Recent Workout Durations",
            markers=True,
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Duration (min)",
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Log some workouts to see duration trends here.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# SECTION 2: MONTHLY COMPLETION COMPARISON
# =========================================================
st.subheader("📊 Monthly Workout Comparison")

col_a, col_b = st.columns([3, 2])

monthly_df = pd.DataFrame()

with col_a:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    try:
        response = requests.get(
            f"{BASE_URL}/client/client_workout_log/completion_rate/monthly",
            params={"client_id": st.session_state.client_id},
            timeout=5,
        )

        if response.status_code == 200:
            monthly_data = response.json()

            if monthly_data:
                monthly_df = pd.DataFrame(monthly_data)

                # Create bar chart
                fig = px.bar(
                    monthly_df,
                    x="month",
                    y="workouts_completed",
                    title="Workouts Completed by Month",
                    labels={"month": "Month", "workouts_completed": "Workouts"},
                    color="workouts_completed",
                    color_continuous_scale=["#ff4d4f", "#fbbf24", "#10b981"],
                    text="workouts_completed",
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data for monthly comparison yet")
        else:
            st.error("Failed to load monthly data from API")
    except Exception as e:
        st.error(f"Error loading monthly data: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### Monthly Breakdown")

    if not monthly_df.empty:
        # Add month names
        month_names = {
            10: "October",
            11: "November",
            12: "December",
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
        }
        monthly_df["month_name"] = monthly_df["month"].map(month_names)

        st.dataframe(
            monthly_df[["month_name", "workouts_completed"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "month_name": "Month",
                "workouts_completed": "Workouts",
            },
        )

        # Show comparison if we have at least 2 months
        if len(monthly_df) >= 2:
            current_month = monthly_df.iloc[0]["workouts_completed"]
            previous_month = monthly_df.iloc[1]["workouts_completed"]
            change = int(current_month - previous_month)

            st.metric(
                "This Month vs Last Month",
                f"{int(current_month)} workouts",
                delta=f"{change:+d} workouts",
                delta_color="normal",
            )

            # Fun contextual message
            if change > 0:
                st.success(
                    f"🎉 Great job! You increased your workout count by {change}!"
                )
            elif change < 0:
                st.warning(
                    f"You completed {abs(change)} fewer workouts. Let's get back on track!"
                )
            else:
                st.info("You maintained the same workout count. Consistency is key!")

        # Mini progress animation (for demo: shows a “progress boost”)
        if len(monthly_df) > 0:
            latest = int(monthly_df.iloc[0]["workouts_completed"])
            max_target = max(latest, 10)  # arbitrary demo target

            st.markdown("#### Progress Boost 🔄")
            progress_bar = st.progress(0)
            text_box = st.empty()

            for i in range(0, 101, 10):
                progress_bar.progress(i)
                # Simple message that feels “alive”
                text_box.text(
                    f"Building your monthly progress… {int(i)}%"
                )
                time.sleep(0.03)

            text_box.text(
                f"You're at {latest} workouts this month (target ~{max_target})"
            )

    else:
        st.caption("Once you log workouts across months, you'll see a breakdown here.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# SECTION 3: NAVIGATION BUTTONS
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("pages/21_Client_home.py")

with col2:
    if st.button("📝 Log a Workout", use_container_width=True):
        st.switch_page("pages/23_client_log_workout.py")

with col3:
    if st.button("🎯 View My Program", use_container_width=True):
        st.switch_page("pages/24_client_my_program.py")
