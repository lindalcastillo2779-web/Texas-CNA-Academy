# Texas CNA Academy - Starter Template

This repository now includes a mobile-friendly Streamlit starter template with:

- Homepage hero and CTA actions
- Feature cards for core modules
- Hosted video embed section (YouTube)
- Placeholder infographic visuals
- Multi-page navigation for:
  - Exam Prep
  - Renewal Readiness
  - CEU Tracker
  - Staffing Compliance

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

- `app.py` - homepage + media + visuals
- `pages/` - module pages
- `styles/theme.css` - reusable theme styles
- `assets/images/` - placeholder infographics

## Customize next

1. Replace demo video URLs in `app.py` with official academy lessons.
2. Swap placeholder SVGs in `assets/images/` with branded infographics.
3. Connect CEU and staffing metrics to your production data source.
