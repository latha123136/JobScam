"""
Email Authenticity Analysis API
Detects fake recruiter emails, spoofed domains, and suspicious patterns
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import re

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class EmailAnalysisRequest(BaseModel):
    email: str


class EmailAnalysisResponse(BaseModel):
    email: str
    domain: str
    is_free_provider: bool
    is_corporate: bool
    trust_score: int
    risk_indicators: List[str]
    trust_indicators: List[str]
    verdict: str
    explanation: str


# ─── Analysis Logic ────────────────────────────────────────────────────────────

class EmailAnalyzer:
    """Recruiter email authenticity analyzer"""

    FREE_PROVIDERS = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "mail.com", "protonmail.com", "yandex.com", "aol.com",
        "zoho.com", "icloud.com", "live.com", "rediffmail.com",
        "gmx.com", "tutanota.com"
    ]

    KNOWN_CORPORATE_DOMAINS = [
        "tcs.com", "infosys.com", "wipro.com", "hcl.com",
        "cognizant.com", "accenture.com", "deloitte.com",
        "google.com", "microsoft.com", "amazon.com", "meta.com",
        "apple.com", "netflix.com", "flipkart.com", "paytm.com",
        "zomato.com", "swiggy.com", "ola.com", "uber.com",
        "linkedin.com", "salesforce.com", "oracle.com", "ibm.com"
    ]

    # Patterns that indicate fake HR emails
    FAKE_HR_PATTERNS = [
        r"hr\..*@gmail", r"hr\..*@yahoo", r"hr\..*@hotmail",
        r"recruit.*@gmail", r"career.*@gmail", r"jobs?\..*@gmail",
        r"hiring.*@gmail", r"placement.*@gmail", r"offer.*@gmail",
        r".*\.careers?@gmail", r".*\.jobs?@yahoo",
        r"hr[-_].*@(gmail|yahoo|hotmail)", r".*helpdesk@(gmail|yahoo)"
    ]

    def analyze(self, email: str) -> dict:
        """Comprehensive email authenticity analysis"""
        email = email.lower().strip()
        risk_indicators = []
        trust_indicators = []
        trust_score = 50

        # Validate email format
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return {
                "email": email,
                "domain": "",
                "is_free_provider": False,
                "is_corporate": False,
                "trust_score": 0,
                "risk_indicators": ["Invalid email format"],
                "trust_indicators": [],
                "verdict": "Invalid Email",
                "explanation": "The email address format is invalid."
            }

        # Extract domain
        domain = email.split("@")[1]
        username = email.split("@")[0]

        # ─── Free Provider Check ──────────────────────────────────────────
        is_free = domain in self.FREE_PROVIDERS
        if is_free:
            trust_score -= 20
            risk_indicators.append(f"Uses free email provider ({domain})")

        # ─── Corporate Domain Check ───────────────────────────────────────
        is_corporate = domain in self.KNOWN_CORPORATE_DOMAINS
        if is_corporate:
            trust_score += 30
            trust_indicators.append(f"Verified corporate domain: {domain}")

        # ─── Fake HR Pattern Detection ────────────────────────────────────
        for pattern in self.FAKE_HR_PATTERNS:
            if re.match(pattern, email):
                trust_score -= 30
                risk_indicators.append("Matches known fake HR email pattern")
                break

        # ─── Username Analysis ────────────────────────────────────────────
        hr_keywords = ["hr", "recruit", "career", "jobs", "hiring", "placement", "offer"]
        has_hr_keyword = any(kw in username for kw in hr_keywords)

        if has_hr_keyword and is_free:
            trust_score -= 25
            risk_indicators.append("HR/recruitment keyword with free email - likely fake")

        # ─── Domain Mismatch Detection ────────────────────────────────────
        company_names_in_email = re.findall(
            r"(amazon|google|microsoft|tcs|infosys|wipro|flipkart|meta|apple)", username
        )
        if company_names_in_email and is_free:
            trust_score -= 35
            risk_indicators.append(
                f"Claims to be from '{company_names_in_email[0]}' but uses {domain}"
            )

        # ─── Excessive Numbers/Special Chars ──────────────────────────────
        digit_count = sum(c.isdigit() for c in username)
        if digit_count > 4:
            trust_score -= 10
            risk_indicators.append("Username contains excessive numbers")

        if len(username) > 30:
            trust_score -= 5
            risk_indicators.append("Unusually long email username")

        # ─── Positive Signals ─────────────────────────────────────────────
        if not is_free and not is_corporate:
            trust_indicators.append("Uses custom domain (may be legitimate company)")
            trust_score += 10

        if re.match(r"^[a-z]+\.[a-z]+@", email):
            trust_indicators.append("Professional name format (firstname.lastname)")
            trust_score += 5

        # Clamp score
        trust_score = max(0, min(100, trust_score))

        # Verdict
        if trust_score >= 70:
            verdict = "Likely Authentic"
        elif trust_score >= 45:
            verdict = "Uncertain - Verify Independently"
        elif trust_score >= 25:
            verdict = "Suspicious - Likely Fake"
        else:
            verdict = "Fraudulent - Do Not Trust"

        # Generate explanation
        explanation = self._generate_explanation(
            email, domain, is_free, is_corporate, risk_indicators, trust_score
        )

        return {
            "email": email,
            "domain": domain,
            "is_free_provider": is_free,
            "is_corporate": is_corporate,
            "trust_score": trust_score,
            "risk_indicators": risk_indicators,
            "trust_indicators": trust_indicators,
            "verdict": verdict,
            "explanation": explanation
        }

    def _generate_explanation(self, email, domain, is_free, is_corporate,
                              risk_indicators, trust_score) -> str:
        """Generate human-readable explanation"""
        if trust_score >= 70:
            return f"This email appears legitimate. It uses a {'corporate' if is_corporate else 'custom'} domain."
        elif trust_score >= 45:
            return f"This email has some uncertain signals. Verify the sender through official company channels."
        else:
            reasons = "; ".join(risk_indicators[:3])
            return f"This email is likely fraudulent. Reasons: {reasons}. Do not share personal information."


email_analyzer = EmailAnalyzer()


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/analyze-email", response_model=EmailAnalysisResponse)
async def analyze_email(data: EmailAnalysisRequest):
    """Analyze a recruiter email for authenticity"""
    if not data.email or "@" not in data.email:
        raise HTTPException(status_code=400, detail="Please provide a valid email address")

    results = email_analyzer.analyze(data.email)
    return EmailAnalysisResponse(**results)
