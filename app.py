import streamlit as st
import pandas as pd
import html
from datetime import date, timedelta

st.set_page_config(
    page_title="TULIP-Link CNA Academy",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
:root{
    --bg:#f5f7fb;
    --surface:#ffffff;
    --surface-2:#f8fafc;
    --surface-3:#eef6ff;
    --text:#16253d;
    --muted:#5c6b82;
    --primary:#1d74d7;
    --primary-dark:#0d4f9b;
    --orange:#ff7a1a;
    --orange-soft:#fff1e7;
    --green:#1ca35d;
    --green-soft:#e8fbef;
    --blue-soft:#e8f2ff;
    --danger:#c2410c;
    --danger-soft:#fff0ea;
    --warning:#b45309;
    --warning-soft:#fff4d6;
    --info:#0f5db4;
    --info-soft:#e7f1ff;
    --border:#dce5f0;
    --shadow:0 18px 42px rgba(21,42,73,.08);
    --shadow-hover:0 24px 48px rgba(21,42,73,.14);
    --radius:22px;
    --radius-sm:12px;
}
html, body, [class*="css"] {
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
    color:var(--text);
}
body { background:var(--bg); }
.block-container {
    padding-top:1rem;
    padding-bottom:4rem;
    max-width:1280px;
}
.stApp{
    background:
        radial-gradient(circle at top left, rgba(255,122,26,.10), transparent 24%),
        radial-gradient(circle at top right, rgba(29,116,215,.10), transparent 28%),
        var(--bg);
}
.main-hero{
    background:linear-gradient(135deg,#ffffff 0%,#f7fbff 58%,#eef6ff 100%);
    color:var(--text);
    border-radius:var(--radius);
    padding:1.5rem 1.5rem;
    box-shadow:var(--shadow);
    border:1px solid rgba(29,116,215,.10);
    margin-bottom:1.2rem;
}
.eyebrow{
    display:inline-flex;
    align-items:center;
    gap:.45rem;
    border-radius:999px;
    background:var(--orange-soft);
    color:var(--orange);
    padding:.36rem .72rem;
    font-size:.8rem;
    font-weight:800;
    letter-spacing:.08em;
    text-transform:uppercase;
}
.hero-title{
    font-size:2.35rem;
    line-height:1.12;
    margin:.9rem 0 .55rem;
    font-weight:800;
}
.hero-copy{
    color:var(--muted);
    font-size:1.02rem;
    line-height:1.65;
    max-width:760px;
}
.hero-highlights{
    display:flex;
    flex-wrap:wrap;
    gap:.75rem;
    margin-top:1.1rem;
}
.hero-chip{
    display:inline-flex;
    align-items:center;
    gap:.45rem;
    padding:.6rem .88rem;
    border-radius:16px;
    background:#fff;
    border:1px solid var(--border);
    color:var(--text);
    font-weight:600;
}
.breadcrumb-bar{
    display:flex;
    align-items:center;
    gap:.45rem;
    color:var(--muted);
    font-size:.9rem;
    font-weight:600;
    margin:0 0 .8rem .2rem;
}
.card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1.15rem;
    box-shadow:var(--shadow);
    margin-bottom:1.15rem;
}
.soft-card{
    background:var(--surface-2);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.interactive-card{
    transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.interactive-card:hover{
    transform:translateY(-4px);
    box-shadow:var(--shadow-hover);
    border-color:rgba(29,116,215,.24);
}
.info-card{
    background:linear-gradient(135deg,#f8fbff 0%,#eef6ff 100%);
    border:1px solid #cfe1fb;
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.metric-card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    box-shadow:var(--shadow);
    text-align:center;
    min-height:122px;
}
.kpi{
    color:var(--primary);
    font-size:2rem;
    font-weight:800;
}
.label{
    color:var(--muted);
    font-size:.92rem;
}
.badge{
    display:inline-block;
    padding:.34rem .72rem;
    border-radius:999px;
    font-size:.82rem;
    font-weight:700;
}
.badge-green{background:var(--green-soft);color:var(--green);}
.badge-red{background:var(--danger-soft);color:var(--danger);}
.badge-amber{background:var(--warning-soft);color:var(--warning);}
.badge-blue{background:var(--info-soft);color:var(--info);}
.badge-orange{background:var(--orange-soft);color:var(--orange);}
.critical{
    color:var(--danger);
    font-weight:800;
}
.check-step{
    background:#fff;
    border:1px solid var(--border);
    border-radius:var(--radius-sm);
    padding:.75rem .85rem;
    margin-bottom:.45rem;
}
.sms-box{
    background:#111827;
    color:#f9fafb;
    border-radius:var(--radius-sm);
    padding:.95rem;
    font-family:Consolas,monospace;
    font-size:.9rem;
}
.footer-note{
    color:var(--muted);
    font-size:.9rem;
}
.small-muted{
    color:var(--muted);
    font-size:.88rem;
}
.progress-shell{
    background:linear-gradient(180deg,#fff 0%,#f8fbff 100%);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem 1.1rem;
    margin-bottom:1rem;
    box-shadow:var(--shadow);
}
.progress-head{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:1rem;
    margin-bottom:.7rem;
}
.progress-percent{
    font-size:2.25rem;
    font-weight:800;
    color:var(--primary-dark);
    line-height:1;
}
.progress-copy{
    color:var(--muted);
    font-size:.94rem;
}
.course-thumb{
    height:88px;
    border-radius:18px;
    background:linear-gradient(135deg,#1d74d7 0%,#42a1ff 55%,#7ec9ff 100%);
    color:#fff;
    display:flex;
    align-items:flex-end;
    justify-content:flex-start;
    padding:1rem;
    font-size:1.65rem;
    font-weight:800;
    margin-bottom:.9rem;
}
.course-card-title{
    font-size:1.06rem;
    font-weight:800;
    margin:.7rem 0 .35rem;
}
.course-card-copy{
    color:var(--muted);
    min-height:3.4rem;
    line-height:1.55;
    font-size:.93rem;
}
.mini-progress{
    width:100%;
    height:10px;
    background:#e7eef7;
    border-radius:999px;
    overflow:hidden;
    margin:.85rem 0 .45rem;
}
.mini-progress > span{
    display:block;
    height:100%;
    background:linear-gradient(90deg,var(--orange) 0%,#ff9d4d 48%,var(--green) 100%);
    border-radius:999px;
}
.course-card-meta{
    display:flex;
    justify-content:space-between;
    gap:.65rem;
    color:var(--muted);
    font-size:.85rem;
}
.quiz-shell{
    background:#fff;
    border:1px solid var(--border);
    border-radius:18px;
    padding:1rem;
    margin-bottom:.9rem;
}
.quiz-label{
    color:var(--primary);
    font-size:.82rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:.06em;
    margin-bottom:.4rem;
}
.pill-row{
    display:flex;
    flex-wrap:wrap;
    gap:.55rem;
    margin-bottom:.85rem;
}
.pill{
    display:inline-flex;
    align-items:center;
    gap:.4rem;
    background:#fff;
    border:1px solid var(--border);
    border-radius:999px;
    padding:.45rem .8rem;
    font-size:.87rem;
    color:var(--text);
    font-weight:600;
}
.section-title{
    font-size:1.35rem;
    font-weight:800;
    margin:0 0 .85rem;
}
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#f8fbff 0%,#eef5fc 100%);
    border-right:1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container{
    padding-top:1.15rem;
}
[data-testid="stSidebar"] .sidebar-brand{
    background:#fff;
    border:1px solid var(--border);
    border-radius:20px;
    padding:1rem;
    box-shadow:var(--shadow);
    margin-bottom:1rem;
}
[data-testid="stSidebar"] .sidebar-panel{
    background:#fff;
    border:1px solid var(--border);
    border-radius:18px;
    padding:.9rem 1rem;
    margin-top:1rem;
}
[data-testid="stSidebar"] .sidebar-panel p{
    color:var(--muted);
    margin-bottom:.3rem;
}
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stSelectbox > label{
    font-weight:700;
    color:var(--text);
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"]{
    gap:.5rem;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label{
    border:1px solid var(--border);
    background:#fff;
    border-radius:14px;
    padding:.55rem .7rem;
}
[data-testid="stSidebar"] .stButton button,
.stButton button{
    border-radius:14px;
    border:1px solid transparent;
    background:linear-gradient(135deg,var(--orange) 0%,#ff9d4d 100%);
    color:#fff;
    font-weight:700;
    box-shadow:none;
}
.stButton button:hover{
    border-color:transparent;
    color:#fff;
}
.stTabs [data-baseweb="tab-list"]{
    gap:.45rem;
    flex-wrap:wrap;
}
.stTabs [data-baseweb="tab"]{
    height:auto;
    padding:.55rem .9rem;
    background:#fff;
    border-radius:999px;
    border:1px solid var(--border);
}
.stTabs [aria-selected="true"]{
    color:var(--primary);
    border-color:rgba(29,116,215,.28);
    background:var(--info-soft);
}
div[data-testid="stProgressBar"] > div > div{
    background:#e5edf7;
    border-radius:999px;
}
div[data-testid="stProgressBar"] > div > div > div{
    background:linear-gradient(90deg,var(--orange) 0%,#ffa44c 45%,var(--green) 100%);
    border-radius:999px;
}
div[data-testid="stAlert"]{
    border-radius:16px;
}
div[data-testid="stDataFrame"]{
    border:1px solid var(--border);
    border-radius:var(--radius);
    overflow:hidden;
}
@media (max-width:768px){
    .block-container{padding-left:.8rem;padding-right:.8rem;}
    .hero-title{font-size:1.8rem;}
    .kpi,.progress-percent{font-size:1.55rem;}
    .progress-head,.course-card-meta{flex-direction:column;}
    .course-card-copy{min-height:auto;}
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
TODAY = date.today()
SCORE_THRESHOLD_ON_TRACK = 85
SCORE_THRESHOLD_BUILDING = 60

def esc(value):
    return html.escape(str(value))

def pct(value, total):
    if total == 0:
        return 0
    return max(0, min(100, int((value / total) * 100)))

def days_until_expiration(expiration_date: date):
    return (expiration_date - TODAY).days

def tulip_window_open_date(expiration_date: date):
    return expiration_date - timedelta(days=90)

def days_until_tulip_window(expiration_date: date):
    return (tulip_window_open_date(expiration_date) - TODAY).days

def status_from_expiration(expiration_date: date):
    return "RED" if days_until_expiration(expiration_date) <= 90 else "GREEN"

def compliance_snapshot(cna_id, expiration_date, ceu_records):
    recs = ceu_records[ceu_records["cna_id"] == cna_id]
    hours = int(recs["hours"].sum()) if not recs.empty else 0
    geriatric = bool(recs["geriatric_flag"].any()) if not recs.empty else False
    dementia = bool(recs["dementia_flag"].any()) if not recs.empty else False
    infection = bool(recs["infection_flag"].any()) if not recs.empty else False
    days_left = days_until_expiration(expiration_date)
    tulip_days = days_until_tulip_window(expiration_date)
    return {
        "hours": hours,
        "geriatric": geriatric,
        "dementia": dementia,
        "infection": infection,
        "days_left": days_left,
        "tulip_days": tulip_days
    }

def readiness_score(summary):
    score = 0
    if summary["hours"] >= 24:
        score += 35
    else:
        score += int((summary["hours"] / 24) * 35)
    if summary["geriatric"]:
        score += 15
    if summary["dementia"]:
        score += 15
    if summary["infection"]:
        score += 15
    if summary["days_left"] > 90:
        score += 20
    elif summary["days_left"] > 0:
        score += 10
    else:
        score += 0
    return max(0, min(100, score))

def missing_items(summary):
    items = []
    if summary["hours"] < 24:
        items.append(f"Complete {24 - summary['hours']} more in-service hours")
    if not summary["geriatric"]:
        items.append("Add geriatrics-related training record")
    if not summary["dementia"]:
        items.append("Add dementia / Alzheimer's-related training record")
    if not summary["infection"]:
        items.append("Confirm annual infection-control training")
    if summary["days_left"] <= 90:
        items.append("Begin or finish TULIP renewal submission now")
    else:
        items.append("Monitor countdown until 90-day TULIP window opens")
    return items

def milestone_label(score):
    if score >= SCORE_THRESHOLD_ON_TRACK:
        return "On track"
    if score >= SCORE_THRESHOLD_BUILDING:
        return "Building momentum"
    return "Needs attention"

def milestone_badge_class(score):
    if score >= SCORE_THRESHOLD_ON_TRACK:
        return "badge-green"
    if score >= SCORE_THRESHOLD_BUILDING:
        return "badge-orange"
    return "badge-blue"

def badge_class_for_category(category):
    palette = {
        "Infection Control": "badge-orange",
        "Resident Rights": "badge-blue",
        "Communication": "badge-green",
        "Safety": "badge-orange",
        "Transfers and Mobility": "badge-blue",
        "Vital Signs": "badge-green",
        "Elimination": "badge-orange",
        "Nutrition and Hydration": "badge-green",
        "Skin Care and Personal Care": "badge-blue",
        "Mental Health and Social Needs": "badge-green",
        "Restorative Care": "badge-orange",
        "Documentation and Reporting": "badge-blue"
    }
    return palette.get(category, "badge-blue")

def icon_for_category(category):
    icons = {
        "Infection Control": "🧼",
        "Resident Rights": "🫶",
        "Communication": "💬",
        "Safety": "🛡️",
        "Transfers and Mobility": "♿",
        "Vital Signs": "💓",
        "Elimination": "🧪",
        "Nutrition and Hydration": "🥗",
        "Skin Care and Personal Care": "🧴",
        "Mental Health and Social Needs": "🌤️",
        "Restorative Care": "🏃",
        "Documentation and Reporting": "📝"
    }
    return icons.get(category, "📘")

def render_breadcrumb(items):
    crumb_html = "".join(
        f"<span>{esc(item)}</span>" if idx == len(items) - 1 else f"<span>{esc(item)}</span><span>›</span>"
        for idx, item in enumerate(items)
    )
    st.markdown(f'<div class="breadcrumb-bar">{crumb_html}</div>', unsafe_allow_html=True)

def render_progress_summary(title, score, detail, badge_text, badge_class="badge-blue"):
    st.markdown(
        f"""
        <div class="progress-shell">
            <div class="progress-head">
                <div>
                    <div class="section-title">{esc(title)}</div>
                    <div class="progress-copy">{esc(detail)}</div>
                </div>
                <div style="text-align:right;">
                    <div class="progress-percent">{score}%</div>
                    <span class="badge {esc(badge_class)}">{esc(badge_text)}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_course_card(icon, badge_class, badge_text, title, description, meta_left, meta_right, progress=None, thumb_style=""):
    progress_html = ""
    if progress is not None:
        progress_html = f'<div class="mini-progress"><span style="width:{progress}%;"></span></div>'
    return f"""
        <div class="card interactive-card">
            <div class="course-thumb" style="{thumb_style}">{esc(icon)}</div>
            <span class="badge {esc(badge_class)}">{esc(badge_text)}</span>
            <div class="course-card-title">{esc(title)}</div>
            <div class="course-card-copy">{esc(description)}</div>
            {progress_html}
            <div class="course-card-meta">
                <span>{esc(meta_left)}</span>
                <span>{esc(meta_right)}</span>
            </div>
        </div>
    """

def make_5506_text(cna_row, facility_row, summary):
    return f"""
TEXAS FORM 5506-NAR MOCK PRE-FILL SUMMARY
=========================================

Form Purpose:
Texas Nurse Aide Registry Employment Verification

APPLICANT INFORMATION
Last Name: {cna_row['last_name']}
First Name: {cna_row['first_name']}
Middle Name:
Maiden Name:
Date of Birth: [Add manually]
Social Security Number: [Do not store in demo]
Email Address: [Add manually]
CNA Certificate Number: {cna_row['license_number']}
Phone Number: {cna_row['phone']}

EMPLOYER INFORMATION
Facility Name: {facility_row['facility_name']}
State License Number: {facility_row['state_license_number']}
Director of Nursing: {facility_row['don_name']}

RENEWAL SUPPORT SNAPSHOT
Last Renewal Date: {cna_row['last_renewal_date']}
Expiration Date: {cna_row['expiration_date']}
Days Until Expiration: {summary['days_left']}
TULIP Window Opens / Opened: {summary['tulip_days']} days from today (negative means already open)
Total In-Service Hours Logged: {summary['hours']}
Geriatrics Training Recorded: {"Yes" if summary["geriatric"] else "No"}
Dementia / Alzheimer's Training Recorded: {"Yes" if summary["dementia"] else "No"}
Annual Infection-Control Training Recorded: {"Yes" if summary["infection"] else "No"}

DON ACTIONS
- Verify employment and identity fields.
- Confirm in-service records and required topic coverage.
- Review timing of renewal activity in TULIP.
- Complete the official state form workflow as required.

NOTE
This is a workflow aid generated by CNA & TULIP-Link - Texas CNA Academy.
Use official Texas HHSC forms and TULIP for real submission.
""".strip()

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "flash_index": 0,
    "flash_flip": False,
    "flash_category": "All Categories",
    "flash_category_prev": "All Categories",
    "mastered_cards": set(),
    "review_cards": set(),
    "written_answers": {},
    "skills_answers": {},
    "skills_checks": {}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# DATA
# =========================================================
facility_df = pd.DataFrame([
    {
        "facility_id": 1,
        "facility_name": "Bluebonnet Skilled Nursing Center",
        "state_license_number": "TX-NF-44821",
        "don_name": "Monica Alvarez, RN"
    }
])

cna_df = pd.DataFrame([
    {
        "cna_id": 1,
        "first_name": "Jasmine",
        "last_name": "Carter",
        "phone": "(325) 555-0101",
        "license_number": "CNA-TX-102344",
        "last_renewal_date": TODAY - timedelta(days=500),
        "expiration_date": TODAY + timedelta(days=160),
        "user_type": "Active CNA"
    },
    {
        "cna_id": 2,
        "first_name": "Marco",
        "last_name": "Diaz",
        "phone": "(325) 555-0102",
        "license_number": "CNA-TX-204877",
        "last_renewal_date": TODAY - timedelta(days=640),
        "expiration_date": TODAY + timedelta(days=48),
        "user_type": "Critical Window CNA"
    },
    {
        "cna_id": 3,
        "first_name": "Aaliyah",
        "last_name": "Brooks",
        "phone": "(325) 555-0103",
        "license_number": "CNA-TX-318209",
        "last_renewal_date": TODAY - timedelta(days=700),
        "expiration_date": TODAY + timedelta(days=12),
        "user_type": "Critical Window CNA"
    },
    {
        "cna_id": 4,
        "first_name": "Ethan",
        "last_name": "Reed",
        "phone": "(325) 555-0104",
        "license_number": "STUDENT-001",
        "last_renewal_date": TODAY,
        "expiration_date": TODAY + timedelta(days=730),
        "user_type": "Student"
    }
])

ceu_df = pd.DataFrame([
    {"record_id": 1, "cna_id": 1, "course_title": "Resident Safety Essentials", "hours": 8, "geriatric_flag": True,  "dementia_flag": False, "infection_flag": False},
    {"record_id": 2, "cna_id": 1, "course_title": "Dementia Communication Basics", "hours": 8, "geriatric_flag": False, "dementia_flag": True,  "infection_flag": False},
    {"record_id": 3, "cna_id": 1, "course_title": "Infection Prevention Update", "hours": 10, "geriatric_flag": False, "dementia_flag": False, "infection_flag": True},
    {"record_id": 4, "cna_id": 2, "course_title": "Geriatric Skin Care", "hours": 6, "geriatric_flag": True,  "dementia_flag": False, "infection_flag": False},
    {"record_id": 5, "cna_id": 2, "course_title": "Lift & Transfer Safety", "hours": 4, "geriatric_flag": False, "dementia_flag": False, "infection_flag": False},
    {"record_id": 6, "cna_id": 3, "course_title": "Alzheimer's Support Foundations", "hours": 6, "geriatric_flag": False, "dementia_flag": True,  "infection_flag": False},
    {"record_id": 7, "cna_id": 3, "course_title": "Resident Rights Refresher", "hours": 5, "geriatric_flag": False, "dementia_flag": False, "infection_flag": False},
])

flashcards = [
    {"category": "Infection Control", "front": "Why should hand hygiene be done before and after caring for a resident?", "back": "It helps reduce the spread of germs and protects both the resident and the caregiver."},
    {"category": "Infection Control", "front": "What does PPE mean in nurse aide care?", "back": "PPE means personal protective equipment, such as gloves, gowns, masks, and face shields."},
    {"category": "Infection Control", "front": "When should gloves be used during resident care?", "back": "Gloves should be used when contact with blood, body fluids, mucous membranes, or contaminated items may happen."},
    {"category": "Infection Control", "front": "Why is it important to avoid touching the inside of the sink during handwashing?", "back": "Touching the sink can recontaminate clean hands."},
    {"category": "Infection Control", "front": "Why should a paper towel be used to shut off the faucet after washing hands?", "back": "Using a paper towel helps prevent clean hands from touching a contaminated faucet."},
    {"category": "Infection Control", "front": "Why should dirty linen be held away from your body?", "back": "Holding soiled linen away from your uniform lowers the chance of spreading contamination."},
    {"category": "Infection Control", "front": "What is the purpose of standard precautions?", "back": "Standard precautions are used with every resident to lower the risk of exposure to infection."},
    {"category": "Infection Control", "front": "Why should a CNA wash hands even after removing gloves?", "back": "Gloves are not perfect barriers, and germs may still be present after removal."},
    {"category": "Infection Control", "front": "Why must clean supplies stay separate from contaminated items?", "back": "Keeping them separate helps stop cross-contamination."},
    {"category": "Infection Control", "front": "Why should fingertips point downward while rinsing the hands?", "back": "This helps water flow away from cleaner areas and reduces contamination."},

    {"category": "Resident Rights", "front": "What does it mean to preserve a resident’s dignity?", "back": "It means treating the resident with respect, courtesy, and sensitivity."},
    {"category": "Resident Rights", "front": "Why should a CNA explain care before starting a task?", "back": "Explanation helps the resident understand what will happen and supports respectful care."},
    {"category": "Resident Rights", "front": "Why should the privacy curtain or door be closed during personal care?", "back": "It protects the resident’s privacy and dignity."},
    {"category": "Resident Rights", "front": "What is informed choice in resident care?", "back": "It means the resident has the right to receive information and take part in decisions."},
    {"category": "Resident Rights", "front": "Why should a CNA knock before entering a resident’s room?", "back": "Knocking shows respect for the resident’s privacy and space."},
    {"category": "Resident Rights", "front": "What should a CNA do if a resident says no to care?", "back": "The CNA should respect the refusal, stay calm, and report it according to policy."},
    {"category": "Resident Rights", "front": "Why must resident information be kept confidential?", "back": "Private health information must be protected from improper sharing."},
    {"category": "Resident Rights", "front": "Why should a resident be covered as much as possible during a bath?", "back": "Keeping the resident covered helps protect privacy, warmth, and dignity."},
    {"category": "Resident Rights", "front": "Why is choice important during daily care routines?", "back": "Allowing choice supports independence and person-centered care."},
    {"category": "Resident Rights", "front": "Why should a CNA speak directly to the resident instead of only to family members?", "back": "The resident remains the main person in the care interaction and deserves direct respect."},

    {"category": "Communication", "front": "How should a CNA talk with a resident who has hearing loss?", "back": "Face the resident, speak clearly, and reduce background noise when possible."},
    {"category": "Communication", "front": "Why is active listening important in CNA work?", "back": "Listening carefully helps the CNA understand needs, preferences, and possible problems."},
    {"category": "Communication", "front": "How should a CNA communicate with a resident who is confused?", "back": "Use short, calm, simple instructions and a reassuring tone."},
    {"category": "Communication", "front": "Why should a CNA avoid arguing with a disoriented resident?", "back": "Arguing can increase stress, fear, and confusion."},
    {"category": "Communication", "front": "What tone of voice is best during resident care?", "back": "A calm, respectful, and reassuring tone is best."},
    {"category": "Communication", "front": "Why is it important to report changes in a resident’s condition quickly?", "back": "Prompt reporting helps the nurse respond to potential problems sooner."},
    {"category": "Communication", "front": "What should a CNA do if a resident does not understand directions?", "back": "Repeat the directions slowly and use simpler wording if needed."},
    {"category": "Communication", "front": "Why should a CNA introduce themselves before giving care?", "back": "Introducing yourself helps orient the resident and build trust."},
    {"category": "Communication", "front": "Why is body language important when caring for residents?", "back": "Posture and facial expression affect whether the resident feels respected and safe."},
    {"category": "Communication", "front": "Why should observations be reported objectively?", "back": "Clear, factual reporting gives the nurse better information for decision-making."},

    {"category": "Safety", "front": "Why must wheelchair wheels be locked before a transfer?", "back": "Locked wheels keep the chair from moving and reduce fall risk."},
    {"category": "Safety", "front": "Why should bed wheels be locked before movement-based care?", "back": "A locked bed stays stable and helps prevent unsafe shifting."},
    {"category": "Safety", "front": "Why should the call light be left within easy reach?", "back": "The resident can request help safely without attempting unsafe movement alone."},
    {"category": "Safety", "front": "Why should walkways stay free of clutter?", "back": "Clear pathways lower the chance of trips and falls."},
    {"category": "Safety", "front": "What should a CNA do if equipment seems unsafe or broken?", "back": "Do not use it and report the problem according to facility policy."},
    {"category": "Safety", "front": "Why are non-skid shoes or socks often important?", "back": "They help lower slipping risk during standing or walking."},
    {"category": "Safety", "front": "What should a CNA do if a resident grows weak during a transfer?", "back": "Protect the resident from falling and call for help."},
    {"category": "Safety", "front": "Why is proper resident positioning important after care is finished?", "back": "Good positioning supports comfort, safety, and pressure relief."},
    {"category": "Safety", "front": "Why should a CNA explain movement before helping a resident stand or transfer?", "back": "Preparation improves cooperation and supports safer movement."},
    {"category": "Safety", "front": "Why should the environment be checked before starting care?", "back": "Looking for hazards first helps prevent accidents during the task."},

    {"category": "Transfers and Mobility", "front": "What is the purpose of a gait belt during certain transfers?", "back": "A gait belt can provide safer support and guidance when moving a resident."},
    {"category": "Transfers and Mobility", "front": "Why should the wheelchair be placed close to the bed before a transfer?", "back": "Close positioning reduces unsafe reaching, twisting, and extra movement."},
    {"category": "Transfers and Mobility", "front": "Why should a CNA use proper body mechanics?", "back": "Good body mechanics help protect both the resident and the caregiver from injury."},
    {"category": "Transfers and Mobility", "front": "Why may the bed height need adjustment before a transfer?", "back": "Proper bed height can support safer movement and better body alignment."},
    {"category": "Transfers and Mobility", "front": "What should be checked before assisting with walking?", "back": "Check the resident’s readiness, footwear, surroundings, and any needed safety equipment."},
    {"category": "Transfers and Mobility", "front": "Why should a resident help with movement if able?", "back": "Participation can improve safety, strength, and independence."},
    {"category": "Transfers and Mobility", "front": "What does ambulation mean?", "back": "Ambulation means walking or helping a resident walk."},
    {"category": "Transfers and Mobility", "front": "Why might a resident need to sit briefly before standing?", "back": "A short pause can help reduce dizziness from position changes."},
    {"category": "Transfers and Mobility", "front": "Why should the wheelchair be aligned correctly before lowering a resident into it?", "back": "Proper alignment supports smoother, safer movement and better positioning."},
    {"category": "Transfers and Mobility", "front": "Why should a CNA stay close during transfer assistance?", "back": "Staying close allows quicker support if balance is lost."},

    {"category": "Vital Signs", "front": "What does blood pressure tell you?", "back": "It reflects the pressure of blood against artery walls."},
    {"category": "Vital Signs", "front": "Why should a blood pressure cuff be placed on a bare arm?", "back": "A bare arm helps improve the accuracy of the reading."},
    {"category": "Vital Signs", "front": "Why should the resident’s arm be supported at heart level during blood pressure measurement?", "back": "Correct arm position helps give a more accurate reading."},
    {"category": "Vital Signs", "front": "What should a CNA do after taking a blood pressure reading?", "back": "Record it correctly and report concerns according to instructions."},
    {"category": "Vital Signs", "front": "Why should unusual vital sign results be reported?", "back": "Abnormal findings may show a change in the resident’s condition."},
    {"category": "Vital Signs", "front": "Why is resident identification important before checking vital signs?", "back": "It helps ensure the right care is provided to the right person."},
    {"category": "Vital Signs", "front": "Why is exact documentation important after measuring a vital sign?", "back": "Accurate records help the care team monitor changes safely."},
    {"category": "Vital Signs", "front": "What does it mean to document a measurement exactly?", "back": "It means recording the actual number observed, not an estimate."},
    {"category": "Vital Signs", "front": "Why should the procedure be explained before taking a vital sign?", "back": "Explaining the step helps the resident know what to expect."},
    {"category": "Vital Signs", "front": "What should a CNA do if unsure whether a reading is correct?", "back": "Follow policy, repeat if allowed, and report to the nurse."},

    {"category": "Elimination", "front": "Why should urinary output be read at eye level?", "back": "Reading it at eye level helps improve measurement accuracy."},
    {"category": "Elimination", "front": "Why are gloves needed when handling urine or urine equipment?", "back": "Gloves help protect against exposure to body fluids."},
    {"category": "Elimination", "front": "Why should urinary output be recorded exactly instead of estimated?", "back": "Exact amounts are needed for accurate monitoring."},
    {"category": "Elimination", "front": "Why is privacy important during elimination care?", "back": "Privacy supports dignity, respect, and comfort."},
    {"category": "Elimination", "front": "What should a CNA do after measuring urinary output?", "back": "Clean equipment as instructed, remove gloves, and perform hand hygiene."},
    {"category": "Elimination", "front": "Why should the measuring container be placed on a flat surface to read it?", "back": "A level surface helps improve measurement accuracy."},
    {"category": "Elimination", "front": "Why should changes in bowel or bladder patterns be reported?", "back": "Changes may signal a health issue that needs attention."},
    {"category": "Elimination", "front": "Why is it important to avoid spills while measuring urine?", "back": "Spills affect accuracy and increase contamination risk."},
    {"category": "Elimination", "front": "What is urinary output?", "back": "Urinary output is the amount of urine a resident produces."},
    {"category": "Elimination", "front": "Why should hand hygiene still be done after glove removal in elimination care?", "back": "Hands may still carry germs after the gloves come off."},

    {"category": "Nutrition and Hydration", "front": "Why is good hydration important for residents?", "back": "Fluids support body function, comfort, and overall health."},
    {"category": "Nutrition and Hydration", "front": "Why should a CNA observe how much a resident eats and drinks?", "back": "Poor intake may need reporting and follow-up."},
    {"category": "Nutrition and Hydration", "front": "Why is positioning important before meals?", "back": "Proper positioning can improve comfort and lower choking risk."},
    {"category": "Nutrition and Hydration", "front": "What should a CNA do if a resident begins coughing during a meal?", "back": "Stop and respond according to safety procedures, then report the concern."},
    {"category": "Nutrition and Hydration", "front": "Why should meal preferences be respected when allowed?", "back": "Respecting preferences supports dignity and better participation in meals."},
    {"category": "Nutrition and Hydration", "front": "Why should a poor appetite be reported?", "back": "Not eating enough may affect nutrition and health."},
    {"category": "Nutrition and Hydration", "front": "Why should residents not be rushed while eating?", "back": "A calm pace supports safety, comfort, and better intake."},
    {"category": "Nutrition and Hydration", "front": "What should be checked before assisting with a meal tray?", "back": "Check the resident, position, and any feeding instructions or precautions."},
    {"category": "Nutrition and Hydration", "front": "Why may intake need to be documented?", "back": "Tracking intake helps the care team monitor nutrition and hydration."},
    {"category": "Nutrition and Hydration", "front": "Why can gentle encouragement help at mealtime?", "back": "Encouragement may improve comfort and cooperation without forcing."},

    {"category": "Skin Care and Personal Care", "front": "Why is observing the skin important during daily care?", "back": "Skin checks can reveal redness, irritation, or breakdown early."},
    {"category": "Skin Care and Personal Care", "front": "Why should the skin be dried gently after bathing?", "back": "Gentle drying helps protect delicate skin and improve comfort."},
    {"category": "Skin Care and Personal Care", "front": "Why is perineal care usually done from cleaner areas toward dirtier areas?", "back": "This method helps reduce the spread of germs."},
    {"category": "Skin Care and Personal Care", "front": "Why should all needed supplies be prepared before starting personal care?", "back": "Preparation helps care stay safe, efficient, and organized."},
    {"category": "Skin Care and Personal Care", "front": "Why should the resident remain covered during a bath except for the body part being washed?", "back": "This protects warmth, privacy, and dignity."},
    {"category": "Skin Care and Personal Care", "front": "Why should skin products be used only as directed?", "back": "Products should follow instructions or care plans to avoid harm."},
    {"category": "Skin Care and Personal Care", "front": "Why should red areas over bony parts be reported?", "back": "They may be early warning signs of pressure injury."},
    {"category": "Skin Care and Personal Care", "front": "Why is oral care important in daily CNA practice?", "back": "Oral care supports comfort, cleanliness, and general health."},
    {"category": "Skin Care and Personal Care", "front": "Why should nail care be done carefully?", "back": "Careful nail care helps avoid injury and supports hygiene."},
    {"category": "Skin Care and Personal Care", "front": "Why does gentle handling matter during personal care?", "back": "Gentle care supports trust, comfort, and dignity."},

    {"category": "Mental Health and Social Needs", "front": "Why is reassurance important for an anxious resident?", "back": "Reassurance can reduce fear and help the resident feel safer."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA encourage independence when possible?", "back": "Encouraging independence supports self-esteem and function."},
    {"category": "Mental Health and Social Needs", "front": "Why may loneliness affect a resident’s well-being?", "back": "Isolation can affect mood, motivation, and overall quality of life."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA report sudden mood or behavior changes?", "back": "Unexpected changes may signal illness, pain, or emotional distress."},
    {"category": "Mental Health and Social Needs", "front": "Why should residents be treated as adults even when they need full care?", "back": "Every resident deserves respect regardless of their level of dependence."},
    {"category": "Mental Health and Social Needs", "front": "Why is patience important when helping a slow-moving resident?", "back": "Patience supports dignity and reduces frustration for the resident."},
    {"category": "Mental Health and Social Needs", "front": "Why should family concerns sometimes be shared with the nurse?", "back": "Family observations may provide useful information about the resident’s condition."},
    {"category": "Mental Health and Social Needs", "front": "Why is social interaction part of quality care?", "back": "Meaningful interaction can support emotional well-being and reduce isolation."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA avoid speaking about a resident as if they are not present?", "back": "It is disrespectful and can harm dignity and trust."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA support resident routines when possible?", "back": "Familiar routines can improve comfort, security, and cooperation."},

    {"category": "Restorative Care", "front": "What is the purpose of restorative care?", "back": "Restorative care helps residents maintain or improve function and independence."},
    {"category": "Restorative Care", "front": "Why should a CNA encourage a resident to do what they can for themselves?", "back": "Doing so helps preserve ability, confidence, and independence."},
    {"category": "Restorative Care", "front": "Why are range-of-motion exercises used?", "back": "They help maintain joint movement and flexibility."},
    {"category": "Restorative Care", "front": "Why should movements during exercises be slow and gentle?", "back": "Slow, careful motion reduces discomfort and injury risk."},
    {"category": "Restorative Care", "front": "Why should pain during movement be reported?", "back": "Pain may mean the exercise or activity should be reassessed."},
    {"category": "Restorative Care", "front": "Why can assistive devices support independence?", "back": "Devices such as walkers or adaptive tools can help residents do more safely."},
    {"category": "Restorative Care", "front": "Why should a CNA follow instructions closely during restorative tasks?", "back": "These activities should match the resident’s plan and safety needs."},
    {"category": "Restorative Care", "front": "Why is regular walking encouragement helpful for some residents?", "back": "Walking may help preserve strength, mobility, and circulation."},
    {"category": "Restorative Care", "front": "Why should a resident’s progress or decline in function be reported?", "back": "Changes in ability may affect the care approach and safety plan."},
    {"category": "Restorative Care", "front": "Why should independence be balanced with supervision?", "back": "Residents should do what they can, but still need protection from unsafe situations."},

    {"category": "Documentation and Reporting", "front": "When should a CNA document care?", "back": "Care should be documented after it is completed."},
    {"category": "Documentation and Reporting", "front": "Why must charting be accurate?", "back": "Accurate charting supports safe communication and care decisions."},
    {"category": "Documentation and Reporting", "front": "What kinds of resident changes should be reported quickly?", "back": "Examples include pain, dizziness, weakness, confusion, unusual drowsiness, or safety concerns."},
    {"category": "Documentation and Reporting", "front": "Why should a CNA avoid guessing when documenting?", "back": "Documentation should reflect exact observations, not assumptions."},
    {"category": "Documentation and Reporting", "front": "Why should a fall be reported right away?", "back": "A fall may involve injury or urgent follow-up needs."},
    {"category": "Documentation and Reporting", "front": "What is objective reporting?", "back": "Objective reporting means sharing clear facts and observations instead of opinions."},
    {"category": "Documentation and Reporting", "front": "Why should unusual bruising, redness, or swelling be reported?", "back": "These may show injury or a change in condition."},
    {"category": "Documentation and Reporting", "front": "Why must documentation be entered for the correct resident?", "back": "Correct identification is necessary for safe, accurate records."},
    {"category": "Documentation and Reporting", "front": "Why is timely reporting important for the nurse aide role?", "back": "Fast reporting helps the care team respond sooner to problems."},
    {"category": "Documentation and Reporting", "front": "Why should facility policy guide reporting and charting?", "back": "Following policy helps information stay consistent, safe, and properly handled."}
]

category_descriptions = {
    "Infection Control": "Practice hand hygiene, PPE, and contamination prevention for every resident interaction.",
    "Resident Rights": "Focus on dignity, privacy, choice, and respectful communication.",
    "Communication": "Use clear, calm language and active listening to support resident understanding.",
    "Safety": "Remember hazard checks, secure equipment, and safe resident positioning.",
    "Transfers and Mobility": "Review gait belts, body mechanics, and safe transfer preparation.",
    "Vital Signs": "Prioritize accurate technique, correct positioning, and prompt reporting.",
    "Elimination": "Keep care private, hygienic, and report any changes in output patterns.",
    "Nutrition and Hydration": "Observe intake, support proper positioning, and report appetite changes.",
    "Skin Care and Personal Care": "Protect skin integrity, maintain cleanliness, and preserve dignity.",
    "Mental Health and Social Needs": "Support emotional well-being with patience, reassurance, and social connection.",
    "Restorative Care": "Encourage independence safely and follow restorative plans consistently.",
    "Documentation and Reporting": "Document observations accurately and report changes clearly.",
}
flashcard_categories = ["All Categories"] + sorted(category_descriptions)

view_meta = {
    "View A: Texas CNA Academy": {
        "eyebrow": "Study.com-inspired learning",
        "title": "A cleaner, brighter CNA prep experience",
        "description": "Move from study tracks to flashcards, quizzes, and clinical skills with a modern course-card layout built for focused review sessions.",
        "breadcrumb": ["Home", "CNA Academy"],
        "highlights": ["Interactive course cards", "Progress milestones", "Quiz feedback"]
    },
    "View B: CNA CEUs & TULIP-Link": {
        "eyebrow": "Renewal planning",
        "title": "Track CEUs and TULIP readiness in one place",
        "description": "See readiness, missing steps, and sponsored learning opportunities with cleaner dashboards and easier scanability.",
        "breadcrumb": ["Home", "Renewal Hub"],
        "highlights": ["Prominent progress", "Checklist-based guidance", "Sponsored CEU cards"]
    },
    "View C: DON or Instructors & Facility Dashboard": {
        "eyebrow": "Facility oversight",
        "title": "Facility-ready compliance dashboards for leaders",
        "description": "Filter urgent staff, review readiness indicators, and coordinate follow-up actions with stronger hierarchy and spacing.",
        "breadcrumb": ["Home", "Facility Dashboard"],
        "highlights": ["Risk filtering", "Action center", "Compliance matrix"]
    }
}

written_quiz = [
    {
        "q": "Which action best supports infection prevention?",
        "choices": ["Wash hands before and after care", "Reuse gloves between residents", "Put linen on the floor", "Skip PPE if hurried"],
        "answer": "Wash hands before and after care",
        "rationale": "Hand hygiene is a core infection-prevention action."
    },
    {
        "q": "Which resident right must be protected during bathing and toileting?",
        "choices": ["Privacy", "Speed only", "Silence from all staff", "Immediate discharge"],
        "answer": "Privacy",
        "rationale": "Residents have the right to privacy, dignity, and respectful treatment."
    },
    {
        "q": "Before beginning a clinical skill, the CNA should first:",
        "choices": ["Identify the resident and explain the procedure", "Document care", "Skip to the task", "Ask another resident for help"],
        "answer": "Identify the resident and explain the procedure",
        "rationale": "Proper identification and communication improve safety and trust."
    },
    {
        "q": "Which observation should be reported promptly?",
        "choices": ["Resident watched TV", "New dizziness during transfer", "Resident requested a blanket", "Resident ate lunch"],
        "answer": "New dizziness during transfer",
        "rationale": "A new change in condition may indicate risk and requires attention."
    },
    {
        "q": "Documentation should occur:",
        "choices": ["After care is completed", "Before care starts", "Only weekly", "Only if family asks"],
        "answer": "After care is completed",
        "rationale": "Documentation should reflect actual completed care and observations."
    },
    {
        "q": "A CNA supports resident independence by:",
        "choices": ["Doing everything quickly without asking", "Encouraging the resident to do what they can safely do", "Ignoring assistive devices", "Avoiding all conversation"],
        "answer": "Encouraging the resident to do what they can safely do",
        "rationale": "Long-term care focuses on preserving function and dignity."
    },
    {
        "q": "Which action supports respectful dementia care?",
        "choices": ["Argue with confusion", "Use calm redirection", "Rush the resident", "Mock repeated questions"],
        "answer": "Use calm redirection",
        "rationale": "Calm redirection is safer and more supportive than confrontation."
    }
]

skills_quiz = [
    {
        "q": "Before transferring a resident from bed to wheelchair, which safety step is critical?",
        "choices": ["Offer juice first", "Lock the wheels", "Raise the bed to the highest point", "Remove footwear"],
        "answer": "Lock the wheels",
        "rationale": "Unlocked equipment can move and create fall risk."
    },
    {
        "q": "For urinary output measurement, what improves accuracy?",
        "choices": ["Estimate visually", "Read at eye level in a graduate", "Chart before measuring", "Discard before reading"],
        "answer": "Read at eye level in a graduate",
        "rationale": "Eye-level measurement is more accurate."
    },
    {
        "q": "During handwashing, which step helps avoid contamination?",
        "choices": ["Touch the inside sink after washing", "Keep fingertips pointed down when rinsing", "Dry hands on clothing", "Skip soap if rushed"],
        "answer": "Keep fingertips pointed down when rinsing",
        "rationale": "This helps keep runoff away from cleaner areas."
    },
    {
        "q": "What should happen if a resident becomes weak during a transfer?",
        "choices": ["Force the transfer", "Ignore it and continue", "Protect the resident and call for help", "Leave the resident alone"],
        "answer": "Protect the resident and call for help",
        "rationale": "Resident safety comes first during any change in condition."
    }
]

clinical_skills = {
    "Handwashing": [
        "Wet hands and wrists under warm running water.",
        "Apply soap.",
        "Lather all surfaces, including between fingers.",
        "Rub for at least 20 seconds.",
        "Clean fingertips and nails.",
        "Rinse with fingertips pointed downward.",
        "Dry with clean paper towel.",
        "Use paper towel to turn off faucet.",
        "CRITICAL SAFETY STEP: Do not recontaminate clean hands by touching the sink or faucet directly."
    ],
    "Measuring & Recording Blood Pressure": [
        "Identify the resident and explain the skill.",
        "Position the arm correctly at heart level.",
        "Apply the cuff to the bare upper arm.",
        "Place the stethoscope over the brachial artery.",
        "Inflate and deflate cuff carefully.",
        "Identify systolic and diastolic values.",
        "Record the reading accurately.",
        "CRITICAL SAFETY STEP: Report abnormal or concerning findings according to policy."
    ],
    "Measuring & Recording Urinary Output": [
        "Explain the procedure and provide privacy.",
        "Put on gloves.",
        "Pour urine into the graduate without spilling.",
        "Read at eye level.",
        "Discard and clean equipment per instructions.",
        "Remove gloves.",
        "Perform hand hygiene.",
        "Record the exact amount measured.",
        "CRITICAL SAFETY STEP: Record the measured amount, not an estimate."
    ],
    "Transfer: Bed to Wheelchair": [
        "Identify the resident and explain the procedure.",
        "Provide non-skid footwear if indicated.",
        "Position wheelchair correctly.",
        "Lock the bed wheels and wheelchair wheels.",
        "Adjust bed height for safe transfer.",
        "Use gait belt if required by care approach.",
        "Pivot safely and lower resident into wheelchair.",
        "Ensure resident is aligned and comfortable.",
        "CRITICAL SAFETY STEP: Lock equipment before movement begins."
    ]
}

study_tracks = [
    {
        "title": "Role of the Nurse Aide",
        "items": [
            "Work under nurse supervision and follow the care plan.",
            "Observe and report changes in resident condition.",
            "Support comfort, safety, dignity, and independence.",
            "Document accurately after care tasks are completed."
        ]
    },
    {
        "title": "Resident Rights",
        "items": [
            "Protect privacy and dignity during all care.",
            "Respect choice, confidentiality, and respectful treatment.",
            "Recognize and report abuse, neglect, or property concerns.",
            "Promote informed participation in care whenever possible."
        ]
    },
    {
        "title": "Infection Prevention & PPE",
        "items": [
            "Perform hand hygiene before and after care.",
            "Use gloves and PPE according to task and exposure risk.",
            "Handle soiled items carefully to reduce spread.",
            "Maintain annual infection-control training awareness."
        ]
    },
    {
        "title": "Communication & Mental Health",
        "items": [
            "Use clear, calm, respectful communication.",
            "Adapt communication for hearing, vision, or cognitive needs.",
            "Use reassurance and redirection with confused residents.",
            "Observe and report behavior or mood changes."
        ]
    },
    {
        "title": "Basic Nursing Skills",
        "items": [
            "Measure and record vital signs and outputs accurately.",
            "Observe pain, weakness, breathing changes, skin concerns, and dizziness.",
            "Use proper body mechanics and safety setup.",
            "Report significant changes promptly."
        ]
    },
    {
        "title": "Restorative Care",
        "items": [
            "Encourage residents to do what they can safely do.",
            "Support mobility, grooming, feeding, and function.",
            "Use assistive devices safely.",
            "Help preserve independence and quality of life."
        ]
    },
    {
        "title": "Dementia / Alzheimer's Support",
        "items": [
            "Approach calmly and reduce environmental stress.",
            "Use short, simple directions and reassurance.",
            "Redirect rather than argue.",
            "Protect safety and maintain respect."
        ]
    }
]

renewal_rules = [
    "Texas nurse aides renew on a 24-month cycle.",
    "The 90-day TULIP action window opens before expiration.",
    "At least 24 hours of in-service education are expected every two years.",
    "Education should include geriatrics and dementia / Alzheimer's-related content.",
    "Annual infection-control training should also be maintained.",
    "Form 5506-NAR workflow can support employment verification needs."
]

tulip_coach_steps = [
    "Sign in to TULIP and confirm your profile details.",
    "Review certificate number, name, and contact information.",
    "Check your expiration date and confirm your renewal window timing.",
    "Confirm your in-service records, including required topic coverage.",
    "Gather any employer verification information needed for renewal workflow.",
    "Upload required documents if the portal requests them.",
    "Review the summary page carefully before final submission.",
    "Save or print your confirmation details for your records."
]

common_delay_mistakes = [
    "Waiting until the last minute after the 90-day window opens.",
    "Not tracking in-service hours throughout the full 24-month period.",
    "Missing geriatrics, dementia, or infection-control documentation.",
    "Entering profile or certificate information incorrectly.",
    "Failing to follow up on TULIP messages or deficiencies.",
    "Not coordinating employer verification early enough."
]

# =========================================================
# HEADER
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="eyebrow">TULIP-Link CNA Academy</div>
            <h3 style="margin:.8rem 0 .45rem;">Study.com-style navigation</h3>
            <p>Jump between study, renewal, and facility workflows without losing your place.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    view = st.radio(
        "Choose your path",
        [
            "View A: Texas CNA Academy",
            "View B: CNA CEUs & TULIP-Link",
            "View C: DON or Instructors & Facility Dashboard"
        ]
    )

    if view == "View A: Texas CNA Academy":
        st.selectbox("Filter flashcards by category", flashcard_categories, key="flash_category")
        if st.session_state.flash_category != "All Categories":
            st.caption(category_descriptions.get(st.session_state.flash_category, ""))
        st.markdown(
            """
            <div class="sidebar-panel">
                <strong>Academy focus</strong>
                <p>Practice flashcards, written questions, and clinical skill checklists in smaller study sprints.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif view == "View B: CNA CEUs & TULIP-Link":
        st.markdown(
            """
            <div class="sidebar-panel">
                <strong>Renewal focus</strong>
                <p>Track in-service requirements, watch the TULIP countdown, and clear missing items faster.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="sidebar-panel">
                <strong>Leadership focus</strong>
                <p>Monitor facility-level readiness, prioritize urgent staff, and support renewal follow-through.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown(
        """
        <div class="sidebar-panel">
            <strong>Quick start</strong>
            <p>1. Pick the role that matches your workflow.</p>
            <p>2. Use the highlighted cards and milestones to spot your next action.</p>
            <p>3. Track progress before test day, renewal, or staff outreach.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

active_view = view_meta[view]
render_breadcrumb(active_view["breadcrumb"])
highlight_html = "".join(f'<span class="hero-chip">{esc(item)}</span>' for item in active_view["highlights"])
st.markdown(
    f"""
    <div class="main-hero">
        <div class="eyebrow">{esc(active_view["eyebrow"])}</div>
        <div class="hero-title">🩺 {esc(active_view["title"])}</div>
        <div class="hero-copy">{esc(active_view["description"])}</div>
        <div class="hero-highlights">{highlight_html}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# VIEW A
# =========================================================
if view == "View A: Texas CNA Academy":
    st.subheader("Texas CNA Academy")
    st.markdown(
        '<div class="info-card">Focus on mastery, practice written questions, and simulate clinical skill checklists. Use the tabs to keep your review structured and efficient.</div>',
        unsafe_allow_html=True
    )

    mastered = len(st.session_state.mastered_cards)
    total_flash = len(flashcards)
    written_score = 0
    if len(st.session_state.written_answers) == len(written_quiz):
        written_score = sum(
            1 for i, q in enumerate(written_quiz)
            if st.session_state.written_answers.get(i) == q["answer"]
        )
    skills_score = 0
    if len(st.session_state.skills_answers) == len(skills_quiz):
        skills_score = sum(
            1 for i, q in enumerate(skills_quiz)
            if st.session_state.skills_answers.get(i) == q["answer"]
        )

    readiness_total = len(flashcards) + len(written_quiz) + len(skills_quiz)
    readiness_points = mastered + written_score + skills_score
    readiness_pct = pct(readiness_points, readiness_total)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{mastered}/{total_flash}</div><div class="label">Flashcards Mastered</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{written_score}/{len(written_quiz)}</div><div class="label">Written Quiz Score</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{skills_score}/{len(skills_quiz)}</div><div class="label">Skills Quiz Score</div></div>', unsafe_allow_html=True)

    render_progress_summary(
        "Test readiness progress",
        readiness_pct,
        "A brighter progress view highlights completion percentage, study momentum, and milestone status at a glance.",
        milestone_label(readiness_pct),
        milestone_badge_class(readiness_pct)
    )
    st.progress(readiness_pct / 100)
    st.write(f"Readiness score: **{readiness_pct}%** complete")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Study Tracks",
        "Flashcards",
        "Written Quiz",
        "Clinical Skills",
        "Skills Quiz",
        "Exam Tips",
        "Texas CNA Success"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Featured Study Tracks")
        st.caption("Browse cleaner course cards with category badges, quick descriptions, and progress indicators before opening the lesson outline below.")
        categories_for_cards = sorted(category_descriptions.keys())
        for start in range(0, len(categories_for_cards), 3):
            cols = st.columns(3)
            for col, category_name in zip(cols, categories_for_cards[start:start + 3]):
                total_in_category = sum(1 for card in flashcards if card["category"] == category_name)
                mastered_in_category = sum(
                    1 for idx in st.session_state.mastered_cards
                    if 0 <= idx < len(flashcards) and flashcards[idx]["category"] == category_name
                )
                review_in_category = sum(
                    1 for idx in st.session_state.review_cards
                    if 0 <= idx < len(flashcards) and flashcards[idx]["category"] == category_name
                )
                course_progress = pct(mastered_in_category, total_in_category)
                with col:
                    st.markdown(
                        render_course_card(
                            icon_for_category(category_name),
                            badge_class_for_category(category_name),
                            category_name,
                            category_name,
                            category_descriptions[category_name],
                            f"{course_progress}% mastered",
                            f"{review_in_category} review",
                            progress=course_progress
                        ),
                        unsafe_allow_html=True
                    )
        st.markdown("### Lesson Outlines")
        for track in study_tracks:
            with st.expander(track["title"], expanded=False):
                for item in track["items"]:
                    st.write(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Interactive Flashcards")
        st.markdown('<div class="info-card">Use the sidebar category filter to narrow the deck, then flip cards and mark mastery as you go.</div>', unsafe_allow_html=True)

        category = st.session_state.flash_category
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(
                f"""
                <div class="pill-row">
                    <span class="pill">Current focus: {esc(category)}</span>
                    <span class="pill">Deck size: {len(flashcards)} cards</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Reset to All Categories", use_container_width=True):
                st.session_state.flash_category = "All Categories"
                st.session_state.flash_category_prev = "All Categories"
                st.session_state.flash_index = 0
                st.session_state.flash_flip = False
                st.rerun()
            if category != "All Categories":
                st.caption(category_descriptions.get(category, ""))
            else:
                st.caption("Browse all flashcards or pick a category to focus your study.")
        with c2:
            total_cards = len(flashcards)
            filtered_count = sum(1 for card in flashcards if category == "All Categories" or card["category"] == category)
            st.metric("Category", category)
            st.metric("Visible cards", f"{filtered_count}/{total_cards}")

        if category != st.session_state.flash_category_prev:
            st.session_state.flash_index = 0
            st.session_state.flash_flip = False
            st.session_state.flash_category_prev = category

        filtered_flashcards = [
            (idx, card)
            for idx, card in enumerate(flashcards)
            if category == "All Categories" or card["category"] == category
        ]

        if not filtered_flashcards:
            st.warning("No flashcards match that category. Please choose another category.")
        else:
            main_col, tip_col = st.columns([3, 1])
            with main_col:
                if st.session_state.flash_index >= len(filtered_flashcards):
                    st.session_state.flash_index = 0

                card_index, card = filtered_flashcards[st.session_state.flash_index]
                st.caption(f"Card {st.session_state.flash_index + 1} of {len(filtered_flashcards)} • {card['category']}")

                st.markdown(
                    f"""
                    <div class="soft-card interactive-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                            <span class="badge {badge_class_for_category(card['category'])}">{esc(card['category'])}</span>
                            <span style="font-size:0.90rem; color:#0f5db4; font-weight:700;">{st.session_state.flash_index + 1}/{len(filtered_flashcards)}</span>
                        </div>
                        <h3>{'Answer' if st.session_state.flash_flip else 'Question'}</h3>
                        <p style="font-size:1.06rem; line-height:1.6;">{esc(card['back'] if st.session_state.flash_flip else card['front'])}</p>
                    </div>
                    """, unsafe_allow_html=True
                )

                progress = (st.session_state.flash_index + 1) / len(filtered_flashcards)
                st.progress(progress)

                nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
                with nav_col1:
                    if st.button("🩺 Previous", use_container_width=True):
                        st.session_state.flash_index = (st.session_state.flash_index - 1) % len(filtered_flashcards)
                        st.session_state.flash_flip = False
                        st.rerun()
                with nav_col2:
                    if st.button("Flip Card", use_container_width=True):
                        st.session_state.flash_flip = not st.session_state.flash_flip
                        st.rerun()
                with nav_col3:
                    if st.button("Next 🩺", use_container_width=True):
                        st.session_state.flash_index = (st.session_state.flash_index + 1) % len(filtered_flashcards)
                        st.session_state.flash_flip = False
                        st.rerun()

                action_col1, action_col2 = st.columns([1, 1])
                with action_col1:
                    if st.button("Mastered", use_container_width=True):
                        st.session_state.mastered_cards.add(card_index)
                        st.session_state.review_cards.discard(card_index)
                        st.success("Marked as mastered.")
                with action_col2:
                    if st.button("Needs Review", use_container_width=True):
                        st.session_state.review_cards.add(card_index)
                        st.session_state.mastered_cards.discard(card_index)
                        st.warning("Marked for review.")

                st.markdown(
                    f"<div class='soft-card' style='padding:0.9rem; background:#f8fafc;'>Mastered: <strong>{len(st.session_state.mastered_cards)}</strong> | Review: <strong>{len(st.session_state.review_cards)}</strong></div>",
                    unsafe_allow_html=True
                )

            with tip_col:
                review_counts = {}
                for idx in st.session_state.review_cards:
                    if 0 <= idx < len(flashcards):
                        cat = flashcards[idx]["category"]
                        review_counts[cat] = review_counts.get(cat, 0) + 1

                current_category_review = 0
                if category != "All Categories":
                    current_category_review = sum(
                        1
                        for idx in st.session_state.review_cards
                        if 0 <= idx < len(flashcards) and flashcards[idx]["category"] == category
                    )

                top_review_category = None
                if review_counts:
                    top_review_category = max(review_counts, key=review_counts.get)

                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown('### Flashcard Focus Summary')
                st.write(f'- Mastered cards: **{len(st.session_state.mastered_cards)}**')
                st.write(f'- Review cards: **{len(st.session_state.review_cards)}**')
                if top_review_category:
                    st.write(f'- Most review cards are in **{top_review_category}** ({review_counts[top_review_category]})')
                else:
                    st.write('- No review cards yet — keep studying and mark anything you want to revisit.')
                if category != "All Categories":
                    st.write(f'- Review cards in this category: **{current_category_review}**')
                if top_review_category and category != top_review_category:
                    st.write(f'- Suggested next focus: **{top_review_category}**')
                st.markdown('---')
                st.markdown('### Texas CNA Study Tips')
                st.write('- Focus on infection control, resident rights, and safe transfers first.')
                st.write('- Speak the answer out loud to help embed the state exam language.')
                st.write('- Use the review flag for cards that mention policy, safety, or documentation.')
                st.write('- Aim for steady progress across categories, not just one topic area.')
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Written Practice Quiz")
        answered_written = len(st.session_state.written_answers)
        st.progress(answered_written / len(written_quiz))
        st.caption(f"Completion: {answered_written}/{len(written_quiz)} questions answered")
        for i, item in enumerate(written_quiz):
            st.markdown(
                f"""
                <div class="quiz-shell">
                    <div class="quiz-label">Question {i+1} of {len(written_quiz)}</div>
                    <strong>{item['q']}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            ans = st.radio(
                f"Choose answer for written question {i+1}",
                item["choices"],
                key=f"written_{i}",
                index=None
            )
            if ans:
                st.session_state.written_answers[i] = ans
                if ans == item["answer"]:
                    st.success(f"Correct. {item['rationale']}")
                else:
                    st.error(f"Incorrect. Correct answer: {item['answer']}. {item['rationale']}")
            st.markdown("---")
        if len(st.session_state.written_answers) == len(written_quiz):
            score = sum(1 for i, q in enumerate(written_quiz) if st.session_state.written_answers.get(i) == q["answer"])
            st.info(f"Written quiz score: {score}/{len(written_quiz)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Clinical Skills Checklists")
        chosen_skill = st.selectbox("Choose a Prometric-style skill", list(clinical_skills.keys()))
        st.markdown('<div class="info-card">Focus especially on hand hygiene, privacy, communication, safe setup, accurate measurement, and reporting concerns.</div>', unsafe_allow_html=True)

        for idx, step in enumerate(clinical_skills[chosen_skill]):
            key = f"{chosen_skill}_{idx}"
            c1, c2 = st.columns([0.08, 0.92])
            with c1:
                checked = st.checkbox("", key=key)
                st.session_state.skills_checks[key] = checked
            with c2:
                if "CRITICAL SAFETY STEP" in step:
                    st.markdown(f'<div class="check-step"><span class="critical">{step}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="check-step">{step}</div>', unsafe_allow_html=True)

        completed = sum(
            1 for idx, _ in enumerate(clinical_skills[chosen_skill])
            if st.session_state.skills_checks.get(f"{chosen_skill}_{idx}", False)
        )
        st.write(f"Checklist completion: **{completed}/{len(clinical_skills[chosen_skill])}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Skills Quiz")
        answered_skills = len(st.session_state.skills_answers)
        st.progress(answered_skills / len(skills_quiz))
        st.caption(f"Completion: {answered_skills}/{len(skills_quiz)} skills questions answered")
        for i, item in enumerate(skills_quiz):
            st.markdown(
                f"""
                <div class="quiz-shell">
                    <div class="quiz-label">Skills question {i+1} of {len(skills_quiz)}</div>
                    <strong>{item['q']}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            ans = st.radio(
                f"Choose answer for skills question {i+1}",
                item["choices"],
                key=f"skills_{i}",
                index=None
            )
            if ans:
                st.session_state.skills_answers[i] = ans
                if ans == item["answer"]:
                    st.success(f"Correct. {item['rationale']}")
                else:
                    st.error(f"Incorrect. Correct answer: {item['answer']}. {item['rationale']}")
            st.markdown("---")
        if len(st.session_state.skills_answers) == len(skills_quiz):
            score = sum(1 for i, q in enumerate(skills_quiz) if st.session_state.skills_answers.get(i) == q["answer"])
            st.info(f"Skills quiz score: {score}/{len(skills_quiz)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Exam Tips")
        st.write("- Practice speaking each skill step out loud.")
        st.write("- Rehearse handwashing until the sequence feels automatic.")
        st.write("- Focus on safety setup before touching the resident.")
        st.write("- Protect privacy and communicate before, during, and after the skill.")
        st.write("- Read written questions carefully for safety, rights, and reporting clues.")
        st.write("- Watch for changes in condition and know what should be reported.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab7:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Texas CNA Success")
        st.write("- Build a routine: flashcards, one study track, and one quiz set each session.")
        st.write("- Repeat the high-risk safety steps until they are automatic.")
        st.write("- Practice documentation language that is factual and simple.")
        st.write("- Learn resident rights and infection prevention as priority content areas.")
        st.write("- Use the Renewal Hub after certification so you stay active in Texas.")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# VIEW B
# =========================================================
elif view == "View B: CNA CEUs & TULIP-Link":
    st.subheader("CNA CEUs & TULIP-Link")
    st.markdown(
        '<div class="info-card">Review CNA renewal readiness, missing CEU requirements, and TULIP timing. Use the dashboard to prioritize the next steps before the 90-day window.</div>',
        unsafe_allow_html=True
    )

    active_options = cna_df[cna_df["user_type"] != "Student"].copy()
    active_options["display"] = active_options["first_name"] + " " + active_options["last_name"] + " • " + active_options["license_number"]
    selected_name = st.selectbox("Select CNA profile", active_options["display"].tolist())
    selected = active_options[active_options["display"] == selected_name].iloc[0]

    summary = compliance_snapshot(selected["cna_id"], selected["expiration_date"], ceu_df)
    score = readiness_score(summary)
    missing = missing_items(summary)
    records = ceu_df[ceu_df["cna_id"] == selected["cna_id"]]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{score}%</div><div class="label">Renewal Readiness</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{summary["hours"]}/24</div><div class="label">In-Service Hours</div></div>', unsafe_allow_html=True)
    with m3:
        status = "OPEN" if summary["tulip_days"] <= 0 else "NOT OPEN"
        st.markdown(f'<div class="metric-card"><div class="kpi">{status}</div><div class="label">TULIP Window</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="kpi">{summary["days_left"]}</div><div class="label">Days Until Expiration</div></div>', unsafe_allow_html=True)

    render_progress_summary(
        "Renewal readiness",
        score,
        "Monitor completion percentage, identify missing training, and keep the next milestone visible before the TULIP window opens.",
        milestone_label(score),
        milestone_badge_class(score)
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Dashboard",
        "Stay Active in Texas",
        "Missing Items",
        "TULIP Coach",
        "CEU Records",
        "Common Delays"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Personal Compliance Dashboard")
        st.write(f"**CNA:** {selected['first_name']} {selected['last_name']}")
        st.write(f"**License Number:** {selected['license_number']}")
        st.write(f"**Last Renewal Date:** {selected['last_renewal_date']}")
        st.write(f"**Expiration Date:** {selected['expiration_date']}")
        st.progress(score / 100)
        st.write(f"Renewal readiness score: **{score}%**")

        x1, x2, x3 = st.columns(3)
        with x1:
            st.success("Geriatrics recorded") if summary["geriatric"] else st.error("Geriatrics not recorded")
        with x2:
            st.success("Dementia / Alzheimer's recorded") if summary["dementia"] else st.error("Dementia / Alzheimer's not recorded")
        with x3:
            st.success("Annual infection-control training recorded") if summary["infection"] else st.error("Annual infection-control training not recorded")

        if summary["tulip_days"] > 0:
            st.info(f"Your TULIP action window opens in **{summary['tulip_days']} days**.")
        elif summary["tulip_days"] == 0:
            st.success("Your TULIP action window opens **today**.")
        else:
            st.warning(f"Your TULIP action window opened **{abs(summary['tulip_days'])} days ago**.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Stay Active in Texas")
        for item in renewal_rules:
            st.write(f"- {item}")
        st.markdown('<div class="info-card">Use this section as a plain-language checklist for staying active and avoiding avoidable renewal delays.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Missing Items Before Submission")
        for item in missing:
            st.write(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### TULIP Coach")
        for i, step in enumerate(tulip_coach_steps, start=1):
            st.write(f"{i}. {step}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### CEU Records")
        if records.empty:
            st.warning("No CEU records found.")
        else:
            display = records.rename(columns={
                "course_title": "Course Title",
                "hours": "Hours",
                "geriatric_flag": "Geriatric",
                "dementia_flag": "Dementia/Alzheimer's",
                "infection_flag": "Infection Control"
            })[["Course Title", "Hours", "Geriatric", "Dementia/Alzheimer's", "Infection Control"]]
            st.dataframe(display, use_container_width=True, hide_index=True)

        st.markdown("### Sponsored Texas CEU Placeholder")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(render_course_card("👵", "badge-green", "Geriatrics", "Geriatric Care Update", "Refresh core aging-care practices while filling a major renewal requirement.", "8 hours", "Sponsored slot", thumb_style="height:76px; margin-bottom:.75rem;"), unsafe_allow_html=True)
        with s2:
            st.markdown(render_course_card("🧠", "badge-blue", "Memory Care", "Dementia & Alzheimer’s Care", "Build confidence in calmer communication, redirection, and safer support routines.", "8 hours", "Sponsored slot", thumb_style="height:76px; margin-bottom:.75rem;"), unsafe_allow_html=True)
        with s3:
            st.markdown(render_course_card("🦠", "badge-orange", "Safety", "Infection Control Refresher", "Keep annual safety documentation current with a faster, cleaner training entry point.", "Annual", "Priority topic", thumb_style="height:76px; margin-bottom:.75rem;"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Common Delay Mistakes")
        for item in common_delay_mistakes:
            st.write(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# VIEW C
# =========================================================
else:
    st.subheader("DON or Instructors & Facility Dashboard")
    st.markdown(
        '<div class="info-card">Monitor facility readiness, highlight urgent CNA action items, and support TULIP compliance with clear staff-level guidance.</div>',
        unsafe_allow_html=True
    )
    facility = facility_df.iloc[0]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**Facility:** {facility['facility_name']}")
    st.write(f"**State License Number:** {facility['state_license_number']}")
    st.write(f"**Director of Nursing:** {facility['don_name']}")
    st.markdown('</div>', unsafe_allow_html=True)

    active_staff = cna_df[cna_df["user_type"] != "Student"].copy()
    rows = []
    for _, row in active_staff.iterrows():
        summary = compliance_snapshot(row["cna_id"], row["expiration_date"], ceu_df)
        rows.append({
            "CNA ID": row["cna_id"],
            "First Name": row["first_name"],
            "Last Name": row["last_name"],
            "License Number": row["license_number"],
            "Days Until Expiration": summary["days_left"],
            "CEU Hours Completed": summary["hours"],
            "Geriatrics": "Yes" if summary["geriatric"] else "No",
            "Dementia": "Yes" if summary["dementia"] else "No",
            "Infection Control": "Yes" if summary["infection"] else "No",
            "Readiness Score": readiness_score(summary),
            "Status": status_from_expiration(row["expiration_date"])
        })

    matrix = pd.DataFrame(rows)

    green_count = len(matrix[matrix["Status"] == "GREEN"])
    red_count = len(matrix[matrix["Status"] == "RED"])
    incomplete_ceu = len(matrix[matrix["CEU Hours Completed"] < 24])

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{green_count}</div><div class="label">Safe Zone Staff</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{red_count}</div><div class="label">Inside 90-Day Window</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{incomplete_ceu}</div><div class="label">Below 24 Hours</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Staff Matrix",
        "Action Center",
        "DON Risk Notes",
        "Career Board"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### TULIP Readiness Staff Matrix")
        urgency = st.segmented_control("Filter by urgency", ["ALL", "GREEN", "RED"], default="ALL")
        filtered = matrix if urgency == "ALL" else matrix[matrix["Status"] == urgency]

        def highlight(row):
            color = "#dcfce7" if row["Status"] == "GREEN" else "#fee2e2"
            return [f"background-color: {color}"] * len(row)

        st.dataframe(filtered.style.apply(highlight, axis=1), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Action Center")
        red_staff = matrix[matrix["Status"] == "RED"]

        if red_staff.empty:
            st.success("No CNAs are currently inside the 90-day TULIP window.")
        else:
            options = red_staff.apply(
                lambda x: f"{x['First Name']} {x['Last Name']} • {x['License Number']} • {x['Days Until Expiration']} days left",
                axis=1
            ).tolist()
            selected_option = st.selectbox("Select CNA needing action", options)
            chosen = red_staff.iloc[options.index(selected_option)]
            chosen_cna = cna_df[cna_df["cna_id"] == chosen["CNA ID"]].iloc[0]
            chosen_summary = compliance_snapshot(chosen_cna["cna_id"], chosen_cna["expiration_date"], ceu_df)

            a1, a2 = st.columns(2)
            with a1:
                if st.button("Pre-fill Form 5506-NAR", use_container_width=True):
                    text = make_5506_text(chosen_cna, facility, chosen_summary)
                    st.success("Mock 5506-NAR summary generated.")
                    st.download_button(
                        "Download 5506-NAR Mock Summary",
                        data=text,
                        file_name=f"5506-NAR-{chosen_cna['last_name']}-{chosen_cna['first_name']}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    st.text_area("Preview", text, height=340)

            with a2:
                if st.button("Mock Twilio SMS Trigger", use_container_width=True):
                    sms = f"Hi {chosen_cna['first_name']}, your 3-month Texas TULIP window is OPEN. Your Form 5506-NAR is pre-filled and waiting on the DON desk."
                    st.info("Mock SMS fired.")
                    st.markdown(f'<div class="sms-box">{sms}</div>', unsafe_allow_html=True)

            n1, n2, n3 = st.columns(3)
            with n1:
                st.markdown(f'<span class="badge badge-red">Days Left: {chosen_summary["days_left"]}</span>', unsafe_allow_html=True)
            with n2:
                st.markdown(f'<span class="badge badge-amber">Readiness: {readiness_score(chosen_summary)}%</span>', unsafe_allow_html=True)
            with n3:
                flags = [
                    "Geriatrics ✔" if chosen_summary["geriatric"] else "Geriatrics ✘",
                    "Dementia ✔" if chosen_summary["dementia"] else "Dementia ✘",
                    "Infection ✔" if chosen_summary["infection"] else "Infection ✘"
                ]
                st.markdown(f'<span class="badge badge-red">{" | ".join(flags)}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### DON Risk Notes")
        st.write("- Monitor all CNAs inside the 90-day TULIP window.")
        st.write("- Audit 24-hour totals and required topic coverage early.")
        st.write("- Confirm annual infection-control training records.")
        st.write("- Prepare Form 5506-NAR support before staff become urgent cases.")
        st.write("- Use readiness score trends to prioritize outreach.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("### Facility Career Board")
        st.write("This placeholder supports a free-community model through targeted facility job and training postings.")
        st.write("- Weekend CNA openings")
        st.write("- Evening and night shift differential opportunities")
        st.write("- Employer-sponsored CEU support")
        st.write("- Test-prep assistance and referral bonuses")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(
    "Educational workflow application for Texas CNA study, renewal support, and DON compliance planning. Confirm current rules, forms, credential status, and submission requirements with official Texas HHSC, TULIP, and Prometric resources."
)
st.markdown(
    '<div class="footer-note">Version 1.0 • For educational planning only. Always verify with Texas HHSC and facility guidance.</div>',
    unsafe_allow_html=True
)
