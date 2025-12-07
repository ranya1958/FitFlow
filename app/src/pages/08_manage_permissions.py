import streamlit as st
import requests
import logging
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:4000/system_admin"

st.title("Manage Permissions for User Roles")

role = st.selectbox("Choose Role", ["trainer", "client", "analyst", "admin"])
new_permissions = st.text_input("New Permissions (comma-separated)")

if st.button("Update Permissions"):
    payload = {
        "role": role,
        "new_permissions": new_permissions,
    }

    resp = requests.put(f"{API_BASE}/user/permissions", json=payload)

    if resp.status_code == 200:
        st.success(f"Permissions updated for all {role} users.")
    else:
        st.error(resp.json())
