import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Welcome System Administrator!")
st.write("### What would you like to do today?")

# --- BUTTON NAVIGATION ---
if st.button("View System Logs", use_container_width=True):
    st.switch_page("pages/01_system_logs.py")

if st.button("View Backup Logs & Status", use_container_width=True):
    st.switch_page("pages/02_backup_logs.py")

if st.button("Create a New User", use_container_width=True):
    st.switch_page("pages/03_create_user.py")

if st.button("Create Trainer Profile", use_container_width=True):
    st.switch_page("pages/04_create_trainer.py")

if st.button("Create Client Profile", use_container_width=True):
    st.switch_page("pages/05_create_client.py")

if st.button("Update Exercise", use_container_width=True):
    st.switch_page("pages/06_update_exercise.py")

if st.button("Delete Exercise", use_container_width=True):
    st.switch_page("pages/07_delete_exercise.py")

if st.button("Manage User Permissions", use_container_width=True):
    st.switch_page("pages/08_manage_permissions.py")
