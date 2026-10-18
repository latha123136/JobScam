"""
Model Retraining API
====================
Endpoints to manually trigger retraining, check live status,
view retraining history, and confirm/reject feedback samples.

Endpoints:
  POST /api/retrain/trigger          — Manually kick off a retrain
  GET  /api/retrain/status           — Current training status + last result
  GET  /api/retrain/history          — All past retraining logs
  GET  /api/retrain/feedback-queue   — Pending feedback waiting for confirmation
  POST /api/retrain/confirm-feedback — Admin confirms a feedback sample
  POST /api/retrain/reject-feedback  — Admin rejects a feedback sample
  GET  /api/retrain/stats            — Quick stats (pending/confirmed counts)
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database.connection import feedback_collection, DB_AVAILABLE
from ml.retraining_engine import retraining_engine

router = APIRouter()


# ─── Lazy import for retraining_logs_collection ──────────────────────────────
# We add this collection dynamically here to avoid circular imports
# and to keep the connection module minimal.

def _get_retraining_logs_collection():
    """Get or create the retraining_logs collection."""
    from database.connection import database, DB_AVAILABLE, MockCollection
    if DB_AVAILABLE and database is not None:
        return database["retraining_logs"]
    return MockCollection()


# ─── Schemas ──────────────────────────────────────────────────────────────────

class ConfirmFeedbackRequest(BaseModel):
    feedback_id: str
    confirmed_label: str   # "scam" or "legitimate"


class RejectFeedbackRequest(BaseModel):
    feedback_id: str
    reason: Optional[str] = None


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.post("/retrain/trigger")
async def trigger_retrain(background_tasks: BackgroundTasks):
    """
    Manually trigger a model retraining cycle.
    Runs in the background — returns immediately with a job ID.
    Poll /api/retrain/status to track progress.
    """
    if retraining_engine.is_training:
        return {
            "status": "already_running",
            "message": "A retraining job is already in progress. Check /api/retrain/status for updates."
        }

    retraining_logs_collection = _get_retraining_logs_collection()

    # Schedule retraining as a background task so this endpoint returns fast
    background_tasks.add_task(
        retraining_engine.run_retraining,
        feedback_collection,
        retraining_logs_collection,
        "manual"
    )

    return {
        "status": "started",
        "message": "Retraining started in the background. The live model will be updated automatically when complete.",
        "check_status_at": "/api/retrain/status"
    }


@router.get("/retrain/status")
async def get_retrain_status():
    """
    Get current retraining status and the result of the last completed run.
    """
    from ml.scam_detector import scam_engine

    return {
        "is_training_now": retraining_engine.is_training,
        "model_loaded": scam_engine.model_loaded,
        "last_retrain_time": (
            retraining_engine.last_retrain_time.isoformat()
            if retraining_engine.last_retrain_time else None
        ),
        "last_retrain_result": retraining_engine.last_retrain_result,
        "feedback_count_at_last_retrain": retraining_engine.feedback_count_at_last_retrain,
        "auto_retrain_threshold": retraining_engine.AUTO_RETRAIN_THRESHOLD
        if hasattr(retraining_engine, "AUTO_RETRAIN_THRESHOLD") else 50
    }


@router.get("/retrain/history")
async def get_retrain_history(limit: int = 20):
    """
    Return the last N retraining run logs from MongoDB.
    Each log contains timing, sample counts, model metrics, and status.
    """
    retraining_logs_collection = _get_retraining_logs_collection()
    history = []
    try:
        cursor = retraining_logs_collection.find().sort("started_at", -1).limit(limit)
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            history.append(doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch history: {str(e)}")

    return {"history": history, "count": len(history)}


@router.get("/retrain/feedback-queue")
async def get_feedback_queue(limit: int = 50, status: str = "pending_review"):
    """
    Return feedback samples waiting for admin confirmation.
    status: "pending_review" | "confirmed" | "rejected"
    """
    queue = []
    try:
        cursor = feedback_collection.find(
            {"status": status,
             "job_text": {"$exists": True, "$ne": None}}
        ).sort("timestamp", -1).limit(limit)

        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            # Truncate long texts for the response
            if doc.get("job_text"):
                doc["job_text_preview"] = doc["job_text"][:300] + (
                    "..." if len(doc["job_text"]) > 300 else ""
                )
            queue.append(doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch queue: {str(e)}")

    return {"queue": queue, "count": len(queue), "status_filter": status}


@router.post("/retrain/confirm-feedback")
async def confirm_feedback(data: ConfirmFeedbackRequest, background_tasks: BackgroundTasks):
    """
    Admin confirms a feedback sample with the correct label.
    Updates status to 'confirmed' so it will be included in the next retrain.
    Automatically triggers retraining if the confirmed count crosses the threshold.
    """
    from bson import ObjectId

    if data.confirmed_label not in ["scam", "legitimate"]:
        raise HTTPException(
            status_code=400,
            detail="confirmed_label must be 'scam' or 'legitimate'"
        )

    try:
        result = await feedback_collection.update_one(
            {"_id": ObjectId(data.feedback_id)},
            {"$set": {
                "status": "confirmed",
                "correct_label": data.confirmed_label,
                "confirmed_at": datetime.utcnow().isoformat()
            }}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Feedback entry not found")

    except Exception as e:
        if "404" in str(e):
            raise
        raise HTTPException(status_code=400, detail=f"Invalid feedback ID: {str(e)}")

    # Check if auto-retrain threshold is now met
    retraining_logs_collection = _get_retraining_logs_collection()
    background_tasks.add_task(
        retraining_engine.check_and_auto_retrain,
        feedback_collection,
        retraining_logs_collection
    )

    return {
        "status": "confirmed",
        "feedback_id": data.feedback_id,
        "correct_label": data.confirmed_label,
        "message": "Feedback confirmed. Will be included in next retraining cycle."
    }


@router.post("/retrain/reject-feedback")
async def reject_feedback(data: RejectFeedbackRequest):
    """
    Admin rejects a feedback sample — it will never be used for training.
    """
    from bson import ObjectId

    try:
        result = await feedback_collection.update_one(
            {"_id": ObjectId(data.feedback_id)},
            {"$set": {
                "status": "rejected",
                "rejection_reason": data.reason or "Rejected by admin",
                "rejected_at": datetime.utcnow().isoformat()
            }}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Feedback entry not found")

    except Exception as e:
        if "404" in str(e):
            raise
        raise HTTPException(status_code=400, detail=f"Invalid feedback ID: {str(e)}")

    return {
        "status": "rejected",
        "feedback_id": data.feedback_id,
        "message": "Feedback rejected and excluded from training data."
    }


@router.get("/retrain/stats")
async def get_retrain_stats():
    """
    Quick overview of feedback queue health and retraining readiness.
    """
    retraining_logs_collection = _get_retraining_logs_collection()

    try:
        pending = await feedback_collection.count_documents({"status": "pending_review"})
        confirmed = await feedback_collection.count_documents({
            "status": "confirmed",
            "job_text": {"$exists": True, "$ne": None},
            "correct_label": {"$in": ["scam", "legitimate"]}
        })
        rejected = await feedback_collection.count_documents({"status": "rejected"})
        total_retrains = await retraining_logs_collection.count_documents({"status": "success"})
        failed_retrains = await retraining_logs_collection.count_documents({"status": "failed"})

        new_since_last = confirmed - retraining_engine.feedback_count_at_last_retrain
        from ml.retraining_engine import AUTO_RETRAIN_THRESHOLD
        threshold = AUTO_RETRAIN_THRESHOLD

    except Exception:
        pending = confirmed = rejected = total_retrains = failed_retrains = 0
        new_since_last = 0
        threshold = 50

    return {
        "feedback_queue": {
            "pending_review": pending,
            "confirmed": confirmed,
            "rejected": rejected
        },
        "auto_retrain": {
            "threshold": threshold,
            "new_confirmed_since_last_retrain": new_since_last,
            "samples_until_next_retrain": max(0, threshold - new_since_last),
            "will_trigger_soon": new_since_last >= threshold
        },
        "retraining_history": {
            "total_successful_retrains": total_retrains,
            "total_failed_retrains": failed_retrains,
            "last_retrain": (
                retraining_engine.last_retrain_time.isoformat()
                if retraining_engine.last_retrain_time else "Never"
            )
        },
        "model_status": {
            "is_training_now": retraining_engine.is_training,
        }
    }
