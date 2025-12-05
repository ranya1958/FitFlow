import streamlit as st
import requests

API_BASE = "http://localhost:4000/system_admin"

st.title("Backup Logs")

if st.button("View All Backups"):
    resp = requests.get(f"{API_BASE}/backup_logs")
    st.dataframe(resp.json())

st.write("---")
st.subheader("Backup Status (Is Backup Due?)")

if st.button("Check Backup Status"):
    resp = requests.get(f"{API_BASE}/backup_logs/status")
    st.json(resp.json())