import streamlit as st
import requests

API_BASE = "http://localhost:4000/system_admin"

st.title("Create User Account")

email = st.text_input("Email")
password = st.text_input("Password", type="password")
role = st.selectbox("Role", ["trainer", "client", "analyst", "admin"])
permissions = st.text_input("Permissions (comma-separated)")
created_by = st.number_input("Created by (System Admin ID)", min_value=1)

if st.button("Create User"):
    payload = {
        "email": email,
        "password_hash": password,
        "role": role,
        "permissions": permissions,
        "created_by": created_by
    }

    resp = requests.post(f"{API_BASE}/user", json=payload)

    if resp.status_code == 201:
        st.success("User created!")
        st.json(resp.json())
    else:
        st.error(resp.json())
