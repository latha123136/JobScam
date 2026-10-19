"""
Scam Detection API Routes
Core prediction endpoint with multi-modal analysis
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ml.scam_detector import scam_engine
from database.connection import predictions_collection, history_collection

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class JobAnalysisRequest(BaseModel):
    text: str
    url: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = "web"  # web, extension, api


class RiskScoreResponse(BaseModel):
    risk_score: int
    risk_level: str
    confidence: float
    ml_prediction: str
    ml_confidence: float
    scam_phrases_detected: List[str]
    urgency_phrases_detected: List[str]
    suspicious_salary_claims: List[str]
    red_flags: List[str]
    legitimacy_indicators: List[str]
    explanation: List[str]
    scam_phrase_score: int
    urgency_score: int
    salary_risk_score: int
    behavioral_score: int
    legitimacy_score: int


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/predict", response_model=RiskScoreResponse)
async def predict_scam(data: JobAnalysisRequest):
    """
    Analyze a job posting for scam indicators.
    Returns comprehensive risk assessment with explainability.
    """
    if not data.text or len(data.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Job text must be at least 10 characters")

    # Run multi-modal analysis — pass url and email so behavioral flags
    # incorporate domain-trust and recruiter-email signals directly.
    results = scam_engine.analyze_text(data.text, url=data.url, email=data.email)

    # Store prediction in database
    try:
        prediction_doc = {
            "text": data.text[:500],  # Store first 500 chars
            "url": data.url,
            "email": data.email,
            "source": data.source,
            "risk_score": results["risk_score"],
            "risk_level": results["risk_level"],
            "ml_prediction": results["ml_prediction"],
            "timestamp": datetime.utcnow().isoformat(),
        }
        await predictions_collection.insert_one(prediction_doc)
    except Exception:
        pass  # Don't fail prediction if DB write fails

    return RiskScoreResponse(**results)


@router.post("/quick-scan")
async def quick_scan(data: JobAnalysisRequest):
    """
    Quick scan endpoint for Chrome extension.
    Returns simplified risk assessment.
    """
    if not data.text or len(data.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Text too short for analysis")

    results = scam_engine.analyze_text(data.text, url=data.url, email=data.email)

    return {
        "risk_score": results["risk_score"],
        "risk_level": results["risk_level"],
        "confidence": results["confidence"],
        "top_reasons": results["explanation"][:3],
        "is_scam": results["risk_score"] > 60
    }
