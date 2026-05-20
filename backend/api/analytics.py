"""
Analytics Dashboard API
Provides aggregated statistics, trends, and fraud intelligence data
"""

from fastapi import APIRouter
from datetime import datetime, timedelta
from database.connection import predictions_collection, history_collection

router = APIRouter()


# ─── Mock Analytics Data (Replace with real DB queries in production) ──────────

MOCK_ANALYTICS = {
    "overview": {
        "total_scans": 15847,
        "scams_detected": 4231,
        "companies_verified": 892,
        "users_protected": 12450,
        "detection_accuracy": 96.7,
        "avg_risk_score": 42.3
    },
    "scam_trends": [
        {"month": "Jan", "scams": 320, "safe": 890},
        {"month": "Feb", "scams": 410, "safe": 920},
        {"month": "Mar", "scams": 380, "safe": 1050},
        {"month": "Apr", "scams": 520, "safe": 980},
        {"month": "May", "scams": 610, "safe": 1100},
        {"month": "Jun", "scams": 480, "safe": 1200},
        {"month": "Jul", "scams": 550, "safe": 1150},
        {"month": "Aug", "scams": 690, "safe": 1300},
        {"month": "Sep", "scams": 720, "safe": 1250},
        {"month": "Oct", "scams": 580, "safe": 1400},
        {"month": "Nov", "scams": 640, "safe": 1350},
        {"month": "Dec", "scams": 530, "safe": 1280}
    ],
    "risk_distribution": [
        {"level": "Safe", "count": 6420, "percentage": 40.5},
        {"level": "Low Risk", "count": 3180, "percentage": 20.1},
        {"level": "Medium Risk", "count": 2840, "percentage": 17.9},
        {"level": "High Risk", "count": 2150, "percentage": 13.6},
        {"level": "Critical Scam", "count": 1257, "percentage": 7.9}
    ],
    "top_scam_types": [
        {"type": "Registration Fee Scam", "count": 1240, "percentage": 29.3},
        {"type": "Fake BPO Jobs", "count": 890, "percentage": 21.0},
        {"type": "WhatsApp/Telegram Scams", "count": 720, "percentage": 17.0},
        {"type": "Fake Internship Certificates", "count": 580, "percentage": 13.7},
        {"type": "Phishing Emails", "count": 450, "percentage": 10.6},
        {"type": "Crypto/MLM Disguised Jobs", "count": 351, "percentage": 8.3}
    ],
    "platform_distribution": [
        {"platform": "LinkedIn", "scams": 890, "total": 4200},
        {"platform": "Internshala", "scams": 620, "total": 3100},
        {"platform": "Naukri", "scams": 450, "total": 2800},
        {"platform": "Indeed", "scams": 380, "total": 2200},
        {"platform": "Telegram", "scams": 1200, "total": 1800},
        {"platform": "WhatsApp", "scams": 691, "total": 1747}
    ],
    "recent_threats": [
        {
            "id": 1,
            "title": "Fake TCS Recruitment Drive",
            "severity": "Critical",
            "date": "2024-12-15",
            "description": "Mass WhatsApp campaign impersonating TCS HR"
        },
        {
            "id": 2,
            "title": "Internshala Certificate Scam",
            "severity": "High",
            "date": "2024-12-14",
            "description": "Fake internship certificates sold for ₹999"
        },
        {
            "id": 3,
            "title": "Amazon WFH Data Entry Scam",
            "severity": "High",
            "date": "2024-12-13",
            "description": "Fake Amazon work-from-home jobs requiring registration fee"
        },
        {
            "id": 4,
            "title": "Crypto Trading Job Scam",
            "severity": "Medium",
            "date": "2024-12-12",
            "description": "Jobs requiring crypto investment disguised as trading roles"
        },
        {
            "id": 5,
            "title": "Government Job Portal Phishing",
            "severity": "Critical",
            "date": "2024-12-11",
            "description": "Fake government job portals collecting personal data"
        }
    ]
}


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.get("/analytics/overview")
async def get_overview():
    """Get platform overview statistics"""
    return MOCK_ANALYTICS["overview"]


@router.get("/analytics/trends")
async def get_trends():
    """Get scam detection trends over time"""
    return {"trends": MOCK_ANALYTICS["scam_trends"]}


@router.get("/analytics/risk-distribution")
async def get_risk_distribution():
    """Get risk level distribution"""
    return {"distribution": MOCK_ANALYTICS["risk_distribution"]}


@router.get("/analytics/scam-types")
async def get_scam_types():
    """Get breakdown of scam types detected"""
    return {"scam_types": MOCK_ANALYTICS["top_scam_types"]}


@router.get("/analytics/platforms")
async def get_platform_stats():
    """Get scam statistics by platform"""
    return {"platforms": MOCK_ANALYTICS["platform_distribution"]}


@router.get("/analytics/threats")
async def get_recent_threats():
    """Get recent threat intelligence feed"""
    return {"threats": MOCK_ANALYTICS["recent_threats"]}


@router.get("/analytics/full")
async def get_full_analytics():
    """Get complete analytics dashboard data"""
    return MOCK_ANALYTICS
