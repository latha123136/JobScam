"""
Real-Time Job Scraping API
Fetches live jobs from platforms and runs them through the AI scam detection engine
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from scraping.job_scraper import job_scraper
from ml.scam_detector import scam_engine
from datetime import datetime

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class ScrapeRequest(BaseModel):
    query: str = "work from home"
    platform: Optional[str] = "all"  # "all", "indeed", "internshala", "linkedin"
    max_results: Optional[int] = 5


class ScrapedJobResult(BaseModel):
    title: str
    company: str
    location: str
    salary: str
    platform: str
    url: str
    risk_score: int
    risk_level: str
    top_reasons: List[str]
    is_scam: bool


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/scrape-jobs")
async def scrape_and_analyze(data: ScrapeRequest):
    """
    Scrape live job postings from platforms and analyze each for scam indicators.
    
    Flow:
    1. Scrape jobs from selected platform(s)
    2. Run each job through the AI scam detection engine
    3. Return jobs with risk scores and explanations
    """
    if not data.query or len(data.query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please provide a search query")

    max_results = min(data.max_results or 5, 15)  # Cap at 15 to avoid overload

    # ─── Scrape based on platform selection ───────────────────────────────
    scraped_jobs = []

    if data.platform == "all":
        results = job_scraper.scrape_all_platforms(
            query=data.query, max_per_platform=max_results
        )
        for platform, jobs in results["platforms"].items():
            scraped_jobs.extend(jobs)
    elif data.platform == "indeed":
        scraped_jobs = job_scraper.scrape_indeed(
            query=data.query, max_jobs=max_results
        )
    elif data.platform == "internshala":
        scraped_jobs = job_scraper.scrape_internshala(
            query=data.query, max_jobs=max_results
        )
    elif data.platform == "linkedin":
        scraped_jobs = job_scraper.scrape_linkedin_public(
            query=data.query, max_jobs=max_results
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid platform. Use: all, indeed, internshala, linkedin")

    # ─── Analyze each scraped job ─────────────────────────────────────────
    analyzed_results = []
    errors = []

    for job in scraped_jobs:
        # Skip error entries
        if "error" in job:
            errors.append(job)
            continue

        # Get the text to analyze
        text_to_analyze = job.get("full_text", "") or job.get("description", "") or job.get("title", "")

        if len(text_to_analyze.strip()) < 10:
            continue

        # Run through AI engine
        analysis = scam_engine.analyze_text(text_to_analyze)

        analyzed_results.append({
            "title": job.get("title", "Unknown"),
            "company": job.get("company", "Unknown"),
            "location": job.get("location", "Unknown"),
            "salary": job.get("salary", "Not disclosed"),
            "platform": job.get("platform", "Unknown"),
            "url": job.get("url", ""),
            "description": job.get("description", "")[:200],
            "scraped_at": job.get("scraped_at", datetime.utcnow().isoformat()),
            "risk_score": analysis["risk_score"],
            "risk_level": analysis["risk_level"],
            "confidence": analysis["confidence"],
            "is_scam": analysis["risk_score"] > 60,
            "top_reasons": analysis["explanation"][:3],
            "red_flags": analysis["red_flags"][:3],
            "scam_phrases_found": analysis["scam_phrases_detected"][:3],
        })

    # ─── Sort by risk score (highest risk first) ──────────────────────────
    analyzed_results.sort(key=lambda x: x["risk_score"], reverse=True)

    # ─── Summary statistics ───────────────────────────────────────────────
    total_analyzed = len(analyzed_results)
    scams_found = len([j for j in analyzed_results if j["is_scam"]])
    safe_jobs = len([j for j in analyzed_results if j["risk_score"] <= 30])

    return {
        "query": data.query,
        "platform": data.platform,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total_scraped": len(scraped_jobs),
            "total_analyzed": total_analyzed,
            "scams_detected": scams_found,
            "safe_jobs": safe_jobs,
            "suspicious_jobs": total_analyzed - scams_found - safe_jobs,
            "scam_rate": round(scams_found / max(total_analyzed, 1) * 100, 1),
        },
        "jobs": analyzed_results,
        "errors": errors,
    }


@router.get("/scrape-jobs/platforms")
async def get_supported_platforms():
    """Get list of supported scraping platforms"""
    return {
        "platforms": [
            {
                "id": "indeed",
                "name": "Indeed India",
                "status": "active",
                "description": "Scrapes public job listings from Indeed India",
                "limitations": "May be rate-limited with heavy use"
            },
            {
                "id": "internshala",
                "name": "Internshala",
                "status": "active",
                "description": "Scrapes internship and job listings",
                "limitations": "Best for internship-related queries"
            },
            {
                "id": "linkedin",
                "name": "LinkedIn",
                "status": "limited",
                "description": "Scrapes public LinkedIn job search",
                "limitations": "Heavily restricted by LinkedIn. May return limited or no results."
            },
            {
                "id": "all",
                "name": "All Platforms",
                "status": "active",
                "description": "Scrapes from all supported platforms simultaneously",
                "limitations": "Takes longer due to multiple requests"
            }
        ]
    }
