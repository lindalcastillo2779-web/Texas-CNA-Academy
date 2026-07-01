import streamlit as st

st.set_page_config(page_title="Staffing Compliance", page_icon="🏥", layout="wide")

st.title("🏥 Staffing Compliance")
st.write("Use this page to monitor staffing readiness and compliance checkpoints.")

st.metric("Open shifts", 6)
st.metric("Staff with expiring credentials", 2)
st.metric("Compliance completion", "84%")

st.warning("Connect real staffing data source for production use.")
