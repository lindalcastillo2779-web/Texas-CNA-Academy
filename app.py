import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="TULIP-Link & CNA Academy",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
:root{
    --bg:#f6f5f1;
    --surface:#ffffff;
    --surface-2:#f3f4f6;
    --surface-3:#ecfeff;
    --text:#1f2937;
    --muted:#6b7280;
    --primary:#0f766e;
    --primary-dark:#134e4a;
    --border:#d1d5db;
    --success:#166534;
    --success-soft:#dcfce7;
    --danger:#b91c1c;
    --danger-soft:#fee2e2;
    --warning:#b45309;
    --warning-soft:#ffedd5;
    --info:#075985;
    --info-soft:#e0f2fe;
    --shadow:0 10px 24px rgba(15,23,42,.08);
    --radius:18px;
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
.main-hero{
    background:linear-gradient(135deg,var(--primary) 0%,var(--primary-dark) 100%);
    color:white;
    border-radius:var(--radius);
    padding:1.2rem 1.2rem;
    box-shadow:var(--shadow);
    margin-bottom:1rem;
}
.card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    box-shadow:var(--shadow);
    margin-bottom:1rem;
}
.soft-card{
    background:var(--surface-2);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.info-card{
    background:var(--surface-3);
    border:1px solid #bae6fd;
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
    font-size:1.85rem;
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
.badge-green{background:var(--success-soft);color:var(--success);}
.badge-red{background:var(--danger-soft);color:var(--danger);}
.badge-amber{background:var(--warning-soft);color:var(--warning);}
.badge-blue{background:var(--info-soft);color:var(--info);}
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
div[data-testid="stDataFrame"]{
    border:1px solid var(--border);
    border-radius:var(--radius);
    overflow:hidden;
}
@media (max-width:768px){
    .block-container{padding-left:.8rem;padding-right:.8rem;}
    .kpi{font-size:1.45rem;}
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
TODAY = date.today()

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
This is a workflow aid generated by TULIP-Link & CNA Academy.
Use official Texas HHSC forms and TULIP for real submission.
""".strip()

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "flash_index": 0,
    "flash_flip": False,
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
    {"category": "Infection Control", "front": "Why is hand hygiene required before and after resident contact?", "back": "It helps reduce the spread of microorganisms and protects both residents and staff."},
    {"category": "Resident Rights", "front": "What does dignity mean during CNA care?", "back": "Privacy, respect, courteous communication, and protecting the resident from unnecessary exposure or embarrassment."},
    {"category": "Safety", "front": "What is a key safety action before transfer?", "back": "Lock the bed and wheelchair wheels before movement begins."},
    {"category": "Communication", "front": "How should a CNA communicate with a resident with hearing loss?", "back": "Face the resident, speak clearly, reduce noise, and confirm understanding."},
    {"category": "Dementia Care", "front": "What is a helpful response when a resident with dementia is distressed?", "back": "Use calm reassurance, redirection, simple explanations, and a safe environment."},
    {"category": "Documentation", "front": "When should care be charted?", "back": "After the care is performed or the observation is made."},
    {"category": "Resident Observation", "front": "Which changes should be reported promptly?", "back": "New dizziness, weakness, pain, skin changes, breathing changes, or changes in behavior or alertness."}
]

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
st.markdown("""
<div class="main-hero">
    <h1>🌷 TULIP-Link & CNA Academy</h1>
    <div>Texas-focused CNA study support, TULIP renewal coaching, CEU tracking, and DON compliance management.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Navigation")
    view = st.radio(
        "Choose your path",
        [
            "View A: CNA Study Academy",
            "View B: CNA Renewal Hub",
            "View C: DON & Facility Dashboard"
        ]
    )
    st.markdown("---")
    st.caption("Built for students, active CNAs, and nursing facility leadership.")

# =========================================================
# VIEW A
# =========================================================
if view == "View A: CNA Study Academy":
    st.subheader("CNA Study Academy")

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

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Test Readiness Progress")
    st.progress(readiness_pct / 100)
    st.write(f"Readiness score: **{readiness_pct}%**")
    st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown("### Texas Study Tracks")
        for track in study_tracks:
            with st.expander(track["title"], expanded=False):
                for item in track["items"]:
                    st.write(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Interactive Flashcards")
        card = flashcards[st.session_state.flash_index]
        st.caption(f"Card {st.session_state.flash_index + 1} of {len(flashcards)} • {card['category']}")

        if not st.session_state.flash_flip:
            st.markdown(
                f"""
                <div class="soft-card">
                    <h3>{card['category']}</h3>
                    <p style="font-size:1.06rem;">{card['front']}</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="soft-card">
                    <h3>Answer</h3>
                    <p style="font-size:1.03rem;">{card['back']}</p>
                </div>
                """, unsafe_allow_html=True
            )

        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            if st.button("⬅ Previous", use_container_width=True):
                st.session_state.flash_index = (st.session_state.flash_index - 1) % len(flashcards)
                st.session_state.flash_flip = False
                st.rerun()
        with b2:
            if st.button("Flip Card", use_container_width=True):
                st.session_state.flash_flip = not st.session_state.flash_flip
                st.rerun()
        with b3:
            if st.button("Mastered", use_container_width=True):
                st.session_state.mastered_cards.add(st.session_state.flash_index)
                st.session_state.review_cards.discard(st.session_state.flash_index)
                st.success("Marked as mastered.")
        with b4:
            if st.button("Needs Review", use_container_width=True):
                st.session_state.review_cards.add(st.session_state.flash_index)
                st.session_state.mastered_cards.discard(st.session_state.flash_index)
                st.warning("Marked for review.")
        with b5:
            if st.button("Next ➡", use_container_width=True):
                st.session_state.flash_index = (st.session_state.flash_index + 1) % len(flashcards)
                st.session_state.flash_flip = False
                st.rerun()

        st.write(f"Mastered: **{len(st.session_state.mastered_cards)}** | Review: **{len(st.session_state.review_cards)}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Written Practice Quiz")
        for i, item in enumerate(written_quiz):
            st.markdown(f"**Q{i+1}. {item['q']}**")
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
        for i, item in enumerate(skills_quiz):
            st.markdown(f"**Q{i+1}. {item['q']}**")
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
elif view == "View B: CNA Renewal Hub":
    st.subheader("CNA Renewal Hub")

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
            st.markdown('<div class="soft-card"><strong>Geriatric Care Update</strong><br><span class="small-muted">8 hours • Sponsored Texas CEU placement</span></div>', unsafe_allow_html=True)
        with s2:
            st.markdown('<div class="soft-card"><strong>Dementia & Alzheimer’s Care</strong><br><span class="small-muted">8 hours • Sponsored Texas CEU placement</span></div>', unsafe_allow_html=True)
        with s3:
            st.markdown('<div class="soft-card"><strong>Infection Control Refresher</strong><br><span class="small-muted">Annual training placement area</span></div>', unsafe_allow_html=True)
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
    st.subheader("DON & Facility Dashboard")
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
