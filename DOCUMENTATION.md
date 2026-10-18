# AI-Powered Job Scam Detection & Prevention System
## Complete Project Documentation

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Structure](#2-project-structure)
3. [Tech Stack](#3-tech-stack)
4. [Frontend](#4-frontend)
5. [Backend](#5-backend)
6. [Database](#6-database)
7. [Machine Learning & AI](#7-machine-learning--ai)
8. [NLP Pipeline](#8-nlp-pipeline)
9. [Scoring System](#9-scoring-system)
10. [API Reference](#10-api-reference)
11. [Authentication & Security](#11-authentication--security)
12. [External Services & Integrations](#12-external-services--integrations)
13. [Chrome Extension](#13-chrome-extension)
14. [Dataset](#14-dataset)
15. [Environment Configuration](#15-environment-configuration)
16. [How to Run the Project](#16-how-to-run-the-project)
17. [Known Limitations](#17-known-limitations)

---

## 1. Project Overview

**JobScam** is an enterprise-grade, AI-powered platform that detects and prevents job recruitment fraud in real time. It is specifically designed for the Indian job market, where scams like registration fee fraud, fake BPO jobs, and WhatsApp recruitment scams are extremely common.

### What It Does

- Analyzes any job posting text and gives a **risk score from 0–100**
- Verifies company authenticity using domain, WHOIS, SSL, and email checks
- Analyzes URLs for phishing indicators
- Detects fake recruiter emails
- Analyzes uploaded images/offer letters for manipulation
- Scrapes live job listings from Indeed, Internshala, and LinkedIn and auto-scans them
- Provides an AI chatbot for scam awareness education
- Tracks scan history and provides analytics dashboard

### Who Should Use This

- Job seekers who want to verify if a job posting is genuine
- HR teams who want to flag suspicious inbound recruitment spam
- Students checking internship offers before paying any fees

---

## 2. Project Structure

```
JobScam/
├── backend/                    # FastAPI Python backend
│   ├── api/                    # All REST API route handlers
│   │   ├── predict.py          # Core scam detection endpoint
│   │   ├── auth.py             # Register / Login / Profile
│   │   ├── url_analysis.py     # URL & domain phishing check
│   │   ├── email_analysis.py   # Recruiter email verification
│   │   ├── company_verify.py   # Company authenticity check
│   │   ├── image_analysis.py   # Image/offer letter fraud detection
│   │   ├── chatbot.py          # AI safety assistant
│   │   ├── history.py          # Scan history retrieval
│   │   ├── feedback.py         # User feedback & scam reports
│   │   ├── analytics.py        # Dashboard analytics data
│   │   └── scraping.py         # Live job scraping + auto-scan
│   ├── auth/
│   │   └── jwt_handler.py      # JWT token generation & validation
│   ├── database/
│   │   └── connection.py       # MongoDB connection + collections
│   ├── ml/
│   │   ├── scam_detector.py    # Core ML + rule-based detection engine
│   │   └── train_pipeline.py   # Model training pipeline (run once)
│   ├── scraping/
│   │   └── job_scraper.py      # Web scraper for job platforms
│   ├── services/
│   │   └── company_engine.py   # Company verification logic
│   ├── app.py                  # FastAPI app entry point
│   ├── train_model.py          # Shortcut to run training
│   ├── test_model.py           # Quick test of trained model
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (secret)
│   └── .env.example            # Template for environment variables
│
├── frontend/
│   └── fake_job_detection/     # React + Vite frontend
│       ├── src/
│       │   ├── pages/          # All application pages
│       │   ├── components/     # Reusable UI components
│       │   ├── layouts/        # Page wrapper with Navbar/Sidebar
│       │   ├── services/
│       │   │   └── api.js      # Axios API client (all API calls)
│       │   ├── App.jsx         # Router configuration
│       │   └── main.jsx        # React entry point
│       ├── package.json
│       └── index.html
│
├── dataset/
│   ├── fake_job_postings.csv   # Labeled dataset for training ML model
│   └── Phishing_Email.csv      # Phishing email samples
│
├── extension/                  # Chrome browser extension
│   ├── manifest.json
│   ├── popup/                  # Extension popup UI
│   ├── content/                # Content script (injects into pages)
│   └── background/             # Background service worker
│
├── docker/                     # Docker deployment files
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
│
└── DOCUMENTATION.md            # This file
```

---

## 3. Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10 | Primary backend language |
| FastAPI | 0.104.1 | REST API framework (async) |
| Uvicorn | 0.24.0 | ASGI server |
| Pydantic | 2.5.2 | Data validation & schemas |
| Motor | 3.3.2 | Async MongoDB driver |
| PyMongo | 4.6.1 | MongoDB utilities |
| Scikit-learn | 1.3.2 | ML model training & TF-IDF |
| XGBoost | 2.0.3 | Gradient boosting classifier |
| Joblib | 1.3.2 | Model serialization |
| Pandas | 2.1.4 | Dataset processing |
| NumPy | 1.26.2 | Numerical operations |
| Pillow | 10.1.0 | Image processing |
| BeautifulSoup4 | 4.12.2 | Web scraping HTML parsing |
| Requests | 2.31.0 | HTTP calls & scraping |
| Python-WHOIS | 0.8.0 | Domain registration lookup |
| Python-Jose | 3.3.0 | JWT token handling |
| Passlib + bcrypt | 1.7.4 | Password hashing |
| SlowAPI | 0.1.9 | Rate limiting |
| Python-dotenv | 1.0.0 | Environment variable loading |
| google-generativeai | 0.3.2 | Gemini AI (configured, not wired yet) |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 19.2.5 | UI framework |
| Vite | 8.0.10 | Build tool & dev server |
| React Router DOM | 6.21.1 | Client-side routing |
| Axios | 1.6.2 | HTTP client for API calls |
| Framer Motion | 10.16.16 | Animations |
| Lucide React | 0.469.0 | Icon library |
| Recharts | 2.15.0 | Charts for analytics dashboard |
| React Hot Toast | 2.4.1 | Toast notifications |
| React Markdown | 9.0.1 | Render markdown in chatbot |
| TailwindCSS | 3.4.0 | Utility-first CSS framework |

### Database
| Technology | Purpose |
|---|---|
| MongoDB Atlas | Cloud-hosted database (primary) |
| MongoDB (local) | Fallback if Atlas not configured |

---

## 4. Frontend

### Pages

| Page | Route | Description |
|---|---|---|
| Landing | `/` | Public homepage with hero section and feature overview |
| Login | `/login` | User authentication |
| Register | `/register` | New user registration |
| Dashboard | `/dashboard` | Main scam detection tool — paste job text, get risk score |
| Analytics | `/analytics` | Charts showing scam trends, risk distribution, threat feed |
| Company Verify | `/company-verify` | Verify a company's authenticity |
| Chat Assistant | `/chat` | AI chatbot for scam awareness Q&A |
| History | `/history` | Past scan results with pagination |
| Awareness | `/awareness` | Educational content about job scam types |
| Live Scraping | `/live-scraping` | Scrape live jobs from platforms and auto-scan them |

### Components

| Component | Purpose |
|---|---|
| `Navbar.jsx` | Top navigation bar |
| `Sidebar.jsx` | Side navigation menu |
| `RiskMeter.jsx` | Visual gauge showing risk score (0–100) |
| `ThreatBadge.jsx` | Color-coded badge showing risk level |
| `LoadingAnimation.jsx` | Loading spinner during API calls |
| `Layout.jsx` | Wrapper that provides Navbar + Sidebar to all inner pages |

### API Service Layer (`services/api.js`)

All API calls are centralized in one file using Axios. It:
- Sets base URL from `VITE_API_URL` env var or defaults to `http://localhost:8000/api`
- Automatically injects JWT token from `localStorage` into every request header
- Exports named functions for every backend endpoint

### Authentication Flow (Frontend)
1. User logs in via `/login` → receives JWT token
2. Token stored in `localStorage`
3. Every subsequent API request sends `Authorization: Bearer <token>` automatically
4. On logout, token is removed from `localStorage`

---

## 5. Backend

### Entry Point (`app.py`)

The FastAPI application is created in `app.py`. It:
- Loads environment variables from `.env`
- Registers all API routers with their URL prefixes
- Configures CORS (allows frontend at `localhost:5173` by default)
- Adds rate limiting via SlowAPI
- Exposes `/docs` (Swagger UI) and `/redoc` for API documentation
- Has a `/health` endpoint for uptime monitoring

### API Routers

| Router | Prefix | File |
|---|---|---|
| Authentication | `/api/auth` | `api/auth.py` |
| Scam Detection | `/api` | `api/predict.py` |
| URL Analysis | `/api` | `api/url_analysis.py` |
| Company Verify | `/api` | `api/company_verify.py` |
| Email Analysis | `/api` | `api/email_analysis.py` |
| Image Analysis | `/api` | `api/image_analysis.py` |
| Chatbot | `/api` | `api/chatbot.py` |
| History | `/api` | `api/history.py` |
| Feedback | `/api` | `api/feedback.py` |
| Analytics | `/api` | `api/analytics.py` |
| Live Scraping | `/api` | `api/scraping.py` |

### Key Backend Files Explained

#### `ml/scam_detector.py` — The Brain
This is the most important file. It's a singleton class `ScamDetectionEngine` that:
- Loads the trained ML model and TF-IDF vectorizer from disk on startup
- On every analysis, runs 5 independent signal checks
- Combines them with a weighted formula to produce a final risk score
- Generates human-readable explanations for every result

#### `ml/train_pipeline.py` — Model Training
Run this once to train the model. It:
- Loads `fake_job_postings.csv`
- Combines title + description + requirements + benefits into one text column
- Vectorizes with TF-IDF
- Trains Logistic Regression, Random Forest, and XGBoost
- Saves the best model (by F1-score) to `ml_model/model.pkl`
- Saves the vectorizer to `ml_model/vectorizer.pkl`

#### `services/company_engine.py` — Company Verification
Multi-step company verification:
1. Checks against a hardcoded known company database (TCS, Infosys, Google, etc.)
2. DNS resolution check
3. WHOIS domain age lookup
4. SSL certificate validity check
5. Website HTTP accessibility check
6. Email domain matching
7. Source platform credibility
8. Company name pattern analysis (suspicious keywords, excessive numbers, ALL CAPS)

#### `scraping/job_scraper.py` — Web Scraper
Scrapes live jobs from:
- **Indeed India** (`indeed.co.in`) — public search results
- **Internshala** — internship and job listings
- **LinkedIn** — public job search (limited, often blocked)

Each scraped job is passed through `scam_engine.analyze_text()` and returned with a risk score.

#### `auth/jwt_handler.py` — Security
- Passwords hashed with bcrypt
- JWT tokens use HS256 algorithm
- Tokens expire after 1440 minutes (24 hours) by default

---

## 6. Database

### Database: MongoDB

**Connection:** Configured via `MONGODB_URL` in `.env`
- Cloud: MongoDB Atlas (`mongodb+srv://...`)
- Local fallback: `mongodb://localhost:27017`
- Database name: `fake_job_detection`

### Collections

| Collection | What It Stores |
|---|---|
| `users` | User accounts (name, email, hashed password, role, scan stats) |
| `scam_predictions` | Every prediction result (text snippet, risk score, risk level, timestamp) |
| `scan_history` | Detailed scan history for the history page |
| `company_verification` | Company verification results |
| `feedback` | User feedback on predictions + scam reports |
| `chatbot_logs` | Chatbot conversation logs |
| `analytics` | Aggregated analytics data |

### Graceful Fallback

If MongoDB is unavailable (Motor not installed or DB unreachable), every collection is replaced by a `MockCollection` that silently accepts all writes without persisting. The app keeps running but data is not saved.

---

## 7. Machine Learning & AI

### Training Data

- **File:** `dataset/fake_job_postings.csv`
- **Source:** EMSCAD dataset (Employment Scam Aegean Dataset)
- **Size:** ~17,000 labeled job postings
- **Label:** `fraudulent` column (0 = real, 1 = fake)
- **Features used:** `title + company_profile + description + requirements + benefits`

### Three Models Trained (Competition)

| Model | Type | Key Parameters |
|---|---|---|
| Logistic Regression | Linear classifier | `C=1.0`, `max_iter=1000` |
| Random Forest | Ensemble (Bagging) | `100 trees`, `max_depth=20`, `n_jobs=-1` |
| XGBoost | Ensemble (Gradient Boosting) | `100 estimators`, `lr=0.1`, `max_depth=6` |

All three are trained, evaluated, and compared. The best by **F1-score** is saved as `model.pkl`.

### Model Evaluation Metrics

For each model, these metrics are computed:
- **Accuracy** — overall correct predictions
- **Precision** — of jobs flagged as scam, how many actually are
- **Recall** — of all actual scams, how many were caught
- **F1-Score** — harmonic mean of precision and recall (primary selection metric)
- **ROC-AUC** — area under the receiver operating curve
- **5-Fold Cross-Validation F1** — stability across different data splits

### Why F1 and Not Accuracy?

The dataset is imbalanced (~17% fake, ~83% real). A model that always says "real" would be 83% accurate but useless. F1-score penalizes models that miss scams (low recall) or cry wolf too often (low precision), making it the correct metric here.

### How the Trained Model is Used

```
Job Text Input
      ↓
TF-IDF Vectorizer → 5000-dimensional sparse vector
      ↓
Classifier.predict()     → 0 (real) or 1 (fake)
Classifier.predict_proba() → [p_real, p_fake]
      ↓
ml_score = p_fake  (used as 25% weight in final score)
```

### ML Model Fallback

If `ml_model/model.pkl` doesn't exist (model not trained yet), `ml_score` defaults to `0.0` and the system falls back entirely to rule-based detection. The app still works — it just relies on regex and behavioral checks only.

---

## 8. NLP Pipeline

This project uses **classical NLP**, not deep learning or transformers.

### Step 1 — Text Preprocessing

```python
text_lower = text.lower()  # Lowercase normalization
```

No stemming, lemmatization, or tokenization beyond what TF-IDF handles internally.

### Step 2 — TF-IDF Vectorization

**TF-IDF (Term Frequency–Inverse Document Frequency)** converts text into numbers.

- **TF** = how often a word appears in this document
- **IDF** = how rare the word is across all documents (rare words carry more weight)
- **TF × IDF** = words that are frequent in this post but rare overall → most informative

Configuration:
```python
TfidfVectorizer(
    stop_words="english",   # Remove: the, is, at, which, on, etc.
    max_features=5000,       # Keep only top 5000 informative terms
    ngram_range=(1, 2),      # Capture both single words AND two-word phrases
    min_df=2,                # Ignore terms appearing in fewer than 2 documents
    max_df=0.95              # Ignore terms appearing in more than 95% of documents
)
```

The `ngram_range=(1, 2)` is important — it captures phrases like `"no interview"`, `"work from home"`, `"registration fee"` as single features, not just individual words.

### Step 3 — Rule-Based Pattern Matching (on top of ML)

Four layers of regex-based checks run in parallel with ML:

**Layer 1 — Scam Phrase Detection (35 patterns)**
India-specific scam language patterns:
```
"earn .* lakh", "no interview", "pay registration fee",
"guaranteed placement", "captcha typing", "work from home.*earn",
"data entry.*earn", "joining fee", "earn.*daily", etc.
```

**Layer 2 — Urgency Phrase Detection (15 patterns)**
Psychological manipulation tactics:
```
"limited seats", "last date today", "hurry up",
"urgent requirement", "join today", "act now", etc.
```

**Layer 3 — Suspicious Salary Pattern Detection (8 regex patterns)**
Numeric patterns for unrealistic salaries:
```
₹\s*\d+\s*lakh, \d+\s*lakh\s*per\s*month,
earn\s*₹?\s*\d{5,}, \$\s*\d{4,}\s*per\s*day, etc.
```

**Layer 4 — Behavioral Red Flags (6 checks)**
```
- WhatsApp or Telegram mentioned
- "No interview" or "no experience required"
- Payment/fee requested to join/register
- HR using Gmail/Yahoo/Hotmail
- Job description under 50 words
- No qualification or skill requirement mentioned
```

**Layer 5 — Legitimacy Indicators (15 patterns, reduces risk)**
```
"years of experience", "bachelor", "ctc", "health insurance",
"background verification", "notice period", etc.
```

### What NLP is NOT Used

| Technique | Status | Why Not |
|---|---|---|
| Word2Vec / GloVe | ❌ Not used | Not needed for this binary classification task |
| BERT / Transformers | ❌ Not used | Overkill for keyword-heavy scam detection |
| spaCy NLP pipeline | ❌ Not used | Installed but not called |
| Named Entity Recognition | ❌ Not used | Could improve company name detection |
| Sentiment Analysis | ❌ Not used | Not directly relevant |
| Google Gemini LLM | ⚠️ Configured | Key in .env but not wired into code yet |

---

## 9. Scoring System

### Five Signal Channels

Every piece of text goes through 5 channels. Each produces a score from 0–100:

| Channel | How Score is Computed | Weight |
|---|---|---|
| ML Model | `predict_proba()[1]` × 100 | **25%** |
| Scam Phrases | `count of matches × 25`, capped at 100 | **32%** |
| Salary Risk | `count of patterns matched × 35`, capped at 100 | **16%** |
| Urgency Phrases | `count of matches × 30`, capped at 100 | **12%** |
| Behavioral Flags | `count of flags × 22`, capped at 100 | **15%** |

Weights sum to exactly **1.0 (100%)**.

### Final Risk Score Formula

```python
raw_score = (
    ml_score        × 0.25 +
    scam_phrase_score × 0.32 +
    urgency_score   × 0.12 +
    salary_score    × 0.16 +
    behavioral_score × 0.15
)

# Legitimacy reduction ONLY if signals are weak (raw_score < 40)
legitimacy_reduction = min(legitimacy_score × 0.08, 8) if raw_score < 40 else 0

final_score = clamp(raw_score - legitimacy_reduction, 0, 100)
```

### Risk Level Thresholds

| Score | Risk Level | Meaning |
|---|---|---|
| 0 – 20 | 🟢 Safe | Appears to be a legitimate job posting |
| 21 – 40 | 🔵 Low Risk | Minor concerns, likely safe but verify |
| 41 – 60 | 🟡 Medium Risk | Suspicious patterns found, verify independently |
| 61 – 80 | 🔴 High Risk | Strong scam indicators, do not share personal info |
| 81 – 100 | 🚨 Critical Scam | Multiple strong signals, almost certainly a scam |

### Confidence Score

A separate confidence score (0–100%) measures how many signal channels fired:

```python
signals = 0
if scam_phrases_detected:    signals += 1
if urgency_phrases_detected: signals += 1
if suspicious_salary_claims: signals += 1
if red_flags:                signals += 1
if ml_prediction != "unknown": signals += 1

confidence = min(signals / 5 × 100, 98)
```

---

## 10. API Reference

### Base URL
```
http://localhost:8000/api
```

### Interactive API Docs
```
http://localhost:8000/docs       (Swagger UI)
http://localhost:8000/redoc      (ReDoc)
```

### Endpoints

#### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/profile` | Get current user profile (requires auth) |

#### Scam Detection
| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict` | Full scam analysis of job text |
| POST | `/quick-scan` | Simplified scan (used by Chrome extension) |

#### Analysis Tools
| Method | Endpoint | Description |
|---|---|---|
| POST | `/analyze-url` | Check a URL for phishing indicators |
| POST | `/analyze-email` | Verify recruiter email authenticity |
| POST | `/verify-company` | Full company authenticity check |
| POST | `/analyze-image` | Upload an image/offer letter for fraud check |

#### Live Scraping
| Method | Endpoint | Description |
|---|---|---|
| POST | `/scrape-jobs` | Scrape live jobs and auto-scan them |
| GET | `/scrape-jobs/platforms` | List supported platforms |

#### Data & History
| Method | Endpoint | Description |
|---|---|---|
| GET | `/history` | Get scan history (paginated) |
| GET | `/history/stats` | Get overall scan statistics |
| GET | `/analytics/full` | Full analytics dashboard data |
| GET | `/analytics/overview` | Summary stats |
| GET | `/analytics/trends` | Monthly scam trend data |
| GET | `/analytics/risk-distribution` | Risk level breakdown |
| GET | `/analytics/scam-types` | Scam type breakdown |
| GET | `/analytics/threats` | Recent threat intelligence feed |

#### Community
| Method | Endpoint | Description |
|---|---|---|
| POST | `/chatbot` | Send a message to the AI safety assistant |
| GET | `/chatbot/suggestions` | Get suggested questions |
| POST | `/feedback` | Submit feedback on a prediction |
| POST | `/report-scam` | Report a scam to the community |

### Example Request — Predict

```json
POST /api/predict
{
  "text": "Earn 2 lakh per month from home. No interview needed. Pay ₹500 registration fee. Urgent requirement. Join today.",
  "url": "http://fakejobs.xyz",
  "email": "hr.tcs.jobs@gmail.com",
  "source": "web"
}
```

### Example Response — Predict

```json
{
  "risk_score": 82,
  "risk_level": "Critical Scam",
  "confidence": 98.0,
  "ml_prediction": "fake",
  "ml_confidence": 91.3,
  "scam_phrases_detected": ["earn  lakh", "no interview", "pay registration fee"],
  "urgency_phrases_detected": ["urgent requirement", "join today"],
  "suspicious_salary_claims": ["2 lakh per month"],
  "red_flags": [
    "Payment requested from candidate",
    "No proper hiring process mentioned",
    "Very short job description"
  ],
  "legitimacy_indicators": [],
  "explanation": [
    "⚠️ Contains 3 known scam phrases",
    "⚠️ Uses psychological urgency tactics",
    "🚩 Payment requested from candidate",
    "🤖 ML Model predicts FAKE with 91.3% confidence",
    "❌ VERDICT: This job posting has strong scam indicators."
  ],
  "scam_phrase_score": 75,
  "urgency_score": 60,
  "salary_risk_score": 35,
  "behavioral_score": 66
}
```

---

## 11. Authentication & Security

### JWT (JSON Web Tokens)

- **Algorithm:** HS256
- **Expiry:** 24 hours (1440 minutes, configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Secret:** Set via `SECRET_KEY` in `.env`
- **Storage (frontend):** `localStorage`
- **Transmission:** `Authorization: Bearer <token>` header

### Password Security

- Passwords are **never stored in plain text**
- Hashed using **bcrypt** via `passlib`
- Verification done by comparing the hash, not the original password

### Rate Limiting

SlowAPI is configured to prevent API abuse. Limits are applied per IP address.

### CORS

Only origins listed in `CORS_ORIGINS` env variable are allowed. Default: `http://localhost:5173`.

---

## 12. External Services & Integrations

| Service | Status | What It Does | Key Required |
|---|---|---|---|
| **MongoDB Atlas** | ✅ Active | Cloud database for all persistent data | `MONGODB_URL` |
| **WHOIS Lookup** | ✅ Active | Checks domain registration age | None (library) |
| **SSL/DNS Checks** | ✅ Active | Verifies HTTPS and domain resolution | None (built-in) |
| **Indeed Scraping** | ✅ Active | Scrapes live Indian job listings | None |
| **Internshala Scraping** | ✅ Active | Scrapes internship/job listings | None |
| **LinkedIn Scraping** | ⚠️ Limited | Often blocked by LinkedIn | None |
| **Google Gemini AI** | ⚠️ Configured | Planned for chatbot upgrade to LLM | `GEMINI_API_KEY` |
| **VirusTotal** | ⚠️ Configured | URL threat intelligence | `VIRUSTOTAL_API_KEY` |
| **Google Safe Browsing** | ⚠️ Configured | Phishing URL database | `GOOGLE_SAFE_BROWSING_KEY` |

> **Note:** The three "Configured" services have API keys in `.env.example` but are not yet wired into the codebase. They are prepared for future integration.

---

## 13. Chrome Extension

Located in the `extension/` folder. It's a Manifest V3 browser extension.

### Files

| File | Purpose |
|---|---|
| `manifest.json` | Extension configuration (permissions, icons, scripts) |
| `popup/popup.html` | Extension popup UI |
| `popup/popup.js` | Popup logic — reads page text, calls `/api/quick-scan` |
| `popup/popup.css` | Popup styles |
| `content/content.js` | Injected into job listing pages to auto-extract text |
| `content/content.css` | Styles for injected UI elements |
| `background/background.js` | Background service worker |

### How It Works

1. User visits a job listing page (LinkedIn, Naukri, Indeed, etc.)
2. Content script extracts the job description text
3. User clicks the extension icon to open the popup
4. Popup sends the extracted text to `/api/quick-scan`
5. Risk score and top 3 reasons are displayed in the popup

### To Install
1. Open Chrome → `chrome://extensions`
2. Enable "Developer Mode"
3. Click "Load Unpacked"
4. Select the `extension/` folder

---

## 14. Dataset

### fake_job_postings.csv

- **Rows:** ~17,880 job postings
- **Source:** EMSCAD (Employment Scam Aegean Dataset)
- **Label column:** `fraudulent` (0 = real, 1 = fake)
- **Other columns:** `job_id`, `title`, `location`, `department`, `salary_range`, `company_profile`, `description`, `requirements`, `benefits`, `telecommuting`, `has_company_logo`, `has_questions`, `employment_type`, `required_experience`, `required_education`, `industry`, `function`
- **Used columns:** `title`, `company_profile`, `description`, `requirements`, `benefits`, `fraudulent`
- **Class distribution:** ~17% fake, ~83% real (imbalanced)

### Phishing_Email.csv

- Contains labeled phishing email samples
- Currently not used in model training
- Available for future email analysis model training

---

## 15. Environment Configuration

Copy `backend/.env.example` to `backend/.env` and fill in your values:

```env
# MongoDB — Required for data persistence
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/fake_job_detection
DATABASE_NAME=fake_job_detection

# JWT — Change this to a strong random string in production
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# API Keys — Optional (features work without them, some degrade gracefully)
GEMINI_API_KEY=your-gemini-api-key
VIRUSTOTAL_API_KEY=your-virustotal-api-key
GOOGLE_SAFE_BROWSING_KEY=your-google-safe-browsing-key

# App Config
APP_ENV=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

> **Minimum required to run:** Only `SECRET_KEY` is strictly needed. Without `MONGODB_URL`, data won't persist but the app still runs with mock collections.

---

## 16. How to Run the Project

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- MongoDB Atlas account (optional but recommended)

### Step 1 — Install Backend Dependencies

```cmd
cd backend
pip install -r requirements.txt
```

### Step 2 — Configure Environment

```cmd
copy .env.example .env
```
Edit `.env` and set your `MONGODB_URL` and `SECRET_KEY`.

### Step 3 — Train the ML Model (First Time Only)

```cmd
cd backend
python train_model.py
```

This creates `ml_model/model.pkl` and `ml_model/vectorizer.pkl`. Without this step, the ML signal defaults to 0 and only rule-based detection runs.

### Step 4 — Start the Backend

```cmd
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5 — Install Frontend Dependencies

```cmd
cd frontend/fake_job_detection
npm install
```

### Step 6 — Start the Frontend

```cmd
cd frontend/fake_job_detection
npm run dev
```

### Access the Application

| URL | Description |
|---|---|
| `http://localhost:5173` | Frontend web app |
| `http://localhost:8000/docs` | Swagger API documentation |
| `http://localhost:8000/health` | Backend health check |

### Docker (Alternative)

```cmd
cd docker
docker-compose up --build
```

---

## 17. Known Limitations

| Limitation | Impact | Potential Fix |
|---|---|---|
| ML model not trained by default | Falls back to rule-based only | Run `python train_model.py` |
| Analytics data is mocked | Dashboard shows hardcoded numbers | Replace with real MongoDB aggregation queries |
| Chatbot uses keyword matching, not LLM | Cannot answer arbitrary questions | Wire in Google Gemini API |
| LinkedIn scraping is unreliable | Often returns 0 results | Use LinkedIn Official API or a proxy service |
| VirusTotal & Safe Browsing not wired | URL analysis is limited to domain heuristics | Implement API calls in `url_analysis.py` |
| No rate limit configuration exposed | Hard to tune per-endpoint limits | Add per-route SlowAPI decorators |
| No admin panel | Cannot review feedback/scam reports | Build an admin dashboard page |
| Model needs periodic retraining | Scam patterns evolve over time | Schedule monthly retraining with new data |
| No HTTPS in development | Fine locally, required in production | Configure nginx SSL in docker setup |

---

*Documentation generated for JobScam v2.0.0*
