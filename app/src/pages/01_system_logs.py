import streamlit as st
import requests

API_BASE = "http://localhost:4000/system_admin"

st.title("System Logs")

action_filter = st.text_input("Filter by action_type (optional): e.g., FLAG_EXERCISE")

if st.button("Load Logs"):
    if action_filter:
        url = f"{API_BASE}/system_logs/{action_filter}"
    else:
        url = f"{API_BASE}/system_logs"

    response = requests.get(url)

    if response.status_code == 200:
        logs = response.json()
        st.dataframe(logs)
    else:
        st.error("Failed to load logs.")