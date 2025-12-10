import streamlit as st
import requests
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="FitFlow | Client Portal",
    page_icon="💪",
    layout="wide"
)

# Configure paths to static assets (logo, etc.)
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
LOGO_PATH = ASSETS_DIR / "fitflow_logo.jpg"

# Sidebar branding
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_column_width=True)
    st.markdown("### FitFlow Client Portal")
    st.markdown("---")

# Get client info from session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = 1
if 'client_name' not in st.session_state:
    st.session_state.client_name = "Chester Stone"

# Header
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=220)
st.title("Welcome to Your FitFlow Portal 💪")
st.markdown(f"### Hey, {st.session_state.client_name}! 👋")

st.markdown(
    """
    Track your workouts, follow your program, and stay on top of your goals — all in one place.
    """
)
st.markdown("---")

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        ## Your Training Hub
        
        Welcome to your personal FitFlow portal! Here you can:
        
        - 📊 **View Your Dashboard** – See your recent workouts and progress at a glance  
        - 📝 **Log Workouts** – Record your training sessions with notes  
        - 🎯 **Check Your Program** – View your coach-assigned workout plan  
        
        Use the sidebar or the quick actions below to jump to what you need.
        """
    )
    
    st.info("💡 **Tip:** Logging your workouts consistently is the fastest way to see your progress over time!")

with col2:
    st.markdown("### Quick Stats")
    
    # Fetch quick stats from API
    try:
        response = requests.get(
            f"http://localhost:4000/client/client_workout_log",
            params={"client_id": st.session_state.client_id}
        )
        
        if response.status_code == 200:
            logs = response.json()
            
            st.metric("Total Workouts Logged", len(logs))
            
            if logs:
                df = pd.DataFrame(logs)
                avg_duration = df['duration_minutes'].mean()
                st.metric("Avg Workout Duration", f"{avg_duration:.0f} min")
            else:
                st.metric("Avg Workout Duration", "0 min")
        else:
            st.warning("Unable to load stats")
    except:
        st.warning("API connection unavailable")

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
    if st.button("Go to Dashboard →", use_container_width=True):
        st.switch_page("pages/Client_Dashboard.py")

with col2:
    st.markdown(
        """
        #### 📝 Log Workout
        Record a new training session with duration, notes, and completion status.
        """
    )
    if st.button("Log Workout →", use_container_width=True):
        st.switch_page("pages/Client_Log_Workout.py")

with col3:
    st.markdown(
        """
        #### 🎯 My Program
        View your coach-assigned workout program with all exercise details.
        """
    )
    if st.button("View Program →", use_container_width=True):
        st.switch_page("pages/Client_My_Program.py")

st.markdown("---")

# Motivational section
st.markdown("### 🔥 Stay Consistent, Stay Strong!")
st.markdown(
    """
    Track your progress, celebrate your wins, and keep pushing toward your goals.  
    Remember: **consistency beats perfection** — small efforts every day add up.
    """
)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>FitFlow © 2025 | Track. Train. Transform.</p>
</div>
""", unsafe_allow_html=True)