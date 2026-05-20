"""
Multi-Modal Scam Detection Engine
Combines NLP, behavioral analysis, and pattern matching for comprehensive fraud detection
"""

import joblib
import numpy as np
import re
from typing import Dict, List, Tuple


class ScamDetectionEngine:
    """Enterprise-grade scam detection using ensemble ML + rule-based intelligence"""

    def __init__(self):
        # Load trained ML model and vectorizer
        try:
            self.model = joblib.load("../ml_model/model.pkl")
            self.vectorizer = joblib.load("../ml_model/vectorizer.pkl")
            self.model_loaded = True
        except Exception:
            self.model_loaded = False

        # India-specific scam phrases
        self.scam_phrases = [
            "earn .* lakh", "earn .* per month", "no interview",
            "instant joining", "pay registration fee", "guaranteed placement",
            "captcha typing", "work from home.*earn", "no experience required.*earn",
            "pay.*fee", "registration.*charge", "security deposit",
            "whatsapp.*interview", "telegram.*job", "data entry.*earn",
            "copy paste.*job", "form filling.*job", "ad posting.*job",
            "sms sending.*job", "email sending.*job", "pay.*advance",
            "refundable.*deposit", "training fee", "joining fee",
            "earn.*daily", "earn.*weekly", "guaranteed.*income",
            "no qualification", "10th pass.*earn", "12th pass.*earn",
            "part time.*lakh", "full time.*lakh", "simple work.*earn",
            "mobile.*job", "laptop.*job", "home based.*lakh"
        ]

        # Urgency manipulation phrases
        self.urgency_phrases = [
            "limited seats", "last date today", "hurry up",
            "offer expires", "immediate joining", "urgent requirement",
            "join today", "don't miss", "act now", "limited time",
            "only.*seats left", "deadline today", "apply immediately",
            "spot offer", "walk-in today"
        ]

        # Suspicious salary patterns
        self.salary_patterns = [
            r"₹\s*\d+\s*lakh", r"\d+\s*lakh\s*per\s*month",
            r"earn\s*₹?\s*\d{5,}", r"\$\s*\d{4,}\s*per\s*day",
            r"salary\s*₹?\s*\d+\s*lakh", r"\d+k\s*per\s*month",
            r"earn\s*\d+\s*daily", r"income\s*₹?\s*\d{5,}"
        ]

        # Legitimate job indicators
        self.legitimate_indicators = [
            "years of experience", "bachelor", "master", "degree required",
            "interview process", "technical round", "hr round",
            "notice period", "ctc", "benefits include", "health insurance",
            "provident fund", "annual leave", "probation period",
            "background verification", "reference check"
        ]

    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive text analysis combining ML prediction with rule-based detection
        Returns detailed scam analysis with explainability
        """
        text_lower = text.lower()
        results = {}

        # ─── ML Model Prediction ──────────────────────────────────────────────
        ml_score = 0.5
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
                detected_scam_phrases.append(phrase.replace(".*", " "))

        scam_phrase_score = min(len(detected_scam_phrases) * 18, 100)
        results["scam_phrases_detected"] = detected_scam_phrases
        results["scam_phrase_score"] = scam_phrase_score

        # ─── Urgency Detection ────────────────────────────────────────────────
        detected_urgency = []
        for phrase in self.urgency_phrases:
            if re.search(phrase, text_lower):
                detected_urgency.append(phrase.replace(".*", " "))

        urgency_score = min(len(detected_urgency) * 20, 100)
        results["urgency_phrases_detected"] = detected_urgency
        results["urgency_score"] = urgency_score

        # ─── Salary Analysis ─────────────────────────────────────────────────
        suspicious_salary = []
        for pattern in self.salary_patterns:
            matches = re.findall(pattern, text_lower)
            suspicious_salary.extend(matches)

        salary_score = min(len(suspicious_salary) * 25, 100)
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
        if len(text.split()) < 50:
            red_flags.append("Very short job description")
        if not re.search(r"qualification|experience|skill|degree", text_lower):
            red_flags.append("No qualification requirements mentioned")

        behavioral_score = min(len(red_flags) * 18, 100)
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
        weights = {
            "ml": 0.25,
            "scam_phrases": 0.30,
            "urgency": 0.10,
            "salary": 0.15,
            "behavioral": 0.20,
            "legitimacy": -0.05  # Reduces risk
        }

        score = (
            ml_score * weights["ml"] +
            scam_phrase_score * weights["scam_phrases"] +
            urgency_score * weights["urgency"] +
            salary_score * weights["salary"] +
            behavioral_score * weights["behavioral"] +
            legitimacy_score * weights["legitimacy"]
        )

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


# Singleton instance
scam_engine = ScamDetectionEngine()
