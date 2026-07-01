import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Texas CNA Academy",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css() -> None:
    css_path = Path("styles/theme.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def hero_section() -> None:
    st.markdown(
        """
        <div class="hero">
            <div>
                <p class="eyebrow">Texas CNA Academy</p>
                <h1>Exam prep, renewal readiness, CEU tracking, and staffing compliance — in one mobile-friendly app.</h1>
                <p class="subtext">
                    Built for Texas nurse aide students, active CNAs, and nursing home DONs.
                    Learn faster, stay compliant, and reduce last-minute renewal stress.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Start Exam Prep", use_container_width=True):
            st.switch_page("pages/1_Exam_Prep.py")
    with col2:
        if st.button("Track CEUs", use_container_width=True):
            st.switch_page("pages/3_CEU_Tracker.py")
    with col3:
        st.caption("Tip: Replace demo videos with your official academy lessons.")


def feature_cards() -> None:
    st.markdown("## Core Learning & Compliance Modules")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="card">
                <h3>📝 Exam Prep</h3>
                <p>Practice workflows, topic checklists, and confidence-building study plans.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="card">
                <h3>🎓 CEU Tracker</h3>
                <p>Monitor progress toward annual CEU goals with quick status views.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
                <h3>✅ Renewal Readiness</h3>
                <p>Stay ahead of deadlines with a guided renewal checklist and reminders.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="card">
                <h3>🏥 Staffing Compliance</h3>
                <p>Support DON workflows with staffing and documentation readiness tools.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def media_section() -> None:
    st.markdown("## Video Learning Library")
    st.write("Use hosted videos for best speed and mobile playback.")

    tab1, tab2, tab3 = st.tabs(["Skills Demo", "Renewal Walkthrough", "Compliance Brief"])

    with tab1:
        st.video("https://www.youtube.com/watch?v=H14bBuluwB8")
        st.caption("Replace with your CNA skills demonstration lesson.")

    with tab2:
        st.video("https://www.youtube.com/watch?v=ysz5S6PUM-U")
        st.caption("Replace with your Texas renewal process walkthrough.")

    with tab3:
        st.video("https://www.youtube.com/watch?v=jNQXAC9IVRw")
        st.caption("Replace with your staffing compliance update brief.")


def infographic_placeholders() -> None:
    st.markdown("## Visual Workflow Guides")
    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "assets/images/renewal-workflow-placeholder.svg",
            caption="Renewal workflow infographic placeholder",
            use_container_width=True,
        )
    with col2:
        st.image(
            "assets/images/compliance-workflow-placeholder.svg",
            caption="Compliance workflow infographic placeholder",
            use_container_width=True,
        )


def footer_note() -> None:
    st.markdown("---")
    st.caption(
        "Template starter: optimize uploaded visuals as WebP and keep lesson videos hosted for performance."
    )


load_css()
hero_section()
feature_cards()
media_section()
infographic_placeholders()
footer_note()
