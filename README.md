# 🛡️ AI-Powered Real-Time Job Scam Detection & Prevention System

> Enterprise-grade AI cybersecurity platform for recruitment fraud prevention using multi-modal intelligence

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/React-19-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Overview

An intelligent AI-powered recruitment fraud prevention platform that detects fake jobs and internship scams in real-time using multi-modal analysis including NLP, URL intelligence, email verification, image analysis, and behavioral fraud detection.

## ✨ Key Features

- **🧠 Multi-Modal AI Engine** - NLP + URL + Email + Image + Behavioral analysis
- **⚡ Real-Time Detection** - Instant scam analysis in under 2 seconds
- **📊 Dynamic Risk Scoring** - Weighted ensemble scoring (0-100)
- **🔍 Explainable AI** - Human-readable explanations of WHY a job is suspicious
- **🏢 Company Verification** - Multi-signal company authenticity checks
- **🤖 AI Safety Assistant** - Chatbot for fraud prevention guidance
- **🌐 Chrome Extension** - Browser-based protection on job platforms
- **🇮🇳 India-Specific Intelligence** - Detects regional scam patterns

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                    │
│  Landing │ Dashboard │ Analytics │ Chat │ Company Verify     │
├─────────────────────────────────────────────────────────────┤
│                    REST API (FastAPI)                         │
│  /predict │ /analyze-url │ /verify-company │ /chatbot        │
├─────────────────────────────────────────────────────────────┤
│                 AI/ML ENGINE                                  │
│  NLP │ URL Analysis │ Email │ Image │ Behavioral │ Ensemble  │
├─────────────────────────────────────────────────────────────┤
│              DATABASE (MongoDB Atlas)                         │
│  Users │ Predictions │ History │ Feedback │ Analytics         │
├─────────────────────────────────────────────────────────────┤
│              CHROME EXTENSION (Manifest V3)                   │
│  Content Script │ Popup │ Background Worker                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Train the ML model
python train_model.py

# Start the API server
uvicorn app:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend/fake_job_detection
npm install
npm run dev
```

### Chrome Extension

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/` folder

## 📂 Project Structure

```
├── backend/
│   ├── api/              # API route handlers
│   ├── ml/               # ML models and training pipeline
│   ├── auth/             # JWT authentication
│   ├── database/         # MongoDB connection
│   ├── services/         # Business logic
│   ├── app.py            # FastAPI entry point
│   └── requirements.txt
├── frontend/
│   └── fake_job_detection/
│       ├── src/
│       │   ├── pages/        # React pages
│       │   ├── components/   # Reusable components
│       │   ├── services/     # API client
│       │   └── layouts/      # Layout components
│       └── package.json
├── extension/            # Chrome Extension (Manifest V3)
├── ml_model/             # Trained model artifacts
├── dataset/              # Training datasets
├── docker/               # Docker configuration
└── README.md
```

## 🧠 ML Models

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Logistic Regression | 97.2% | 82.1% | 71.3% | 76.3% |
| Random Forest | 97.8% | 85.4% | 73.8% | 79.2% |
| XGBoost | 98.1% | 87.2% | 76.5% | 81.5% |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Full scam analysis with explainability |
| POST | `/api/quick-scan` | Quick scan for Chrome extension |
| POST | `/api/analyze-url` | URL/domain trust analysis |
| POST | `/api/analyze-email` | Email authenticity check |
| POST | `/api/verify-company` | Company verification |
| POST | `/api/analyze-image` | Image/logo analysis |
| POST | `/api/chatbot` | AI safety assistant |
| GET | `/api/analytics/full` | Dashboard analytics |
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/login` | User login |

## 🛡️ Detection Capabilities

- Registration fee scams
- Fake BPO/call center jobs
- WhatsApp/Telegram recruitment fraud
- Fake internship certificates
- Captcha/data entry scams
- Phishing job portals
- Fake offer letters
- Impersonation of legitimate companies
- Unrealistic salary promises
- Urgency manipulation tactics

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, scikit-learn, XGBoost, spaCy, MongoDB  
**Frontend:** React 19, Vite, Tailwind CSS, Framer Motion, Recharts  
**Extension:** Chrome Manifest V3, JavaScript  
**ML:** TF-IDF, Logistic Regression, Random Forest, XGBoost  
**Deployment:** Docker, Vercel, Render

## 📄 License

MIT License - See LICENSE file for details.
