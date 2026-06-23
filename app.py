import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

st.set_page_config(
    page_title="TULIP-Link & CNA Academy",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLES ──────────────────────────────────────────────
st.markdown("""
<style>
:root {
  --bg: #f6f5f1; --surface: #fcfbf8; --surface-2: #f0ede7;
  --text: #1f2937; --muted: #6b7280; --primary: #0f766e;
  --primary-dark: #115e59; --accent: #d97706; --danger: #dc2626;
  --success: #16a34a; --warning: #ca8a04; --radius: 12px;
}
body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; }
.block-container { padding: 1rem 1.5rem 3rem; max-width: 900px; }
.card { background: var(--surface); border: 1px solid #e5e7eb;
  border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-bottom: 1rem;
  box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.section-head { font-size: 1.1rem; font-weight: 700; color: var(--primary);
  border-bottom: 2px solid var(--primary); padding-bottom: .4rem; margin-bottom: 1rem; }
.tag { display:inline-block; padding:.2rem .7rem; border-radius:20px;
  font-size:.75rem; font-weight:600; margin:.2rem; }
.tag-green { background:#dcfce7; color:#166534; }
.tag-red   { background:#fee2e2; color:#991b1b; }
.tag-yellow{ background:#fef9c3; color:#854d0e; }
.tag-blue  { background:#dbeafe; color:#1e40af; }
.tag-purple{ background:#ede9fe; color:#5b21b6; }
.step-row { display:flex; align-items:flex-start; gap:.6rem;
  padding:.5rem 0; border-bottom:1px solid #f3f4f6; }
.step-num { background:var(--primary); color:#fff; border-radius:50%;
  width:24px; height:24px; display:flex; align-items:center;
  justify-content:center; font-size:.75rem; font-weight:700; flex-shrink:0; }
.critical { background:#fff1f2; border-left:4px solid var(--danger);
  padding:.6rem 1rem; border-radius:0 8px 8px 0; margin:.4rem 0;
  font-size:.88rem; color:#7f1d1d; }
.warning-box { background:#fffbeb; border-left:4px solid var(--accent);
  padding:.7rem 1rem; border-radius:0 8px 8px 0; margin:.5rem 0; font-size:.9rem; }
.info-box { background:#eff6ff; border-left:4px solid #3b82f6;
  padding:.7rem 1rem; border-radius:0 8px 8px 0; margin:.5rem 0; font-size:.9rem; }
.success-box { background:#f0fdf4; border-left:4px solid var(--success);
  padding:.7rem 1rem; border-radius:0 8px 8px 0; margin:.5rem 0; font-size:.9rem; }
.badge { display:inline-block; padding:.15rem .6rem; border-radius:20px;
  font-size:.72rem; font-weight:700; }
.badge-green { background:#dcfce7; color:#166534; }
.badge-red   { background:#fee2e2; color:#991b1b; }
.badge-yellow{ background:#fef9c3; color:#854d0e; }
.badge-blue  { background:#dbeafe; color:#1e40af; }
.facility-board { background: linear-gradient(135deg,#0f766e,#115e59);
  color:#fff; border-radius:var(--radius); padding:1.2rem 1.5rem; margin:.8rem 0; }
.table-note { background:#f9fafb; border:1px dashed #d1d5db;
  border-radius:8px; padding:.8rem; font-size:.82rem; color:var(--muted); }
</style>
""", unsafe_allow_html=True)

TODAY = date.today()

# ── MOCK DATA ────────────────────────────────────────────
FACILITY = {
    "name": "Lone Star Care Center",
    "city": "Abilene, TX",
    "medicare_id": "67-5432",
    "don": "Linda Castillo, LVN",
    "total_beds": 120,
    "current_census": 98
}

cna_profiles = [
    {"cna_id":1,"first_name":"Rosa","last_name":"Martinez","phone":"(325) 555-0101",
     "license_number":"CNA-TX-112233","last_renewal_date": TODAY - timedelta(days=560),
     "expiration_date": TODAY + timedelta(days=160),"user_type":"Active CNA"},
    {"cna_id":2,"first_name":"Marco","last_name":"Diaz","phone":"(325) 555-0102",
     "license_number":"CNA-TX-204877","last_renewal_date": TODAY - timedelta(days=640),
     "expiration_date": TODAY + timedelta(days=48),"user_type":"Critical Window CNA"},
    {"cna_id":3,"first_name":"Aaliyah","last_name":"Brooks","phone":"(325) 555-0103",
     "license_number":"CNA-TX-318209","last_renewal_date": TODAY - timedelta(days=700),
     "expiration_date": TODAY + timedelta(days=12),"user_type":"Critical Window CNA"},
    {"cna_id":4,"first_name":"Ethan","last_name":"Cole","phone":"(325) 555-0104",
     "license_number":"STUDENT-001","last_renewal_date": TODAY,
     "expiration_date": TODAY + timedelta(days=730),"user_type":"Student CNA"},
]

ceu_records = [
    {"cna_id":1,"topic":"Infection Control","hours":4,"date": TODAY - timedelta(days=90),"geriatric":True,"dementia":False},
    {"cna_id":1,"topic":"Dementia & Alzheimer's Care","hours":3,"date": TODAY - timedelta(days=60),"geriatric":True,"dementia":True},
    {"cna_id":1,"topic":"Resident Rights & Dignity","hours":2,"date": TODAY - timedelta(days=30),"geriatric":False,"dementia":False},
    {"cna_id":2,"topic":"Infection Control","hours":4,"date": TODAY - timedelta(days=200),"geriatric":True,"dementia":False},
    {"cna_id":2,"topic":"Fall Prevention","hours":2,"date": TODAY - timedelta(days=100),"geriatric":True,"dementia":False},
    {"cna_id":3,"topic":"Infection Control","hours":4,"date": TODAY - timedelta(days=300),"geriatric":True,"dementia":False},
    {"cna_id":3,"topic":"Dementia Care","hours":3,"date": TODAY - timedelta(days=250),"geriatric":True,"dementia":True},
]

# ── FLASHCARDS ───────────────────────────────────────────
flashcards = [
    {"q":"What is the FIRST step in any clinical procedure?","a":"Perform hand hygiene (wash hands or use alcohol-based sanitizer).","domain":"Infection Control"},
    {"q":"How long must you scrub hands with soap and water?","a":"At least 20 seconds — friction on all surfaces including between fingers and under nails.","domain":"Infection Control"},
    {"q":"When must gloves be changed between tasks?","a":"Between each resident AND after touching contaminated surfaces — never reuse gloves.","domain":"Infection Control"},
    {"q":"What PPE is required for contact with body fluids?","a":"Gloves (minimum); add gown, mask, and eye protection based on splash risk.","domain":"Infection Control"},
    {"q":"Define 'clean to dirty' technique.","a":"Always move from the cleanest area to the dirtiest — never reverse direction to avoid spreading pathogens.","domain":"Infection Control"},
    {"q":"What are a resident's rights under federal law?","a":"Privacy, dignity, self-determination, freedom from abuse/restraint, access to records, right to refuse treatment.","domain":"Resident Rights"},
    {"q":"A resident refuses a bath. What should the CNA do?","a":"Respect the refusal, document it, and report to the nurse. Never force or coerce.","domain":"Resident Rights"},
    {"q":"What is 'dignity in care'?","a":"Treating every resident with respect, using their preferred name, maintaining privacy, and honoring choices.","domain":"Resident Rights"},
    {"q":"What is HIPAA and how does it affect CNAs?","a":"Health Insurance Portability and Accountability Act — CNAs must never share resident health info with unauthorized persons.","domain":"Resident Rights"},
    {"q":"What are the 5 rights of delegation?","a":"Right task, right circumstance, right person, right directions, right supervision.","domain":"Role of the Nurse Aide"},
    {"q":"What is the CNA's scope of practice in Texas?","a":"Assist with ADLs, take vitals, report observations to nurse — CNAs do NOT diagnose, prescribe, or create care plans.","domain":"Role of the Nurse Aide"},
    {"q":"What is the Texas Nurse Aide Registry (NAR)?","a":"HHSC database of all certified CNAs — tracks certification, renewals, and abuse/neglect findings.","domain":"Role of the Nurse Aide"},
    {"q":"Normal adult pulse rate range?","a":"60–100 beats per minute at rest.","domain":"Basic Nursing Skills"},
    {"q":"Normal adult respiratory rate?","a":"12–20 breaths per minute.","domain":"Basic Nursing Skills"},
    {"q":"Normal adult blood pressure?","a":"Less than 120/80 mmHg (systolic/diastolic).","domain":"Basic Nursing Skills"},
    {"q":"Normal oral temperature?","a":"98.6°F (37°C) — axillary is 1° lower, rectal is 1° higher.","domain":"Basic Nursing Skills"},
    {"q":"What is a 'dangling' position?","a":"Resident sits at the edge of the bed with feet hanging — used to prevent orthostatic hypotension before standing.","domain":"Basic Nursing Skills"},
    {"q":"What is the Fowler's position?","a":"Semi-sitting at 45–60°; High Fowler's is 90°. Used for breathing issues and eating.","domain":"Basic Nursing Skills"},
    {"q":"What does PRN mean?","a":"'Pro re nata' — as needed. Medication or care given only when the resident requires it.","domain":"Basic Nursing Skills"},
    {"q":"How do you measure urinary output?","a":"Pour urine into a graduate cylinder at eye level, read the amount in mL, record and report.","domain":"Basic Nursing Skills"},
    {"q":"What is the draw sheet technique?","a":"Using a draw sheet to lift and move a resident up in bed without friction — always use two caregivers.","domain":"Personal Care Skills"},
    {"q":"Signs of pressure injury (Stage 1)?","a":"Non-blanchable redness on intact skin — does NOT turn white when pressed. Report immediately.","domain":"Personal Care Skills"},
    {"q":"Where are pressure injuries most common?","a":"Bony prominences: sacrum, heels, hips, elbows, back of head.","domain":"Personal Care Skills"},
    {"q":"How often should a bedbound resident be repositioned?","a":"Every 2 hours — document position changes and skin condition.","domain":"Personal Care Skills"},
    {"q":"What is the purpose of a bed bath?","a":"Cleanliness, skin assessment, circulation stimulation, comfort, and dignity.","domain":"Personal Care Skills"},
    {"q":"Signs/symptoms of dehydration in elderly residents?","a":"Dry mouth, dark urine, confusion, decreased skin turgor, rapid weak pulse.","domain":"Mental Health & Social Needs"},
    {"q":"What is sundowning in dementia?","a":"Increased confusion, agitation, or wandering in late afternoon/evening — common in Alzheimer's disease.","domain":"Mental Health & Social Needs"},
    {"q":"How should a CNA respond to an agitated dementia resident?","a":"Stay calm, use simple words, redirect, maintain eye contact, avoid arguing or correcting.","domain":"Mental Health & Social Needs"},
    {"q":"What is Maslow's Hierarchy related to care?","a":"Meet physiological needs first (air, food, water, warmth), then safety, then emotional and social needs.","domain":"Mental Health & Social Needs"},
    {"q":"What are signs of depression in a resident?","a":"Withdrawal, loss of appetite, sleep changes, tearfulness, statements of hopelessness — report to nurse.","domain":"Mental Health & Social Needs"},
]

# ── CLINICAL SKILLS ──────────────────────────────────────
skills = [
    {"name":"Hand Washing","icon":"🧼",
     "prep":["Approach, identify, and greet resident","Explain procedure","Gather: soap, paper towels, nail cleaner"],
     "steps":["Turn on water — adjust to warm","Wet hands; apply soap","Scrub all surfaces vigorously for 20 seconds","Clean under fingernails","Rinse hands downward","Dry with paper towel","Turn off faucet with paper towel"],
     "critical":["Must scrub for full 20 seconds","Water must run downward (clean to dirty)","Never touch faucet with clean hands"],
     "mistakes":["Skipping nail beds","Not timing 20 seconds","Using same towel to turn off faucet"],
     "charting":"Procedure performed. Hand hygiene protocol followed per HHSC guidelines."},

    {"name":"Indirect Care / Measuring Vital Signs","icon":"🩺",
     "prep":["Identify resident with two identifiers","Explain procedure","Gather: BP cuff, stethoscope, thermometer, watch, pen, paper"],
     "steps":["Wash hands","Take pulse (radial — 60 seconds)","Count respirations (do NOT tell resident — count for 30 seconds × 2)","Take blood pressure (correct cuff size, arm at heart level)","Record temperature","Document all values immediately"],
     "critical":["Count respirations WITHOUT telling resident","BP cuff must be correct size","Document within scope — report abnormals immediately"],
     "mistakes":["Telling resident you're counting breaths (changes rate)","Using wrong BP cuff size","Rounding vital signs"],
     "charting":"Vital signs obtained and recorded. Abnormal values reported to charge nurse."},

    {"name":"Ambulation with Gait Belt","icon":"🚶",
     "prep":
