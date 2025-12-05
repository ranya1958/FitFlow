import streamlit as st
from streamlit_assests.app_logo import add_logo
import requests

st.set_page_config(
    page_title="Chester's Portal",
    page_icon="💪",
    layout="wide"
)

# Get client info from session state
if 'client_id' not in st.session_state:
    st.session_state.client_id = 1
if 'client_name' not in st.session_state:
    st.session_state.client_name = "Chester Stone"

# Header
st.title("💪 Welcome to Your Fitness Portal")
st.markdown(f"### Hello, {st.session_state.client_name}!")

st.markdown("---")

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## Your Training Hub
    
    Welcome to your personal fitness tracking portal! Here you can:
    
    - 📊 **View Your Dashboard** - See your recent workouts and progress at a glance
    - 📝 **Log Workouts** - Record your training sessions with notes
    - 🎯 **Check Your Program** - View your coach-assigned workout plan
    
    Use the sidebar to navigate between different sections of your portal.
    """)
    
    st.info("💡 **Tip:** Make sure to log your workouts consistently to track your progress!")

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
                import pandas as pd
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
st.markdown("### Quick Access")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 📊 Dashboard
    View your recent workout history and see how you're progressing month over month.
    """)
    if st.button("Go to Dashboard →", use_container_width=True):
        st.switch_page("pages/31_Chester_Dashboard.py")

with col2:
    st.markdown("""
    #### 📝 Log Workout
    Record a new training session with duration, notes, and completion status.
    """)
    if st.button("Log Workout →", use_container_width=True):
        st.switch_page("pages/32_Chester_Log_Workout.py")

with col3:
    st.markdown("""
    #### 🎯 My Program
    View your coach-assigned workout program with all exercise details.
    """)
    if st.button("View Program →", use_container_width=True):
        st.switch_page("pages/33_Chester_My_Program.py")

st.markdown("---")

# Motivational section
st.markdown("### 🔥 Stay Consistent, Stay Strong!")
st.markdown("""
Track your progress, celebrate your wins, and keep pushing toward your goals. 
Remember: **consistency beats perfection!**
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>FitFlow © 2025 | Track. Train. Transform.</p>
</div>
""", unsafe_allow_html=True)