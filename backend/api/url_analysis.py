"""
URL & Domain Analysis API
Analyzes URLs for phishing indicators, domain trust, and website authenticity
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import re
import socket
from datetime import datetime
from urllib.parse import urlparse

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class URLAnalysisRequest(BaseModel):
    url: str


class DomainTrustResponse(BaseModel):
    url: str
    domain: str
    is_https: bool
    domain_age_status: str
    trust_score: int
    risk_indicators: list
    trust_indicators: list
    verdict: str


# ─── Analysis Logic ────────────────────────────────────────────────────────────

class URLAnalyzer:
    """Domain and URL threat intelligence analyzer"""

    # Known legitimate job platforms
    TRUSTED_DOMAINS = [
        "linkedin.com", "indeed.com", "glassdoor.com", "naukri.com",
        "internshala.com", "monster.com", "shine.com", "foundit.in",
        "angel.co", "wellfound.com", "lever.co", "greenhouse.io",
        "workday.com", "careers.google.com", "amazon.jobs",
        "microsoft.com", "infosys.com", "tcs.com", "wipro.com"
    ]

    # Suspicious TLDs
    SUSPICIOUS_TLDS = [
        ".xyz", ".top", ".club", ".work", ".click", ".link",
        ".info", ".online", ".site", ".website", ".space",
        ".buzz", ".tk", ".ml", ".ga", ".cf"
    ]

    # Typosquatting patterns
    TYPOSQUAT_PATTERNS = [
        r"linkedln", r"linkdin", r"lnkedin", r"internshalla",
        r"naukkri", r"indeeed", r"glasdoor", r"amazom",
        r"gooogle", r"microsft", r"infossys"
    ]

    def analyze(self, url: str) -> dict:
        """Comprehensive URL analysis"""
        parsed = urlparse(url if url.startswith("http") else f"https://{url}")
        domain = parsed.netloc or parsed.path.split("/")[0]
        domain = domain.lower().replace("www.", "")

        risk_indicators = []
        trust_indicators = []
        trust_score = 50  # Start neutral

        # ─── HTTPS Check ──────────────────────────────────────────────────
        is_https = parsed.scheme == "https"
        if is_https:
            trust_score += 10
            trust_indicators.append("Uses HTTPS encryption")
        else:
            trust_score -= 15
            risk_indicators.append("No HTTPS - connection not encrypted")

        # ─── Trusted Domain Check ─────────────────────────────────────────
        is_trusted = any(trusted in domain for trusted in self.TRUSTED_DOMAINS)
        if is_trusted:
            trust_score += 30
            trust_indicators.append(f"Recognized legitimate job platform: {domain}")

        # ─── Suspicious TLD Check ─────────────────────────────────────────
        for tld in self.SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                trust_score -= 20
                risk_indicators.append(f"Uses suspicious TLD: {tld}")
                break

        # ─── Typosquatting Detection ──────────────────────────────────────
        for pattern in self.TYPOSQUAT_PATTERNS:
            if re.search(pattern, domain):
                trust_score -= 30
                risk_indicators.append(f"Possible typosquatting domain (mimics legitimate site)")
                break

        # ─── Domain Length Analysis ───────────────────────────────────────
        if len(domain) > 30:
            trust_score -= 10
            risk_indicators.append("Unusually long domain name")

        # ─── Subdomain Analysis ───────────────────────────────────────────
        subdomain_count = domain.count(".")
        if subdomain_count > 2:
            trust_score -= 10
            risk_indicators.append(f"Multiple subdomains detected ({subdomain_count} levels)")

        # ─── IP Address Check ─────────────────────────────────────────────
        if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
            trust_score -= 25
            risk_indicators.append("URL uses IP address instead of domain name")

        # ─── Free Hosting Detection ───────────────────────────────────────
        free_hosts = ["blogspot", "wordpress.com", "wix.com", "weebly",
                      "sites.google", "github.io", "netlify.app", "herokuapp"]
        for host in free_hosts:
            if host in domain:
                trust_score -= 10
                risk_indicators.append(f"Hosted on free platform: {host}")
                break

        # ─── Special Character Check ──────────────────────────────────────
        if re.search(r"[-]{2,}|[_]", domain):
            trust_score -= 5
            risk_indicators.append("Domain contains unusual characters")

        # ─── Number Heavy Domain ──────────────────────────────────────────
        digit_ratio = sum(c.isdigit() for c in domain) / max(len(domain), 1)
        if digit_ratio > 0.3:
            trust_score -= 10
            risk_indicators.append("Domain contains excessive numbers")

        # ─── DNS Resolution Check ─────────────────────────────────────────
        try:
            socket.gethostbyname(domain)
            trust_indicators.append("Domain resolves to valid IP")
            trust_score += 5
        except socket.gaierror:
            risk_indicators.append("Domain does not resolve - may not exist")
            trust_score -= 20

        # Clamp score
        trust_score = max(0, min(100, trust_score))

        # Determine verdict
        if trust_score >= 70:
            verdict = "Trusted"
        elif trust_score >= 50:
            verdict = "Moderate - Exercise Caution"
        elif trust_score >= 30:
            verdict = "Suspicious - High Caution Advised"
        else:
            verdict = "Dangerous - Likely Fraudulent"

        # Domain age status (simplified without WHOIS API)
        if is_trusted:
            domain_age_status = "Established (well-known platform)"
        else:
            domain_age_status = "Unknown - verify independently"

        return {
            "url": url,
            "domain": domain,
            "is_https": is_https,
            "domain_age_status": domain_age_status,
            "trust_score": trust_score,
            "risk_indicators": risk_indicators,
            "trust_indicators": trust_indicators,
            "verdict": verdict
        }


url_analyzer = URLAnalyzer()


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/analyze-url", response_model=DomainTrustResponse)
async def analyze_url(data: URLAnalysisRequest):
    """Analyze a URL for phishing and trust indicators"""
    if not data.url or len(data.url.strip()) < 4:
        raise HTTPException(status_code=400, detail="Please provide a valid URL")

    results = url_analyzer.analyze(data.url)
    return DomainTrustResponse(**results)
