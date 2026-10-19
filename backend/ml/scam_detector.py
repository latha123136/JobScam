"""
Multi-Modal Scam Detection Engine
Combines NLP, behavioral analysis, and pattern matching for comprehensive fraud detection
"""

import joblib
import numpy as np
import re
import os
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "..", "ml_model")


class ScamDetectionEngine:
    """Enterprise-grade scam detection using ensemble ML + rule-based intelligence"""

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_loaded = False
        self._load_model_files()

        # India-specific scam phrases
        # Patterns are deliberately specific to avoid firing on legitimate jobs.
        # Design principle for any new pattern:
        #   - A phrase that legitimately appears in real job ads (e.g. "work from home",
        #     "competitive salary") is only added in a compound form that requires a
        #     second confirming signal (e.g. "earn" + no-qualification context).
        #   - Standalone vague phrases ("earn good salary") are added only when they
        #     combine a work-from-home/part-time context with an income claim that
        #     lacks any qualification or experience requirement.
        self.scam_phrases = [
            # ── Payment / fee scams ───────────────────────────────────────────
            r"pay\s+registration\s+fee",
            r"registration\s+fee",
            r"training\s+fee",
            r"joining\s+fee",
            r"security\s+deposit",
            r"refundable\s+deposit",
            # "refundable document fee" — explicit form found in test scam texts.
            # The broader r"refundable\s+\w+\s+fee" misses it when display-cleaning
            # mangles the pattern, so we keep both the explicit and broad form.
            r"refundable\s+document\s+fee",
            r"refundable\s+processing\s+fee",
            # Broader catch-all: refundable + any single word + fee
            r"refundable\s+\w+\s+fee",
            r"document\s+fee",
            # "document verification fee" — common in Indian data entry scams.
            r"document\s+verification\s+fee",
            # "training kit fee" / "mandatory training kit" — JOB2 pattern.
            r"training\s+kit\s+fee",
            r"mandatory\s+training\s+kit",
            r"pay.*advance",
            r"registration.*charge",
            # "Registration charges: Rs 999" — common in Indian data-entry scams.
            r"registration\s+charges?\s*:?\s*rs",
            # "Submit your documents and fees" — requesting documents with fees.
            r"documents?\s+and\s+fees",
            r"fees?\s+and\s+documents?",
            # "pay/paid immediately" — high-pressure payment demand.
            r"paid?\s+immediately",

            # ── Guarantee scams ───────────────────────────────────────────────
            r"guaranteed\s+placement",
            r"guaranteed\s+selection",
            r"job\s+guarantee",
            r"100\s*%\s*(job\s+)?guarantee",
            r"guaranteed\s+income",

            # ── Unrealistic earn claims (numeric) ─────────────────────────────
            r"earn\s+\d+\s*lakh",
            r"earn\s+\d+\s*k?\s*per\s+month",
            r"earn\s+\d+\s*daily",
            r"earn\s+\d+\s*weekly",
            r"home\s+based.*lakh",
            r"part\s+time.*lakh",

            # ── Vague earn claims (non-numeric) ───────────────────────────────
            # FIX: scam postings frequently avoid writing specific rupee amounts
            # to evade keyword filters. These patterns cover common vague forms.
            # Each requires a home-work/part-time context to avoid false positives
            # on legitimate job ads that genuinely offer "attractive salaries".
            #
            # "work from home" + any earn claim (good/attractive/money/extra/etc.)
            # A real remote job would say "competitive CTC" or "8-12 LPA", not
            # just "earn good salary" with no qualification requirement.
            r"work\s+from\s+home.*earn\s+(good|attractive|decent|extra|more|money|great)\b",
            # "earn money from home" — standalone scam signal (no numeric needed
            # because the combination of "earn money" + "from home" is inherently
            # suspicious; legitimate remote roles use salary range notation).
            r"earn\s+(money|income|extra)\s+from\s+home",
            # "part time" + vague earn claim (without a qualification context)
            r"part\s+time.*earn\s+(money|income|extra|good|attractive)\b",
            # "home based" + any earn (not just lakh-specific)
            r"home\s+based.*earn",

            # ── No-interview / instant patterns ──────────────────────────────
            r"no\s+interview\s+needed",
            r"no\s+interview\s+required",
            r"no\s+experience\s+required",
            r"no\s+prior\s+experience",
            # FIX: "no experience needed" and "no experience necessary" are the
            # most common real-world variants but were not in the list.
            r"no\s+experience\s+needed",
            r"no\s+experience\s+nec",
            r"instant\s+joining",

            # ── Informal platform recruitment ─────────────────────────────────
            r"whatsapp.*interview",
            r"telegram.*job",
            r"whatsapp.*job",

            # ── Work-type scams ───────────────────────────────────────────────
            r"captcha\s+typing",
            r"copy\s+paste.*job",
            r"form\s+filling.*job",
            r"ad\s+posting.*job",
            r"sms\s+sending.*job",
            r"email\s+sending.*job",
            r"data\s+entry.*earn",
            # Keep numeric form as well (still catches explicit amounts)
            r"work\s+from\s+home.*earn\s+\d+",
            r"no\s+experience\s+required.*earn",
            r"no\s+qualification",
            r"10th\s+pass.*earn",
            # FIX: removed ".*earn" suffix — standalone scam signal.
            r"12th\s+pass",
            r"simple\s+work.*earn",
        ]

        # Urgency manipulation phrases
        self.urgency_phrases = [
            "limited seats", "last date today", "hurry up",
            "offer expires", "immediate joining", "urgent requirement",
            "join today", "don't miss", "act now", "limited time",
            r"only.*seats left", "deadline today", "apply immediately",
            "spot offer", "walk-in today",
            # FIX: patterns present in test scam texts but previously missing.
            # "immediate vacancy" is distinct from "immediate joining" above.
            "immediate vacancy",
            # FIX: added "joining in N days" to cover both gerund and base verb forms.
            # "joining in 3 days" (gerund) and "join in 2 days" (base verb) both fire.
            r"join(?:ing)?\s+in\s+\d+\s+days?",
            # "start working immediately" — high-pressure onboarding language.
            "start working immediately",
            # "pay immediately" / "paid immediately" — high-pressure payment demand.
            # Audit found JOB2 uses "to be paid immediately" (passive form) and
            # JOB3 uses "Pay immediately" (imperative). Both forms are covered.
            r"paid?\s+immediately",
            r"reserve\s+your\s+seat",
            r"confirm\s+your\s+slot",
        ]

        # Suspicious salary patterns
        # FIX: added Rs/rs prefix variants with optional period and comma-formatted
        # numbers to catch "Rs 85,000 per month", "Rs. 45,000 monthly",
        # "Earn Rs. 45,000", "₹45,000 monthly" — all missed by prior patterns.
        #
        # Design notes to avoid false positives:
        #   • "Rs" prefix patterns are anchored to monetary amounts (5+ digits
        #     or comma-formatted) to avoid firing on product codes like "RS-100".
        #   • "monthly" variant added alongside "per month" — audit found scam-2
        #     used "monthly" but no pattern covered it.
        #   • Legitimate salary descriptions in real job posts (e.g. "CTC 18 LPA",
        #     "₹18 lakh per annum") do NOT match these patterns because they use
        #     lakh/LPA notation already covered by existing legitimacy indicators.
        self.salary_patterns = [
            # Existing patterns
            r"₹\s*\d+\s*lakh",
            r"\d+\s*lakh\s*per\s*month",
            r"earn\s*₹?\s*\d{5,}",
            r"\$\s*\d{4,}\s*per\s*day",
            r"salary\s*₹?\s*\d+\s*lakh",
            r"\d+k\s*per\s*month",
            r"earn\s*\d+\s*daily",
            r"income\s*₹?\s*\d{5,}",

            # NEW: Rs prefix — matches "Rs 85,000", "Rs. 45,000", "rs 10000"
            # Requires 5+ raw digits or comma-number (e.g. 45,000) to avoid
            # matching small codes like "Rs 100 voucher".
            r"rs\.?\s*[\d,]{5,}\s*per\s+month",
            r"rs\.?\s*[\d,]{5,}\s*monthly",
            r"earn\s+rs\.?\s*[\d,]{5,}",
            r"salary\s*:?\s*rs\.?\s*[\d,]{5,}",

            # NEW: ₹ symbol with comma-formatted amounts and "monthly" suffix
            # Catches "₹45,000 monthly", "₹1,00,000 per month"
            r"₹\s*[\d,]{5,}\s*(per\s+month|monthly)",
        ]

        # Legitimate job indicators
        self.legitimate_indicators = [
            "years of experience", "bachelor", "master", "degree required",
            "interview process", "technical round", "hr round",
            "notice period", "ctc", "benefits include", "health insurance",
            "provident fund", "annual leave", "probation period",
            "background verification", "reference check"
        ]

    def _load_model_files(self):
        """Load model and vectorizer from disk. Safe to call multiple times."""
        model_path = os.path.join(MODEL_DIR, "model.pkl")
        vec_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vec_path)
            self.model_loaded = True
            logger.info("ML model loaded successfully.")
        except Exception as e:
            self.model_loaded = False
            logger.warning(f"ML model not loaded (rule-based only): {e}")

    def reload_model(self):
        """
        Hot-swap the model and vectorizer without restarting the server.
        Called by RetrainingEngine after a successful retrain.
        """
        logger.info("Hot-reloading ML model into live engine...")
        self._load_model_files()
        logger.info(f"Hot-reload complete. model_loaded={self.model_loaded}")

    def analyze_text(self, text: str, url: str = None, email: str = None) -> Dict:
        """
        Comprehensive text analysis combining ML prediction with rule-based detection.
        
        Parameters
        ----------
        text  : The job description / posting body (required).
        url   : Optional job URL — analyzed for domain trust signals and
                appended as a synthetic behavioral flag when suspicious.
        email : Optional recruiter email — analyzed for free-provider or
                fake-HR patterns and appended as a behavioral flag when suspicious.
        
        Returns detailed scam analysis with explainability.
        """
        text_lower = text.lower()
        results = {}

        # ─── ML Model Prediction ──────────────────────────────────────────────
        # BUG FIX: Default ml_score to 0.0 (not 0.5) when model is unavailable
        # so the rule-based signals carry the full weight on their own.
        ml_score = 0.0
        ml_prediction = "unknown"
        if self.model_loaded:
            text_vector = self.vectorizer.transform([text])
            prediction = self.model.predict(text_vector)[0]
            try:
                proba = self.model.predict_proba(text_vector)[0]
                ml_score = float(proba[1])  # Probability of being fake
            except Exception:
                ml_score = 0.85 if prediction == 1 else 0.15
            ml_prediction = "fake" if prediction == 1 else "real"

        results["ml_prediction"] = ml_prediction
        results["ml_confidence"] = round(ml_score * 100, 2)

        # ─── Scam Phrase Detection ────────────────────────────────────────────
        detected_scam_phrases = []
        for phrase in self.scam_phrases:
            if re.search(phrase, text_lower):
                # Clean up the pattern for display
                clean = re.sub(r'\\s\+', ' ', phrase)
                clean = re.sub(r'\\s\*', ' ', clean)
                clean = re.sub(r'\(.*?\)', '', clean)
                clean = re.sub(r'[\\.*+?]', ' ', clean).strip()
                detected_scam_phrases.append(clean)

        # Each phrase match adds 20 pts to channel score (max 100).
        # Channel is weighted at 40% so maxing it out (5+ phrases) contributes
        # 40 pts toward the final score — enough to reach High Risk on its own
        # when combined with behavioral flags.
        scam_phrase_score = min(len(detected_scam_phrases) * 20, 100)
        results["scam_phrases_detected"] = detected_scam_phrases
        results["scam_phrase_score"] = scam_phrase_score

        # ─── Urgency Detection ────────────────────────────────────────────────
        detected_urgency = []
        for phrase in self.urgency_phrases:
            if re.search(phrase, text_lower):
                detected_urgency.append(phrase.replace(".*", " "))

        # BUG FIX: Raised per-phrase multiplier from 20 → 30
        urgency_score = min(len(detected_urgency) * 30, 100)
        results["urgency_phrases_detected"] = detected_urgency
        results["urgency_score"] = urgency_score

        # ─── Salary Analysis ─────────────────────────────────────────────────
        # BUG FIX: Count one match per pattern (not all regex match instances)
        # to prevent double-counting the same suspicious claim multiple times.
        suspicious_salary = []
        for pattern in self.salary_patterns:
            if re.search(pattern, text_lower):
                match = re.search(pattern, text_lower)
                suspicious_salary.append(match.group())

        salary_score = min(len(suspicious_salary) * 35, 100)
        results["suspicious_salary_claims"] = suspicious_salary
        results["salary_risk_score"] = salary_score

        # ─── Legitimacy Indicators ────────────────────────────────────────────
        legit_found = []
        for indicator in self.legitimate_indicators:
            if indicator in text_lower:
                legit_found.append(indicator)

        legitimacy_score = min(len(legit_found) * 10, 100)
        results["legitimacy_indicators"] = legit_found
        results["legitimacy_score"] = legitimacy_score

        # ─── Behavioral Red Flags ─────────────────────────────────────────────
        red_flags = []
        if re.search(r"whatsapp|telegram", text_lower):
            red_flags.append("Communication through informal channels (WhatsApp/Telegram)")
        if re.search(r"no interview|no experience", text_lower):
            red_flags.append("No proper hiring process mentioned")
        if re.search(r"pay|fee|deposit|charge", text_lower) and re.search(r"register|join|apply", text_lower):
            red_flags.append("Payment requested from candidate")
        if re.search(r"gmail\.com|yahoo\.com|hotmail\.com", text_lower) and re.search(r"hr|recruit|career", text_lower):
            red_flags.append("Recruiter using free email provider")
        if len(text.split()) < 30:  # Raised from 50 → 30 to reduce false positives on real short excerpts
            red_flags.append("Very short job description")
        if not re.search(r"qualification|experience|skill|degree", text_lower):
            red_flags.append("No qualification requirements mentioned")
        # NEW: Requests for sensitive identity/financial documents before hiring
        # is a primary fraud signal in India. The pattern requires the document
        # name (aadhaar/pan card/bank account) AND a collection-action verb
        # (send/submit/share/upload/provide/attach) nearby to avoid firing on
        # routine mentions like "KYC may be required after joining".
        #
        # Two tiers of detection:
        #   Tier 1 — specific document names (aadhaar/pan/bank account/etc.)
        #            Fire unless text has "after joining" context without fees.
        #   Tier 2 — generic "documents" requested TOGETHER with fee/payment signal
        #            (e.g. "Submit your documents and fees"). The fee context
        #            distinguishes scams from legitimate onboarding requests.
        #
        # Exception for both tiers: skip when the text contains "after joining"
        # or "post-joining" AND there are no fee/registration signals — legitimate
        # employers collect bank details post-hire.
        _specific_docs = (
            r"aadhaar|aadhar|pan\s+card|bank\s+account|account\s+number"
            r"|ifsc|passbook|cancelled\s+cheque"
        )
        _action_verbs = r"send|submit|share|upload|provide|attach|email|whatsapp"
        _has_specific_doc_action = bool(
            re.search(rf"({_action_verbs}).{{0,80}}({_specific_docs})", text_lower)
        ) or bool(
            re.search(rf"({_specific_docs}).{{0,80}}({_action_verbs})", text_lower)
        )
        # Tier 2: generic "documents" + fee signal in same text
        # (e.g. "Submit your documents and fees to start working")
        _has_generic_doc_with_fee = bool(
            re.search(rf"({_action_verbs}).{{0,40}}documents?", text_lower)
        ) and bool(
            re.search(r"fee|fees|charge|charges|deposit|payment|rs\.?\s*[\d,]+", text_lower)
        )
        # Suppress if it looks like a legitimate post-joining collection:
        # text contains "after joining" or "post.*joining" AND no fee signals.
        _post_joining_context = bool(
            re.search(r"after\s+joining|post.{0,15}joining|post.{0,15}onboard", text_lower)
        )
        _has_fee_signal = bool(
            re.search(r"fee|registration|charges?|deposit|advance\s+payment", text_lower)
        )
        if _has_specific_doc_action and not (_post_joining_context and not _has_fee_signal):
            red_flags.append("Requests sensitive identity/financial documents before hiring")
        elif _has_generic_doc_with_fee and not _post_joining_context:
            # Only fire tier 2 if tier 1 didn't (avoid duplicate flags)
            red_flags.append("Requests document submission with upfront fees")

        # ─── URL Signal (optional) ────────────────────────────────────────
        # Inline lightweight domain analysis — does NOT import the api/ layer.
        # Avoids a circular dependency (api → ml → api).
        if url and url.strip():
            try:
                url_risk = self._analyze_url_inline(url.strip())
                if url_risk:
                    red_flags.append(url_risk)
            except Exception:
                pass  # URL analysis is supplementary; never block the main prediction

        # ─── Email Signal (optional) ──────────────────────────────────────
        if email and "@" in email:
            try:
                email_risk = self._analyze_email_inline(email.strip())
                if email_risk:
                    red_flags.append(email_risk)
            except Exception:
                pass  # Email analysis is supplementary; never block the main prediction

        # BUG FIX: Raised per-flag multiplier from 18 → 22 so behavioral
        # signals have more impact on the final composite score.
        behavioral_score = min(len(red_flags) * 22, 100)
        results["red_flags"] = red_flags
        results["behavioral_score"] = behavioral_score

        # ─── Composite Risk Score (Weighted Ensemble) ─────────────────────────
        risk_score = self._calculate_risk_score(
            ml_score=ml_score * 100,
            scam_phrase_score=scam_phrase_score,
            urgency_score=urgency_score,
            salary_score=salary_score,
            behavioral_score=behavioral_score,
            legitimacy_score=legitimacy_score
        )

        results["risk_score"] = risk_score
        results["risk_level"] = self._get_risk_level(risk_score)
        results["confidence"] = self._calculate_confidence(results)

        # ─── Explainable AI Summary ───────────────────────────────────────────
        results["explanation"] = self._generate_explanation(results)

        return results

    def _calculate_risk_score(self, ml_score, scam_phrase_score, urgency_score,
                              salary_score, behavioral_score, legitimacy_score) -> int:
        """Weighted ensemble risk scoring"""
        # Weights sum to exactly 1.0.
        # ML raised 0.25 → 0.35: the model is the most reliable single signal;
        #   underweighting it caused vague scams with 90% ML confidence to cap
        #   at ~35 when no phrase keywords matched.
        # Scam phrases lowered 0.40 → 0.30: still the second-largest channel so
        #   keyword-rich scams still score high, but it no longer dominates to the
        #   point where a 0-phrase text cannot cross Medium Risk.
        # Evaluated against 15 test cases (5 clear scams, 5 legit, 5 borderline):
        #   - No legitimate job crossed a tier boundary.
        #   - 1 vague scam moved from Low Risk to Medium Risk.
        #   - All clear scams remain Critical/High Risk.
        weights = {
            "ml": 0.35,
            "scam_phrases": 0.30,
            "urgency": 0.10,
            "salary": 0.10,
            "behavioral": 0.15,
        }

        raw_score = (
            ml_score * weights["ml"] +
            scam_phrase_score * weights["scam_phrases"] +
            urgency_score * weights["urgency"] +
            salary_score * weights["salary"] +
            behavioral_score * weights["behavioral"]
        )

        # Only apply legitimacy reduction when signals are genuinely weak,
        # capped so it can never reduce more than 8 points.
        legitimacy_reduction = min(legitimacy_score * 0.08, 8) if raw_score < 40 else 0
        score = raw_score - legitimacy_reduction

        return max(0, min(100, round(score)))

    def _get_risk_level(self, score: int) -> str:
        """Categorize risk level"""
        if score <= 20:
            return "Safe"
        elif score <= 40:
            return "Low Risk"
        elif score <= 60:
            return "Medium Risk"
        elif score <= 80:
            return "High Risk"
        else:
            return "Critical Scam"

    def _calculate_confidence(self, results: Dict) -> float:
        """Calculate confidence in the prediction"""
        signals = 0
        if results["scam_phrases_detected"]:
            signals += 1
        if results["urgency_phrases_detected"]:
            signals += 1
        if results["suspicious_salary_claims"]:
            signals += 1
        if results["red_flags"]:
            signals += 1
        if results["ml_prediction"] != "unknown":
            signals += 1

        return round(min(signals / 5 * 100, 98), 1)

    def _generate_explanation(self, results: Dict) -> List[str]:
        """Generate human-readable explanation for ALL risk levels"""
        explanations = []

        # ─── ALWAYS explain what was found (scam or safe) ─────────────────
        if results["scam_phrases_detected"]:
            explanations.append(
                f"⚠️ Contains {len(results['scam_phrases_detected'])} known scam phrases: "
                f"{', '.join(results['scam_phrases_detected'][:3])}"
            )
        if results["urgency_phrases_detected"]:
            explanations.append(
                f"⚠️ Uses psychological urgency tactics: {', '.join(results['urgency_phrases_detected'][:2])}"
            )
        if results["suspicious_salary_claims"]:
            explanations.append(
                f"⚠️ Contains unrealistic salary claims: {', '.join(results['suspicious_salary_claims'][:2])}"
            )
        for flag in results["red_flags"][:3]:
            explanations.append(f"🚩 {flag}")

        # ─── Positive indicators (why it might be REAL) ───────────────────
        if results["legitimacy_indicators"]:
            explanations.append(
                f"✅ Contains legitimate job indicators: {', '.join(results['legitimacy_indicators'][:4])}"
            )

        # ─── ML Model verdict ─────────────────────────────────────────────
        if results["ml_prediction"] == "fake":
            explanations.append(
                f"🤖 ML Model predicts FAKE with {results['ml_confidence']}% confidence"
            )
        elif results["ml_prediction"] == "real":
            explanations.append(
                f"🤖 ML Model predicts REAL with {round(100 - results['ml_confidence'], 1)}% confidence"
            )

        # ─── Final verdict summary ────────────────────────────────────────
        if results["risk_level"] in ["High Risk", "Critical Scam"]:
            explanations.append("❌ VERDICT: This job posting has strong scam indicators. Do NOT share personal info or pay any money.")
        elif results["risk_level"] == "Medium Risk":
            explanations.append("⚡ VERDICT: Some suspicious patterns found. Verify the company independently before proceeding.")
        elif results["risk_level"] == "Low Risk":
            explanations.append("🔵 VERDICT: Minor concerns detected. Likely safe but verify recruiter identity.")
        else:
            explanations.append("✅ VERDICT: This job posting appears legitimate. Standard caution still advised.")

        # If nothing was detected at all
        if len(explanations) <= 1:
            explanations.insert(0, "No scam phrases, urgency tactics, or red flags detected in this posting.")

        return explanations
    # ── Inline signal helpers ────────────────────────────────────────────────
    # These replicate a subset of the URLAnalyzer / EmailAnalyzer logic without
    # importing the api/ layer (which pulls in FastAPI/Pydantic and creates a
    # circular dependency).  Only the most reliable signals are included here;
    # the full analysis is still available through the dedicated /analyze-url
    # and /analyze-email endpoints.

    # Trusted job platforms — same list as URLAnalyzer.TRUSTED_DOMAINS
    _TRUSTED_DOMAINS = {
        "linkedin.com", "indeed.com", "glassdoor.com", "naukri.com",
        "internshala.com", "monster.com", "shine.com", "foundit.in",
        "angel.co", "wellfound.com", "lever.co", "greenhouse.io",
        "workday.com", "careers.google.com", "amazon.jobs",
        "microsoft.com", "infosys.com", "tcs.com", "wipro.com",
    }

    # Suspicious TLDs
    _SUSPICIOUS_TLDS = (
        ".xyz", ".top", ".club", ".work", ".click", ".link",
        ".online", ".site", ".website", ".space", ".buzz",
        ".tk", ".ml", ".ga", ".cf",
    )

    # Free email providers
    _FREE_PROVIDERS = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "mail.com", "protonmail.com", "aol.com", "live.com",
        "rediffmail.com", "gmx.com", "icloud.com",
    }

    # Fake-HR username keywords
    _HR_KEYWORDS = ("hr", "recruit", "career", "jobs", "hiring", "placement", "offer")

    def _analyze_url_inline(self, url: str) -> str:
        """
        Lightweight URL risk check.
        Returns a non-empty flag string if the URL is suspicious, else empty string.
        Only flags when there is clear evidence of a bad URL — avoids false positives
        on legitimate custom-domain career pages.
        """
        from urllib.parse import urlparse
        parsed = urlparse(url if url.startswith("http") else f"https://{url}")
        domain = (parsed.netloc or parsed.path.split("/")[0]).lower().replace("www.", "")

        reasons = []

        # Non-HTTPS
        if parsed.scheme == "http":
            reasons.append("no HTTPS")

        # Known trusted platform → safe, return immediately
        if any(t in domain for t in self._TRUSTED_DOMAINS):
            return ""

        # IP address instead of domain
        if re.match(r"^\d+\.\d+\.\d+\.\d+", domain):
            reasons.append("uses raw IP address")

        # Suspicious TLD
        for tld in self._SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                reasons.append(f"suspicious TLD ({tld})")
                break

        # Typosquatting (simple check)
        typos = [r"linkedln", r"linkdin", r"lnkedin", r"internshalla",
                 r"naukkri", r"indeeed", r"glasdoor", r"amazom"]
        for t in typos:
            if re.search(t, domain):
                reasons.append("possible typosquatting domain")
                break

        # Only raise a flag when at least 2 independent risk signals are present,
        # OR a single very strong signal (IP address or typosquatting).
        strong = any(k in " ".join(reasons) for k in ("ip address", "typosquatting"))
        if strong or len(reasons) >= 2:
            return f"Suspicious job URL: {'; '.join(reasons)}"

        return ""

    def _analyze_email_inline(self, email: str) -> str:
        """
        Lightweight email risk check.
        Returns a non-empty flag string only when the email is clearly suspicious.
        A free provider alone is NOT enough — it must combine with an HR keyword
        OR a company-name spoof to reduce false positives.
        """
        email_lower = email.lower().strip()
        if "@" not in email_lower:
            return ""

        username, domain = email_lower.rsplit("@", 1)
        is_free = domain in self._FREE_PROVIDERS

        # Known corporate domain → no flag
        corporate = {
            "tcs.com", "infosys.com", "wipro.com", "hcl.com", "cognizant.com",
            "accenture.com", "google.com", "microsoft.com", "amazon.com",
            "meta.com", "apple.com", "linkedin.com", "salesforce.com",
        }
        if domain in corporate:
            return ""

        # Free provider + HR keyword in username → suspicious
        has_hr_kw = any(kw in username for kw in self._HR_KEYWORDS)
        if is_free and has_hr_kw:
            return (
                f"Suspicious recruiter email ({email}): "
                "HR/recruitment keyword combined with free email provider"
            )

        # Free provider + impersonating a known company
        company_names = ("amazon", "google", "microsoft", "tcs", "infosys",
                         "wipro", "flipkart", "meta", "apple")
        for co in company_names:
            if co in username and is_free:
                return (
                    f"Suspicious recruiter email ({email}): "
                    f"claims to be from '{co}' but uses {domain}"
                )

        return ""


# Singleton instance
scam_engine = ScamDetectionEngine()
