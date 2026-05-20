"""
Company Authenticity Engine
Complete verification service with domain analysis, WHOIS lookup,
existence duration estimation, and explainable risk scoring.
"""

import re
import socket
import ssl
import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class CompanyAuthenticityEngine:
    """Enterprise-grade company verification with multi-signal analysis"""

    # Verified company database (expandable)
    KNOWN_COMPANIES = {
        "tcs": {"full_name": "Tata Consultancy Services", "domain": "tcs.com", "founded": 1968},
        "infosys": {"full_name": "Infosys Limited", "domain": "infosys.com", "founded": 1981},
        "wipro": {"full_name": "Wipro Limited", "domain": "wipro.com", "founded": 1945},
        "hcl": {"full_name": "HCL Technologies", "domain": "hcltech.com", "founded": 1976},
        "google": {"full_name": "Google LLC", "domain": "google.com", "founded": 1998},
        "microsoft": {"full_name": "Microsoft Corporation", "domain": "microsoft.com", "founded": 1975},
        "amazon": {"full_name": "Amazon.com Inc", "domain": "amazon.com", "founded": 1994},
        "flipkart": {"full_name": "Flipkart Internet Pvt Ltd", "domain": "flipkart.com", "founded": 2007},
        "accenture": {"full_name": "Accenture plc", "domain": "accenture.com", "founded": 1989},
        "deloitte": {"full_name": "Deloitte Touche Tohmatsu", "domain": "deloitte.com", "founded": 1845},
        "cognizant": {"full_name": "Cognizant Technology Solutions", "domain": "cognizant.com", "founded": 1994},
        "reliance": {"full_name": "Reliance Industries Limited", "domain": "ril.com", "founded": 1966},
        "paytm": {"full_name": "One97 Communications Ltd", "domain": "paytm.com", "founded": 2010},
        "zomato": {"full_name": "Zomato Limited", "domain": "zomato.com", "founded": 2008},
        "meta": {"full_name": "Meta Platforms Inc", "domain": "meta.com", "founded": 2004},
        "apple": {"full_name": "Apple Inc", "domain": "apple.com", "founded": 1976},
        "netflix": {"full_name": "Netflix Inc", "domain": "netflix.com", "founded": 1997},
        "uber": {"full_name": "Uber Technologies Inc", "domain": "uber.com", "founded": 2009},
        "swiggy": {"full_name": "Swiggy (Bundl Technologies)", "domain": "swiggy.com", "founded": 2014},
        "byju": {"full_name": "BYJU'S (Think & Learn)", "domain": "byjus.com", "founded": 2011},
        "ola": {"full_name": "ANI Technologies Pvt Ltd", "domain": "olacabs.com", "founded": 2010},
        "razorpay": {"full_name": "Razorpay Software Pvt Ltd", "domain": "razorpay.com", "founded": 2014},
        "zoho": {"full_name": "Zoho Corporation", "domain": "zoho.com", "founded": 1996},
        "freshworks": {"full_name": "Freshworks Inc", "domain": "freshworks.com", "founded": 2010},
        "tech mahindra": {"full_name": "Tech Mahindra Limited", "domain": "techmahindra.com", "founded": 1986},
    }

    SUSPICIOUS_TLDS = [".xyz", ".top", ".click", ".buzz", ".tk", ".ml", ".ga", ".cf", ".gq", ".work", ".loan"]
    FREE_EMAIL_PROVIDERS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "rediffmail.com", "ymail.com", "aol.com", "protonmail.com"]

    def analyze(self, company_name: str, website: Optional[str] = None,
                email: Optional[str] = None, source_platform: Optional[str] = None) -> Dict:
        """Run complete company authenticity analysis"""

        result = {
            "company_name": company_name,
            "company_existence_years": None,
            "company_founded_year": None,
            "domain_existence_years": None,
            "domain_creation_date": None,
            "legitimacy_score": 50,
            "scam_probability": 50,
            "trust_level": "Unknown",
            "verification_status": "Pending",
            "linkedin_presence": "Not Checked",
            "email_authenticity": "Not Checked",
            "website_security": "Not Checked",
            "domain_registrar": None,
            "ssl_valid": None,
            "dns_resolves": None,
            "risk_flags": [],
            "trust_signals": [],
            "checks_performed": [],
            "analysis_summary": "",
            "recommendation": "",
        }

        score = 50  # Start neutral

        # 1. Known Company Database Check
        score = self._check_known_company(company_name, website, result, score)

        # 2. Domain / WHOIS Analysis
        if website:
            score = self._analyze_domain(website, result, score)

        # 3. SSL / Website Security
        if website:
            score = self._check_website_security(website, result, score)

        # 4. Email Verification
        if email:
            score = self._verify_email(email, website, result, score)

        # 5. Company Name Pattern Analysis
        score = self._analyze_company_name(company_name, result, score)

        # 6. Source Platform Analysis
        if source_platform:
            score = self._analyze_source_platform(source_platform, result, score)

        # 7. Consistency Checks
        score = self._check_consistency(result, score)

        # Final scoring
        score = max(0, min(100, score))
        result["legitimacy_score"] = score
        result["scam_probability"] = 100 - score

        # Trust level
        if score >= 75:
            result["trust_level"] = "Safe"
            result["verification_status"] = "Verified - Trusted"
            result["recommendation"] = "This company appears legitimate based on multiple verification signals. Proceed with standard caution."
        elif score >= 50:
            result["trust_level"] = "Moderate"
            result["verification_status"] = "Partially Verified - Exercise Caution"
            result["recommendation"] = "Some verification signals are positive but not all checks passed. Verify through official channels before sharing personal information."
        elif score >= 30:
            result["trust_level"] = "Suspicious"
            result["verification_status"] = "Unverified - Suspicious"
            result["recommendation"] = "Multiple risk indicators detected. Do not share personal details or make payments without thorough independent verification."
        else:
            result["trust_level"] = "High Risk"
            result["verification_status"] = "Failed Verification - Likely Fraudulent"
            result["recommendation"] = "High probability of fraud. Do NOT share personal information, bank details, or make any payments. Report this company."

        # Generate summary
        result["analysis_summary"] = self._generate_summary(result)

        return result

    # ─── Private Analysis Methods ──────────────────────────────────────────

    def _check_known_company(self, company_name: str, website: Optional[str], result: Dict, score: int) -> int:
        """Check against known company database"""
        company_lower = company_name.lower().strip()
        known_match = None

        for key, data in self.KNOWN_COMPANIES.items():
            if key in company_lower or company_lower in data["full_name"].lower():
                known_match = data
                break

        if known_match:
            score += 20
            result["company_founded_year"] = known_match["founded"]
            current_year = datetime.datetime.now().year
            result["company_existence_years"] = current_year - known_match["founded"]
            result["trust_signals"].append(f"Recognized company: {known_match['full_name']}")
            result["linkedin_presence"] = "Verified (Known Company)"
            result["checks_performed"].append({
                "check": "Company Database",
                "status": "verified",
                "detail": f"Found in verified database as {known_match['full_name']} (Founded: {known_match['founded']})"
            })

            # Verify website matches known domain
            if website:
                parsed = urlparse(website if website.startswith("http") else f"https://{website}")
                domain = (parsed.netloc or parsed.path).replace("www.", "").lower().split("/")[0]
                if known_match["domain"] in domain or domain in known_match["domain"]:
                    score += 15
                    result["trust_signals"].append("Website matches verified company domain")
                    result["checks_performed"].append({
                        "check": "Domain Match",
                        "status": "verified",
                        "detail": f"Website {domain} matches known domain {known_match['domain']}"
                    })
                else:
                    score -= 20
                    result["risk_flags"].append(f"Website doesn't match known domain ({known_match['domain']})")
                    result["checks_performed"].append({
                        "check": "Domain Match",
                        "status": "failed",
                        "detail": f"Expected {known_match['domain']}, got {domain}"
                    })
        else:
            result["checks_performed"].append({
                "check": "Company Database",
                "status": "not_found",
                "detail": "Company not in verified database (doesn't necessarily indicate fraud)"
            })

        return score

    def _analyze_domain(self, website: str, result: Dict, score: int) -> int:
        """Analyze domain age, WHOIS data, and DNS"""
        parsed = urlparse(website if website.startswith("http") else f"https://{website}")
        domain = (parsed.netloc or parsed.path).replace("www.", "").lower().split("/")[0]

        # DNS Resolution
        try:
            ip = socket.gethostbyname(domain)
            score += 5
            result["dns_resolves"] = True
            result["trust_signals"].append("Domain resolves to valid IP")
            result["checks_performed"].append({
                "check": "DNS Resolution",
                "status": "verified",
                "detail": f"Domain {domain} resolves to {ip}"
            })
        except socket.gaierror:
            score -= 15
            result["dns_resolves"] = False
            result["risk_flags"].append("Domain does not resolve - website may not exist")
            result["checks_performed"].append({
                "check": "DNS Resolution",
                "status": "failed",
                "detail": f"Domain {domain} could not be resolved"
            })
            return score  # No point checking further if domain doesn't resolve

        # WHOIS Lookup
        if WHOIS_AVAILABLE:
            try:
                w = whois.whois(domain)
                creation_date = w.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]

                if creation_date:
                    now = datetime.datetime.now()
                    if isinstance(creation_date, datetime.datetime):
                        domain_age_days = (now - creation_date).days
                    else:
                        creation_dt = datetime.datetime.combine(creation_date, datetime.time())
                        domain_age_days = (now - creation_dt).days

                    domain_age_years = round(domain_age_days / 365.25, 1)
                    result["domain_existence_years"] = domain_age_years
                    result["domain_creation_date"] = creation_date.strftime("%Y-%m-%d") if hasattr(creation_date, 'strftime') else str(creation_date)

                    if domain_age_years >= 5:
                        score += 15
                        result["trust_signals"].append(f"Domain is {domain_age_years} years old (established)")
                    elif domain_age_years >= 2:
                        score += 8
                        result["trust_signals"].append(f"Domain is {domain_age_years} years old")
                    elif domain_age_years >= 1:
                        score += 3
                        result["trust_signals"].append(f"Domain is {domain_age_years} years old (relatively new)")
                    else:
                        score -= 15
                        result["risk_flags"].append(f"Domain is only {domain_age_years} years old (very new)")

                    # Check consistency with company age
                    if result["company_existence_years"] and domain_age_years < 1 and result["company_existence_years"] > 10:
                        score -= 15
                        result["risk_flags"].append("Company claims to be old but domain was recently created")

                    result["checks_performed"].append({
                        "check": "Domain Age (WHOIS)",
                        "status": "verified",
                        "detail": f"Domain created on {result['domain_creation_date']} ({domain_age_years} years ago)"
                    })

                # Registrar info
                registrar = w.registrar
                if registrar:
                    result["domain_registrar"] = registrar
                    result["checks_performed"].append({
                        "check": "Domain Registrar",
                        "status": "info",
                        "detail": f"Registered with: {registrar}"
                    })

            except Exception as e:
                result["checks_performed"].append({
                    "check": "Domain Age (WHOIS)",
                    "status": "unavailable",
                    "detail": f"WHOIS lookup failed: {str(e)[:80]}"
                })

        # Suspicious TLD check
        if any(domain.endswith(tld) for tld in self.SUSPICIOUS_TLDS):
            score -= 15
            result["risk_flags"].append(f"Website uses suspicious top-level domain")
            result["checks_performed"].append({
                "check": "TLD Analysis",
                "status": "warning",
                "detail": f"Domain uses a TLD commonly associated with spam/scam sites"
            })
        else:
            result["checks_performed"].append({
                "check": "TLD Analysis",
                "status": "verified",
                "detail": "Domain uses a standard top-level domain"
            })

        return score

    def _check_website_security(self, website: str, result: Dict, score: int) -> int:
        """Check SSL certificate and HTTPS"""
        parsed = urlparse(website if website.startswith("http") else f"https://{website}")
        domain = (parsed.netloc or parsed.path).replace("www.", "").lower().split("/")[0]

        # SSL Certificate Check
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        score += 10
                        result["ssl_valid"] = True
                        result["website_security"] = "HTTPS with valid SSL"
                        result["trust_signals"].append("Valid SSL certificate detected")

                        # Check cert expiry
                        not_after = cert.get("notAfter", "")
                        if not_after:
                            expiry = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                            if expiry > datetime.datetime.now():
                                result["checks_performed"].append({
                                    "check": "SSL Certificate",
                                    "status": "verified",
                                    "detail": f"Valid SSL certificate (expires: {expiry.strftime('%Y-%m-%d')})"
                                })
                            else:
                                score -= 10
                                result["ssl_valid"] = False
                                result["website_security"] = "SSL certificate expired"
                                result["risk_flags"].append("SSL certificate has expired")
                                result["checks_performed"].append({
                                    "check": "SSL Certificate",
                                    "status": "failed",
                                    "detail": "SSL certificate has expired"
                                })
        except (socket.timeout, socket.gaierror, ssl.SSLError, ConnectionRefusedError, OSError):
            result["ssl_valid"] = False
            result["website_security"] = "SSL check failed or no HTTPS"
            result["checks_performed"].append({
                "check": "SSL Certificate",
                "status": "warning",
                "detail": "Could not verify SSL certificate (site may not support HTTPS)"
            })

        # HTTP response check
        if REQUESTS_AVAILABLE and result.get("dns_resolves"):
            try:
                url = website if website.startswith("http") else f"https://{website}"
                resp = requests.head(url, timeout=5, allow_redirects=True)
                if resp.status_code < 400:
                    score += 5
                    result["trust_signals"].append("Website is accessible and responding")
                    result["checks_performed"].append({
                        "check": "Website Accessibility",
                        "status": "verified",
                        "detail": f"Website responded with status {resp.status_code}"
                    })
                else:
                    result["risk_flags"].append(f"Website returned error status {resp.status_code}")
                    result["checks_performed"].append({
                        "check": "Website Accessibility",
                        "status": "warning",
                        "detail": f"Website returned HTTP {resp.status_code}"
                    })
            except Exception:
                result["checks_performed"].append({
                    "check": "Website Accessibility",
                    "status": "unavailable",
                    "detail": "Could not connect to website"
                })

        return score

    def _verify_email(self, email: str, website: Optional[str], result: Dict, score: int) -> int:
        """Verify recruiter email authenticity"""
        if "@" not in email:
            result["email_authenticity"] = "Invalid Format"
            result["risk_flags"].append("Invalid email format provided")
            score -= 10
            return score

        email_domain = email.split("@")[-1].lower()

        # Free email provider check
        if email_domain in self.FREE_EMAIL_PROVIDERS:
            score -= 15
            result["email_authenticity"] = f"Free Provider ({email_domain})"
            result["risk_flags"].append(f"Recruiter uses free email provider ({email_domain}) - legitimate companies use corporate email")
            result["checks_performed"].append({
                "check": "Email Domain",
                "status": "warning",
                "detail": f"Uses free email provider: {email_domain}"
            })
        elif website:
            # Check if email domain matches website
            parsed = urlparse(website if website.startswith("http") else f"https://{website}")
            web_domain = (parsed.netloc or parsed.path).replace("www.", "").lower().split("/")[0]

            if email_domain == web_domain or web_domain.endswith(email_domain) or email_domain.endswith(web_domain):
                score += 10
                result["email_authenticity"] = "Matches Company Domain"
                result["trust_signals"].append("Recruiter email domain matches company website")
                result["checks_performed"].append({
                    "check": "Email-Website Match",
                    "status": "verified",
                    "detail": f"Email domain ({email_domain}) matches website domain"
                })
            else:
                score -= 10
                result["email_authenticity"] = "Domain Mismatch"
                result["risk_flags"].append(f"Email domain ({email_domain}) doesn't match website domain ({web_domain})")
                result["checks_performed"].append({
                    "check": "Email-Website Match",
                    "status": "failed",
                    "detail": f"Email domain ({email_domain}) doesn't match website ({web_domain})"
                })
        else:
            result["email_authenticity"] = f"Corporate Domain ({email_domain})"
            result["trust_signals"].append("Uses corporate email domain")
            score += 5
            result["checks_performed"].append({
                "check": "Email Domain",
                "status": "verified",
                "detail": f"Uses corporate email: {email_domain}"
            })

        return score

    def _analyze_company_name(self, company_name: str, result: Dict, score: int) -> int:
        """Analyze company name for suspicious patterns"""
        # Excessive numbers
        if re.search(r"\d{4,}", company_name):
            score -= 5
            result["risk_flags"].append("Company name contains excessive numbers")

        # Very short name
        if len(company_name.strip()) < 3:
            score -= 10
            result["risk_flags"].append("Company name is suspiciously short")

        # All caps (shouting)
        if company_name == company_name.upper() and len(company_name) > 5:
            score -= 3
            result["risk_flags"].append("Company name is in ALL CAPS (unprofessional)")

        # Suspicious keywords in name
        scam_keywords = ["earn", "income", "money", "cash", "rich", "millionaire", "crypto", "forex"]
        name_lower = company_name.lower()
        for keyword in scam_keywords:
            if keyword in name_lower:
                score -= 10
                result["risk_flags"].append(f"Company name contains suspicious keyword: '{keyword}'")
                break

        # Generic/vague names
        generic_patterns = [r"^(the\s+)?company$", r"^(the\s+)?group$", r"^(the\s+)?firm$"]
        for pattern in generic_patterns:
            if re.match(pattern, name_lower):
                score -= 5
                result["risk_flags"].append("Company name is extremely generic")
                break

        result["checks_performed"].append({
            "check": "Company Name Analysis",
            "status": "verified" if not any("name" in f.lower() for f in result["risk_flags"]) else "warning",
            "detail": "Company name pattern analysis completed"
        })

        return score

    def _analyze_source_platform(self, source_platform: str, result: Dict, score: int) -> int:
        """Analyze the job source platform credibility"""
        trusted_platforms = ["linkedin", "naukri", "indeed", "glassdoor", "monster", "internshala", "angel.co", "wellfound"]
        suspicious_platforms = ["telegram", "whatsapp", "facebook group", "olx", "quikr"]

        platform_lower = source_platform.lower()

        if any(p in platform_lower for p in trusted_platforms):
            score += 5
            result["trust_signals"].append(f"Job posted on trusted platform ({source_platform})")
            result["checks_performed"].append({
                "check": "Source Platform",
                "status": "verified",
                "detail": f"Posted on recognized job platform: {source_platform}"
            })
        elif any(p in platform_lower for p in suspicious_platforms):
            score -= 10
            result["risk_flags"].append(f"Job posted on suspicious platform ({source_platform})")
            result["checks_performed"].append({
                "check": "Source Platform",
                "status": "warning",
                "detail": f"Posted on non-standard platform: {source_platform}"
            })
        else:
            result["checks_performed"].append({
                "check": "Source Platform",
                "status": "info",
                "detail": f"Source platform: {source_platform}"
            })

        return score

    def _check_consistency(self, result: Dict, score: int) -> int:
        """Cross-check consistency between different signals"""
        # Company age vs domain age inconsistency
        if result["company_existence_years"] and result["domain_existence_years"]:
            company_years = result["company_existence_years"]
            domain_years = result["domain_existence_years"]

            if company_years > 20 and domain_years < 2:
                score -= 10
                result["risk_flags"].append(
                    f"Inconsistency: Company claims {company_years} years but domain is only {domain_years} years old"
                )

        # Multiple risk flags compound penalty
        risk_count = len(result["risk_flags"])
        if risk_count >= 4:
            score -= 10
            result["risk_flags"].append("Multiple risk indicators detected (compounding risk)")

        return score

    def _generate_summary(self, result: Dict) -> str:
        """Generate human-readable analysis summary"""
        parts = []

        if result["company_existence_years"]:
            parts.append(f"Company has existed for approximately {result['company_existence_years']} years.")

        if result["domain_existence_years"]:
            parts.append(f"Domain has been active for {result['domain_existence_years']} years.")

        if result["trust_signals"]:
            parts.append(f"Positive signals: {', '.join(result['trust_signals'][:3])}.")

        if result["risk_flags"]:
            parts.append(f"Risk indicators: {', '.join(result['risk_flags'][:3])}.")

        parts.append(f"Overall trust level: {result['trust_level']} (Score: {result['legitimacy_score']}/100).")

        return " ".join(parts)
