import streamlit as st

st.set_page_config(
    page_title="Texas CNA Academy",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PRIMARY = "#008080"
BG = "#F4F7F6"
CARD = "#E0F2F1"
TEXT = "#1A365D"

HHSC_URL = "https://www.hhs.texas.gov/"
RESOURCES_URL = "https://www.hhs.texas.gov/providers/long-term-care-providers"
CONTACT_URL = "mailto:info@texascnaacademyapp.com"
PRIVACY_URL = "#"

st.markdown(f"""
<style>
:root {{
  --primary: {PRIMARY};
  --bg: {BG};
  --card: {CARD};
  --text: {TEXT};
}}
html, body, [class*="css"] {{
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
.stApp {{
  background: var(--bg);
}}
.hero {{
  background: linear-gradient(135deg, var(--primary), #0d9488);
  color: white;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}}
.card {{
  background: var(--card);
  border-radius: 12px;
  padding: 1rem;
  color: var(--text);
  height: 100%;
}}
.footer-links a {{
  color: var(--primary);
  text-decoration: none;
  margin-right: 1rem;
}}
</style>
""", unsafe_allow_html=True)

if "route" not in st.session_state:
    st.session_state.route = "home"


def go(route_name: str):
    st.session_state.route = route_name


st.markdown("""
<div class="hero">
  <h1>Texas CNA Academy</h1>
  <p>Train smarter, renew confidently, and support your team with Texas-focused CNA education and compliance tools.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-links">
  <a href="https://www.hhs.texas.gov/" target="_blank">Texas HHSC</a>
  <a href="https://www.hhs.texas.gov/providers/long-term-care-providers" target="_blank">Long-Term Care Resources</a>
  <a href="mailto:info@texascnaacademyapp.com">Contact</a>
  <a href="#">Privacy</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height: 0.5rem"></div>', unsafe_allow_html=True)
cols = st.columns(5, gap="small")
with cols[0]:
    if st.button("Texas CNA Academy", key="student_btn"):
        go("student_onboarding")
with cols[1]:
    if st.button("I am a Certified Nursing Assistant", key="cna_btn"):
        go("cna_center")
with cols[2]:
    if st.button("CEUs &amp; License Renewal", key="ceu_btn"):
        go("ceu_renewal")
with cols[3]:
    if st.button("Instructors", key="instructors_btn"):
        go("instructor_portal")
with cols[4]:
    if st.button("Director of Nursing &amp; Facility Staff", key="don_btn"):
        go("facility_dashboard")

route = st.session_state.route

if route == "home":
    st.markdown('<div style="height: 0.5rem"></div>', unsafe_allow_html=True)
    value_cols = st.columns(5, gap="medium")
    values = [
        ("Compassion", "Putting the heart in healthcare by treating every resident, student, and colleague with deep empathy and kindness."),
        ("Dedication", "Remaining steadfastly committed to the growth, success, and continuous education of Texas caregivers."),
        ("Excellence", "Setting the highest standard for CNA training, clinical skills, and professional compliance."),
        ("Integrity", "Operating with absolute honesty, transparency, and accountability to remain a trusted resource for Texas state standards."),
        ("Community", "Building a supportive network that bridges the gap between students, working CNAs, instructors, and healthcare facilities."),
    ]
    for col, (title, desc) in zip(value_cols, values):
        with col:
            st.markdown(f"""
            <div class="card">
              <h4>{title}</h4>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height: 0.5rem"></div>', unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3, gap="medium")
    testimonials = [
        (
            "The Aspiring CNA (Student)",
            '"The videos and practice quizzes made studying for my Texas state exam so simple. The skills check-off list was my Bible, and I passed on my very first try!" — Sarah M., Future CNA',
        ),
        (
            "The Active CNA (License Renewal)",
            '"I was so stressed about my license expiring, but this app guided me through the exact Texas HHSC steps and let me finish my CEUs on my phone between shifts." — David R., Certified Nursing Assistant',
        ),
        (
            "The Director of Nursing (Facility Hub)",
            '"Managing compliance used to be a nightmare of spreadsheets. Now, I can monitor all of my CNAs\' licenses and CEU hours from one single dashboard." — Elena V., RN, Director of Nursing',
        ),
    ]
    for col, (title, quote) in zip([t1, t2, t3], testimonials):
        with col:
            st.markdown(f"""
            <div class="card">
              <h4>{title}</h4>
              <p>{quote}</p>
            </div>
            """, unsafe_allow_html=True)

elif route == "student_onboarding":
    st.subheader("Student Onboarding &amp; Training Catalog")
    st.write("Build this page in `/pages/01_student_onboarding.py` with modules, videos, flashcards, quizzes, and downloadable skills check-off lists.")
elif route == "cna_center":
    st.subheader("Active CNA Resource Center")
    st.write("Build this page with quick links, compliance reminders, shift-friendly mobile tools, and advancement resources.")
elif route == "ceu_renewal":
    st.subheader("CEUs &amp; License Renewal")
    st.write("Build this page with CEU tracking, approved course links, and a license recovery step-by-step wizard.")
elif route == "instructor_portal":
    st.subheader("Instructor Portal")
    st.write("Build this page for cohort management, student progress, attendance, and skills validation.")
elif route == "facility_dashboard":
    st.subheader("Director of Nursing &amp; Facility Staff Dashboard")
    st.write("Build this page for license monitoring, CEU milestones, staff compliance alerts, and exports.")

st.markdown(f"""
<hr>
<small style="color:{TEXT};">Texas CNA Academy • Educational support tool. Always verify requirements with Texas HHSC.</small>
""", unsafe_allow_html=True)
