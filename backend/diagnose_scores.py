import sys
sys.path.insert(0, '.')
from ml.scam_detector import scam_engine

TEST_CASES = [
    {"label": "OBVIOUS SCAM",        "text": "Earn 2 lakh per month from home. No interview needed. Pay registration fee of Rs 500. Urgent requirement. Join today. Work from home and earn 20000 daily. No experience required. Guaranteed placement. Contact on WhatsApp."},
    {"label": "SUBTLE SCAM",         "text": "Work from home data entry earn 5000 job. Simple copy paste job. Earn weekly. Immediate joining. No qualification required. Training fee applicable. Limited seats available."},
    {"label": "LEGIT - Software Eng","text": "We are hiring a Senior Software Engineer with 3-5 years of experience. Bachelor degree in Computer Science required. The role involves designing scalable backend systems using Python and FastAPI. Interview process includes a technical round and HR round. CTC: 18-22 LPA. Benefits include health insurance, provident fund, and annual leave. Notice period: 30 days. Background verification required."},
    {"label": "LEGIT - Marketing",   "text": "Marketing Manager role at ABC Corp. Requires master degree or equivalent with 5 years experience in digital marketing. Responsibilities include campaign management, team leadership, and analytics. Full-time position. Benefits include health insurance and performance bonus. Apply through our official portal. Probation period of 3 months. Reference check required."},
    {"label": "BORDERLINE WFH Tech", "text": "Software developer needed for remote work. Work from home opportunity. Earn competitive salary. Experience in React and Node.js required. Bachelor degree preferred. Interview process includes technical assessment. CTC 8-12 LPA."},
    {"label": "BORDERLINE Part time","text": "Part time content writer needed. Work from home. Earn 15000 per month. Flexible hours. No prior experience needed. Good English writing skills required. Payment weekly."},
]

print("=" * 75)
print(f"{'CASE':<28} {'SCORE':>6}  {'LEVEL':<16}  {'PHRASES':>7}  {'URGENCY':>7}  {'SALARY':>7}  {'BEHAV':>6}")
print("=" * 75)
for case in TEST_CASES:
    r = scam_engine.analyze_text(case["text"])
    print(f"{case['label']:<28} {r['risk_score']:>6}  {r['risk_level']:<16}  {r['scam_phrase_score']:>7}  {r['urgency_score']:>7}  {r['salary_risk_score']:>7}  {r['behavioral_score']:>6}")
    if r['scam_phrases_detected']:
        print(f"  phrases: {r['scam_phrases_detected']}")
    if r['red_flags']:
        print(f"  flags:   {r['red_flags']}")
print("=" * 75)
