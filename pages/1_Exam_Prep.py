import streamlit as st

st.set_page_config(page_title="Exam Prep", page_icon="📝", layout="wide")

st.title("📝 Exam Prep")
st.write("Use this page for practice questions, topic drills, and skill checklists.")

with st.expander("Starter content ideas", expanded=True):
    st.markdown(
        """
        - Daily practice quiz bank
        - CNA skills checklist by category
        - Weak-topic tracker
        - 7-day readiness sprint
        """
    )
