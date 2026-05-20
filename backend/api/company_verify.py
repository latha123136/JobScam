"""
Company Authenticity Verification API
Complete company verification with domain analysis, WHOIS, SSL, and risk scoring
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

import sys
sys.path.insert(0, '..')

from services.company_engine import CompanyAuthenticityEngine

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class CompanyVerifyRequest(BaseModel):
    company_name: str
    website: Optional[str] = None
    email: Optional[str] = None
    source_platform: Optional[str] = None


class CompanyVerifyResponse(BaseModel):
    company_name: str
    company_existence_years: Optional[float] = None
    company_founded_year: Optional[int] = None
    domain_existence_years: Optional[float] = None
    domain_creation_date: Optional[str] = None
    legitimacy_score: int
    scam_probability: int
    trust_level: str
    verification_status: str
    linkedin_presence: str
    email_authenticity: str
    website_security: str
    domain_registrar: Optional[str] = None
    ssl_valid: Optional[bool] = None
    dns_resolves: Optional[bool] = None
    risk_flags: List[str]
    trust_signals: List[str]
    checks_performed: List[dict]
    analysis_summary: str
    recommendation: str


# ─── Engine Instance ───────────────────────────────────────────────────────────

engine = CompanyAuthenticityEngine()


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/verify-company", response_model=CompanyVerifyResponse)
async def verify_company(data: CompanyVerifyRequest):
    """
    Comprehensive company authenticity verification.
    Analyzes domain age, SSL, WHOIS, email, and company patterns.
    """
    if not data.company_name or len(data.company_name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please provide a valid company name (min 2 characters)")

    try:
        result = engine.analyze(
            company_name=data.company_name.strip(),
            website=data.website.strip() if data.website else None,
            email=data.email.strip() if data.email else None,
            source_platform=data.source_platform.strip() if data.source_platform else None,
        )
        return CompanyVerifyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
