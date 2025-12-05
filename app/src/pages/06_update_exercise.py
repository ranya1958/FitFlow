import streamlit as st
import requests

API_BASE = "http://localhost:4000/system_admin"

st.title("Update Exercise")

exercise_id = st.number_input("Exercise ID", min_value=1)
name = st.text_input("New Name")
desc = st.text_area("New Description")
cat = st.text_input("New Category")

if st.button("Update Exercise"):
    payload = {}

    if name: payload["name"] = name
    if desc: payload["description"] = desc
    if cat: payload["category"] = cat

    resp = requests.put(f"{API_BASE}/exercise/{exercise_id}", json=payload)

    if resp.status_code == 200:
        st.success("Exercise updated!")
    else:
        st.error(resp.json())
