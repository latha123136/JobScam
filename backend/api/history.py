"""
Scan History API
Track and retrieve user scan history
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database.connection import history_collection

router = APIRouter()


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.get("/history")
async def get_history(limit: int = 20, skip: int = 0):
    """Get scan history with pagination"""
    try:
        cursor = history_collection.find().sort("timestamp", -1).skip(skip).limit(limit)
        history = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            history.append(doc)
        return {"history": history, "count": len(history)}
    except Exception as e:
        return {"history": [], "count": 0}


@router.get("/history/stats")
async def get_stats():
    """Get overall scanning statistics"""
    try:
        total_scans = await history_collection.count_documents({})
        scams_detected = await history_collection.count_documents({"risk_level": {"$in": ["High Risk", "Critical Scam"]}})
        safe_jobs = await history_collection.count_documents({"risk_level": {"$in": ["Safe", "Low Risk"]}})

        return {
            "total_scans": total_scans,
            "scams_detected": scams_detected,
            "safe_jobs": safe_jobs,
            "detection_rate": round(scams_detected / max(total_scans, 1) * 100, 1)
        }
    except Exception:
        return {
            "total_scans": 0,
            "scams_detected": 0,
            "safe_jobs": 0,
            "detection_rate": 0
        }
