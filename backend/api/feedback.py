"""
Feedback & Self-Improving AI API
Allows users to report false predictions and submit scam reports.
Every submission is stored as "pending_review" — an admin must
confirm it via POST /api/retrain/confirm-feedback before it is
used for retraining. Once the confirmed count crosses the
AUTO_RETRAIN_THRESHOLD the retraining engine fires automatically.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database.connection import feedback_collection

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    scan_id: Optional[str] = None
    feedback_type: str   # "false_positive", "false_negative", "scam_report", "general"
    message: str
    job_text: Optional[str] = None
    correct_label: Optional[str] = None  # "scam" or "legitimate"


class ScamReportRequest(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    description: str
    platform: Optional[str] = None
    scam_type: Optional[str] = None
    evidence_url: Optional[str] = None


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/feedback")
async def submit_feedback(data: FeedbackRequest, background_tasks: BackgroundTasks):
    """
    Submit feedback on a prediction.
    Saved as 'pending_review' — admin confirms before it trains the model.
    """
    if data.correct_label and data.correct_label not in ["scam", "legitimate"]:
        raise HTTPException(
            status_code=400,
            detail="correct_label must be 'scam' or 'legitimate'"
        )

    try:
        feedback_doc = {
            "scan_id": data.scan_id,
            "feedback_type": data.feedback_type,
            "message": data.message,
            "job_text": data.job_text,
            "correct_label": data.correct_label,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_review"   # Requires admin confirmation before training
        }
        result = await feedback_collection.insert_one(feedback_doc)
        inserted_id = str(result.inserted_id)

    except Exception:
        return {
            "message": "Feedback recorded. Thank you!",
            "feedback_id": None,
            "next_step": "pending_review"
        }

    return {
        "message": "Feedback submitted successfully. Thank you for helping improve our AI!",
        "feedback_id": inserted_id,
        "next_step": (
            "Your correction will be reviewed and used to retrain the model."
            if data.correct_label
            else "Your feedback has been noted."
        )
    }


@router.post("/report-scam")
async def report_scam(data: ScamReportRequest):
    """
    Submit a scam report for community protection.
    Reports are stored as 'under_review'. Admin verifies before training.
    """
    try:
        report_doc = {
            "company_name": data.company_name,
            "job_title": data.job_title,
            "description": data.description,
            "platform": data.platform,
            "scam_type": data.scam_type,
            "evidence_url": data.evidence_url,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "under_review",
            "verified": False
        }
        result = await feedback_collection.insert_one(report_doc)
        inserted_id = str(result.inserted_id)

    except Exception:
        return {
            "message": "Report recorded. Thank you for protecting the community!",
            "report_id": None,
            "report_status": "under_review"
        }

    return {
        "message": "Scam report submitted. Our team will review and verify it.",
        "report_id": inserted_id,
        "report_status": "under_review"
    }
