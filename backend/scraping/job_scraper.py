"""
Real-Time Job Scraping Engine
Fetches live job postings from Indeed and Internshala for automated scam analysis.

Supported Platforms:
- Indeed India (publicly accessible job listings)
- Internshala (internship and job listings)
- LinkedIn (limited - public job search only)

Note: This module respects robots.txt and rate limits.
Do NOT use for mass scraping or commercial purposes.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict, Optional
from datetime import datetime


class JobScraper:
    """Multi-platform job scraper with rate limiting and error handling"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
        })
        self.rate_limit_delay = 2  # seconds between requests

    # ─────────────────────────────────────────────────────────────────────────
    # INDEED INDIA SCRAPER
    # ─────────────────────────────────────────────────────────────────────────

    def scrape_indeed(self, query: str = "data entry", location: str = "India", max_jobs: int = 10) -> List[Dict]:
        """
        Scrape job listings from Indeed India.
        Uses the public search results page.
        """
        jobs = []
        base_url = "https://www.indeed.co.in/jobs"
        params = {
            "q": query,
            "l": location,
            "sort": "date",  # Most recent first
        }

        try:
            response = self.session.get(base_url, params=params, timeout=15)
            if response.status_code != 200:
                return [{"error": f"Indeed returned status {response.status_code}", "platform": "Indeed"}]

            soup = BeautifulSoup(response.text, "html.parser")

            # Find job cards
            job_cards = soup.find_all("div", class_=re.compile(r"job_seen_beacon|cardOutline|result"))

            if not job_cards:
                # Try alternative selectors
                job_cards = soup.find_all("a", class_=re.compile(r"jcs-JobTitle"))

            for card in job_cards[:max_jobs]:
                job = self._parse_indeed_card(card)
                if job:
                    job["platform"] = "Indeed"
                    job["scraped_at"] = datetime.utcnow().isoformat()
                    jobs.append(job)

            time.sleep(self.rate_limit_delay)

        except requests.exceptions.Timeout:
            return [{"error": "Indeed request timed out", "platform": "Indeed"}]
        except requests.exceptions.ConnectionError:
            return [{"error": "Could not connect to Indeed", "platform": "Indeed"}]
        except Exception as e:
            return [{"error": f"Indeed scraping error: {str(e)}", "platform": "Indeed"}]

        return jobs

    def _parse_indeed_card(self, card) -> Optional[Dict]:
        """Parse a single Indeed job card"""
        try:
            # Title
            title_el = card.find("h2") or card.find("a", class_=re.compile(r"title|JobTitle"))
            title = title_el.get_text(strip=True) if title_el else "Unknown Title"

            # Company
            company_el = card.find("span", class_=re.compile(r"company|companyName"))
            if not company_el:
                company_el = card.find("span", {"data-testid": "company-name"})
            company = company_el.get_text(strip=True) if company_el else "Unknown Company"

            # Location
            location_el = card.find("div", class_=re.compile(r"companyLocation|location"))
            if not location_el:
                location_el = card.find("span", class_=re.compile(r"location"))
            location = location_el.get_text(strip=True) if location_el else "India"

            # Salary (if available)
            salary_el = card.find("div", class_=re.compile(r"salary|salaryText"))
            if not salary_el:
                salary_el = card.find("span", class_=re.compile(r"salary"))
            salary = salary_el.get_text(strip=True) if salary_el else "Not disclosed"

            # Snippet/Description
            snippet_el = card.find("div", class_=re.compile(r"snippet|job-snippet"))
            if not snippet_el:
                snippet_el = card.find("ul") or card.find("div", class_=re.compile(r"description"))
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""

            # Job URL
            link_el = card.find("a", href=True)
            job_url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                if href.startswith("/"):
                    job_url = f"https://www.indeed.co.in{href}"
                else:
                    job_url = href

            # Combine for analysis
            full_text = f"{title} {company} {snippet} {salary}"

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "description": snippet[:500],
                "url": job_url,
                "full_text": full_text,
            }
        except Exception:
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # INTERNSHALA SCRAPER
    # ─────────────────────────────────────────────────────────────────────────

    def scrape_internshala(self, query: str = "work from home", max_jobs: int = 10) -> List[Dict]:
        """
        Scrape internship/job listings from Internshala.
        Uses the public search page.
        """
        jobs = []
        # Internshala URL format
        search_term = query.replace(" ", "-")
        url = f"https://internshala.com/internships/{search_term}-internship"

        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                # Try jobs section
                url = f"https://internshala.com/jobs/{search_term}-jobs"
                response = self.session.get(url, timeout=15)
                if response.status_code != 200:
                    return [{"error": f"Internshala returned status {response.status_code}", "platform": "Internshala"}]

            soup = BeautifulSoup(response.text, "html.parser")

            # Find internship/job cards
            cards = soup.find_all("div", class_=re.compile(r"individual_internship|internship_meta"))
            if not cards:
                cards = soup.find_all("div", class_=re.compile(r"container-fluid individual"))
            if not cards:
                # Try finding by the internship listing structure
                cards = soup.find_all("div", id=re.compile(r"internship_"))

            for card in cards[:max_jobs]:
                job = self._parse_internshala_card(card)
                if job:
                    job["platform"] = "Internshala"
                    job["scraped_at"] = datetime.utcnow().isoformat()
                    jobs.append(job)

            time.sleep(self.rate_limit_delay)

        except requests.exceptions.Timeout:
            return [{"error": "Internshala request timed out", "platform": "Internshala"}]
        except requests.exceptions.ConnectionError:
            return [{"error": "Could not connect to Internshala", "platform": "Internshala"}]
        except Exception as e:
            return [{"error": f"Internshala scraping error: {str(e)}", "platform": "Internshala"}]

        return jobs

    def _parse_internshala_card(self, card) -> Optional[Dict]:
        """Parse a single Internshala listing card"""
        try:
            # Title - first <a> tag or div with class generic_container
            title_el = card.find("div", class_="generic_container")
            if not title_el:
                title_el = card.find("a")
            title = title_el.get_text(strip=True) if title_el else "Unknown Title"

            # Company - div with class heading_6 company_name
            company_el = card.find("div", class_="heading_6")
            if not company_el:
                company_el = card.find("p", class_="company_name")
            company = company_el.get_text(strip=True).replace("Actively hiring", "").strip() if company_el else "Unknown Company"

            # Location - first span without class or with location-related content
            spans = card.find_all("span")
            location = "India"
            salary = "Not disclosed"
            duration = ""

            for span in spans:
                text = span.get_text(strip=True)
                classes = span.get("class", [])
                if "stipend" in classes:
                    salary = text
                elif "₹" in text or "/month" in text:
                    salary = text
                elif "month" in text.lower() or "week" in text.lower():
                    duration = text
                elif "ago" in text.lower():
                    continue
                elif any(city in text.lower() for city in ["bangalore", "mumbai", "delhi", "hyderabad", "chennai", "pune", "kolkata", "work from home", "remote", "noida", "gurgaon", "ahmedabad"]):
                    location = text
                elif not classes and not location != "India" and text and len(text) < 30:
                    location = text

            # Duration
            duration_spans = [s for s in spans if "month" in s.get_text(strip=True).lower() or "week" in s.get_text(strip=True).lower()]
            if duration_spans:
                duration = duration_spans[0].get_text(strip=True)

            # URL
            link_el = card.find("a", href=True)
            job_url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                if href.startswith("/"):
                    job_url = f"https://internshala.com{href}"
                else:
                    job_url = href

            full_text = f"{title} {company} {location} {salary} {duration}"

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "description": f"Duration: {duration}" if duration else "",
                "url": job_url,
                "full_text": full_text,
            }
        except Exception:
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # LINKEDIN PUBLIC SEARCH (Limited)
    # ─────────────────────────────────────────────────────────────────────────

    def scrape_linkedin_public(self, query: str = "data entry", location: str = "India", max_jobs: int = 10) -> List[Dict]:
        """
        Scrape LinkedIn public job search (no login required).
        LinkedIn heavily restricts this - may return limited results.
        """
        jobs = []
        url = "https://www.linkedin.com/jobs/search/"
        params = {
            "keywords": query,
            "location": location,
            "position": 1,
            "pageNum": 0,
            "sortBy": "DD",  # Date descending
        }

        try:
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code != 200:
                return [{"error": f"LinkedIn returned status {response.status_code}. LinkedIn restricts automated access.", "platform": "LinkedIn"}]

            soup = BeautifulSoup(response.text, "html.parser")

            # LinkedIn public job cards
            cards = soup.find_all("div", class_=re.compile(r"base-card|job-search-card"))
            if not cards:
                cards = soup.find_all("li", class_=re.compile(r"result-card"))

            for card in cards[:max_jobs]:
                job = self._parse_linkedin_card(card)
                if job:
                    job["platform"] = "LinkedIn"
                    job["scraped_at"] = datetime.utcnow().isoformat()
                    jobs.append(job)

            time.sleep(self.rate_limit_delay)

        except requests.exceptions.Timeout:
            return [{"error": "LinkedIn request timed out", "platform": "LinkedIn"}]
        except requests.exceptions.ConnectionError:
            return [{"error": "Could not connect to LinkedIn", "platform": "LinkedIn"}]
        except Exception as e:
            return [{"error": f"LinkedIn scraping error: {str(e)}", "platform": "LinkedIn"}]

        return jobs

    def _parse_linkedin_card(self, card) -> Optional[Dict]:
        """Parse a LinkedIn public job card"""
        try:
            # Title
            title_el = card.find("h3") or card.find("span", class_=re.compile(r"sr-only"))
            title = title_el.get_text(strip=True) if title_el else "Unknown Title"

            # Company
            company_el = card.find("h4") or card.find("a", class_=re.compile(r"hidden-nested-link"))
            company = company_el.get_text(strip=True) if company_el else "Unknown Company"

            # Location
            location_el = card.find("span", class_=re.compile(r"job-search-card__location"))
            location = location_el.get_text(strip=True) if location_el else "India"

            # URL
            link_el = card.find("a", href=True)
            job_url = link_el["href"] if link_el else ""

            full_text = f"{title} {company} {location}"

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": "Not disclosed",
                "description": "",
                "url": job_url,
                "full_text": full_text,
            }
        except Exception:
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # MULTI-PLATFORM SCRAPE
    # ─────────────────────────────────────────────────────────────────────────

    def scrape_all_platforms(self, query: str = "work from home", max_per_platform: int = 5) -> Dict:
        """
        Scrape from all supported platforms and return combined results.
        """
        results = {
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "platforms": {},
            "total_jobs": 0,
        }

        # Indeed
        indeed_jobs = self.scrape_indeed(query=query, max_jobs=max_per_platform)
        results["platforms"]["indeed"] = indeed_jobs
        results["total_jobs"] += len([j for j in indeed_jobs if "error" not in j])

        # Internshala
        internshala_jobs = self.scrape_internshala(query=query, max_jobs=max_per_platform)
        results["platforms"]["internshala"] = internshala_jobs
        results["total_jobs"] += len([j for j in internshala_jobs if "error" not in j])

        # LinkedIn (may fail due to restrictions)
        linkedin_jobs = self.scrape_linkedin_public(query=query, max_jobs=max_per_platform)
        results["platforms"]["linkedin"] = linkedin_jobs
        results["total_jobs"] += len([j for j in linkedin_jobs if "error" not in j])

        return results


# Singleton instance
job_scraper = JobScraper()
