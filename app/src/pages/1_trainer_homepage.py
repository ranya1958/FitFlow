import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# sidebar links 
SideBarLinks()

st.title(f"Welcome Trainer, {st.session_state['first_name']}.")
st.write("")
st.write("### What would you like to do today?")

# Create Workout Template
if st.button("Create Workout Templates", use_container_width=True):
    st.switch_page("pages/3_trainer_workout_templates.py")

# Assign Workout to Client
if st.button("Assign Workout to Client", use_container_width=True):
    st.switch_page("pages/4_trainer_client_programs.py")

# Track Client Progress
if st.button("Track Client Progress", use_container_width=True):
    st.switch_page("pages/5_trainer_client_logs.py")