import streamlit as st
import requests
import logging
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:4000/system_admin"

st.title("Delete Exercise")

exercise_id = st.number_input("Exercise ID", min_value=1)

if st.button("Delete Exercise"):
    resp = requests.delete(f"{API_BASE}/exercise/{exercise_id}")
    if resp.status_code == 200:
        st.success("Exercise deleted.")
    else:
        st.error(resp.json())

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/00_Sys_Admin_Home.py")
