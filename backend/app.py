"""
AI-Powered Real-Time Job Scam Detection & Prevention System
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
from api.predict import router as predict_router
from api.url_analysis import router as url_router
from api.company_verify import router as company_router
from api.email_analysis import router as email_router
from api.image_analysis import router as image_router
from api.chatbot import router as chatbot_router
from api.auth import router as auth_router
from api.history import router as history_router
from api.feedback import router as feedback_router
from api.analytics import router as analytics_router
from api.scraping import router as scraping_router
from api.retrain import router as retrain_router

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="AI Job Scam Detection Platform",
    description="Enterprise-grade AI-powered recruitment fraud prevention system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(predict_router, prefix="/api", tags=["Scam Detection"])
app.include_router(url_router, prefix="/api", tags=["URL Analysis"])
app.include_router(company_router, prefix="/api", tags=["Company Verification"])
app.include_router(email_router, prefix="/api", tags=["Email Analysis"])
app.include_router(image_router, prefix="/api", tags=["Image Analysis"])
app.include_router(chatbot_router, prefix="/api", tags=["AI Chatbot"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(feedback_router, prefix="/api", tags=["Feedback"])
app.include_router(analytics_router, prefix="/api", tags=["Analytics"])
app.include_router(scraping_router, prefix="/api", tags=["Real-Time Scraping"])
app.include_router(retrain_router, prefix="/api", tags=["Model Retraining"])


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "platform": "AI Job Scam Detection & Prevention System",
        "version": "2.0.0",
        "modules": [
            "NLP Scam Detection",
            "URL & Domain Analysis",
            "Company Verification",
            "Email Authenticity",
            "Image/Logo Verification",
            "Behavioral Fraud Analysis",
            "AI Safety Assistant",
            "Real-Time Risk Scoring"
        ]
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "job-scam-detection-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
