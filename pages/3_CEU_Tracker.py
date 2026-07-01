import streamlit as st

st.set_page_config(page_title="CEU Tracker", page_icon="🎓", layout="wide")

st.title("🎓 CEU Tracker")
st.write("Monitor CEU completion and training progress.")

completed = st.slider("Completed CEU hours", 0, 40, 12)
target = st.number_input("Target CEU hours", min_value=1, max_value=80, value=24)
progress = min(completed / target, 1.0)

st.progress(progress)
st.caption(f"{completed} / {target} hours complete")
