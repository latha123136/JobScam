"""
AI Safety Assistant / Chatbot API
Provides scam awareness, fraud prevention guidance, and job safety education
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    suggestions: List[str]
    category: str


# ─── Knowledge Base ────────────────────────────────────────────────────────────

SCAM_KNOWLEDGE_BASE = {
    "registration fee": {
        "response": "🚨 **Red Flag: Registration Fee Request**\n\nLegitimate companies NEVER ask candidates to pay registration fees, processing fees, or security deposits. This is one of the most common job scam tactics in India.\n\n**What to do:**\n- Immediately stop communication\n- Do not transfer any money\n- Report the job posting on the platform\n- Block the recruiter\n\n**Remember:** If you have to pay to get a job, it's NOT a job — it's a scam.",
        "category": "scam_warning"
    },
    "fake offer letter": {
        "response": "📄 **How to Identify Fake Offer Letters:**\n\n1. **Check the email domain** - Legitimate companies use corporate emails (e.g., hr@tcs.com), not Gmail/Yahoo\n2. **Verify the company** - Search for the company on MCA portal, LinkedIn, and Glassdoor\n3. **Look for errors** - Fake letters often have spelling mistakes, wrong logos, or inconsistent formatting\n4. **Contact HR directly** - Call the company's official number to verify\n5. **Check salary** - If it's too good to be true, it probably is\n\n**Red flags in offer letters:**\n- Sent via WhatsApp/Telegram\n- Asks for immediate joining\n- Requests payment for background verification\n- No proper company letterhead\n- Generic content without specific role details",
        "category": "education"
    },
    "whatsapp job": {
        "response": "📱 **WhatsApp/Telegram Job Scams:**\n\nScammers increasingly use WhatsApp and Telegram to reach victims because:\n- No verification required\n- Easy to create fake profiles\n- Messages can be deleted\n- Difficult to trace\n\n**Common WhatsApp job scam patterns:**\n- \"Hi, I'm HR from [Big Company]\"\n- Part-time work offers with high pay\n- Like/review/rating tasks\n- Crypto investment schemes disguised as jobs\n- Data entry work requiring upfront payment\n\n**Safety Rule:** No legitimate company conducts their entire hiring process on WhatsApp or Telegram.",
        "category": "scam_warning"
    },
    "safe job search": {
        "response": "✅ **Safe Job Search Tips:**\n\n1. **Use verified platforms** - LinkedIn, Naukri, Indeed, Internshala\n2. **Research the company** - Check MCA registration, Glassdoor reviews, LinkedIn presence\n3. **Verify the recruiter** - Look them up on LinkedIn, verify their corporate email\n4. **Never pay money** - Legitimate jobs don't require payment from candidates\n5. **Trust your instincts** - If something feels wrong, it probably is\n6. **Check the job description** - Vague descriptions with high pay are red flags\n7. **Verify offer letters** - Call the company's official number\n8. **Protect your data** - Don't share Aadhaar, PAN, or bank details before joining\n\n**Golden Rule:** A real job pays YOU, not the other way around.",
        "category": "education"
    },
    "internship scam": {
        "response": "🎓 **Internship Scam Warning:**\n\nStudents are prime targets for internship scams. Watch out for:\n\n**Red Flags:**\n- \"Guaranteed internship certificate\" for a fee\n- No interview or selection process\n- Work involves only watching videos or filling forms\n- Certificate from unknown/unverifiable organization\n- Bulk WhatsApp messages offering internships\n- \"Pay ₹999 for training, get internship\"\n\n**Legitimate Internships:**\n- Have a proper application process\n- Provide real work assignments\n- Have a supervisor/mentor\n- Come from verifiable companies\n- Don't require payment from interns\n\n**Verify on:** Internshala, LinkedIn, company's official career page",
        "category": "education"
    },
    "report scam": {
        "response": "🛡️ **How to Report Job Scams in India:**\n\n1. **Cyber Crime Portal** - cybercrime.gov.in (National Cyber Crime Reporting Portal)\n2. **Helpline** - Call 1930 (Cyber Crime Helpline)\n3. **Platform Reporting** - Report on LinkedIn/Naukri/Indeed\n4. **Police Complaint** - File FIR at local police station\n5. **RBI** - If money was transferred, contact your bank immediately\n\n**What to preserve:**\n- Screenshots of conversations\n- Email headers\n- Payment receipts\n- Job posting links\n- Recruiter contact details\n\n**Act fast** - The sooner you report, the higher the chance of recovery.",
        "category": "action"
    },
    "red flags": {
        "response": "🚩 **Top Job Scam Red Flags:**\n\n1. ❌ Asks for money (registration/training/security deposit)\n2. ❌ Too-good-to-be-true salary\n3. ❌ No interview process\n4. ❌ Recruiter uses Gmail/Yahoo for corporate communication\n5. ❌ Urgency pressure (\"Join today or lose the offer\")\n6. ❌ Vague job description\n7. ❌ Communication only via WhatsApp/Telegram\n8. ❌ Company website doesn't exist or looks fake\n9. ❌ No company LinkedIn presence\n10. ❌ Asks for sensitive documents before selection\n11. ❌ Offers work-from-home with unrealistic pay\n12. ❌ No physical office address\n13. ❌ Newly created website/social media\n14. ❌ Generic offer letter without specific details\n15. ❌ Recruiter avoids video calls",
        "category": "education"
    }
}

# Default responses for unmatched queries
DEFAULT_RESPONSES = [
    {
        "response": "I'm your AI Job Safety Assistant. I can help you with:\n\n• Identifying fake job postings\n• Verifying company authenticity\n• Understanding scam red flags\n• Safe job search practices\n• Reporting fraud\n\nWhat would you like to know about job safety?",
        "category": "general"
    }
]

SUGGESTED_QUESTIONS = [
    "What are common job scam red flags?",
    "How to identify fake offer letters?",
    "Is it safe if a company asks for registration fee?",
    "How to verify a company's authenticity?",
    "What are WhatsApp job scams?",
    "How to report a job scam in India?",
    "Are internship certificate scams common?",
    "How to do a safe job search?"
]


# ─── Chat Logic ────────────────────────────────────────────────────────────────

def get_chatbot_response(message: str) -> dict:
    """Generate contextual response based on user query"""
    message_lower = message.lower()

    # Match against knowledge base
    best_match = None
    best_score = 0

    for key, value in SCAM_KNOWLEDGE_BASE.items():
        keywords = key.split()
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > best_score:
            best_score = score
            best_match = value

    # Additional keyword matching
    if not best_match or best_score == 0:
        if any(w in message_lower for w in ["fee", "pay", "money", "deposit", "charge"]):
            best_match = SCAM_KNOWLEDGE_BASE["registration fee"]
        elif any(w in message_lower for w in ["whatsapp", "telegram", "message"]):
            best_match = SCAM_KNOWLEDGE_BASE["whatsapp job"]
        elif any(w in message_lower for w in ["offer letter", "appointment", "joining letter"]):
            best_match = SCAM_KNOWLEDGE_BASE["fake offer letter"]
        elif any(w in message_lower for w in ["intern", "certificate", "student"]):
            best_match = SCAM_KNOWLEDGE_BASE["internship scam"]
        elif any(w in message_lower for w in ["report", "complaint", "police", "cyber crime"]):
            best_match = SCAM_KNOWLEDGE_BASE["report scam"]
        elif any(w in message_lower for w in ["red flag", "warning", "sign", "identify", "detect"]):
            best_match = SCAM_KNOWLEDGE_BASE["red flags"]
        elif any(w in message_lower for w in ["safe", "tip", "advice", "protect", "how to"]):
            best_match = SCAM_KNOWLEDGE_BASE["safe job search"]

    if best_match:
        return {
            "response": best_match["response"],
            "suggestions": SUGGESTED_QUESTIONS[:4],
            "category": best_match["category"]
        }

    return {
        "response": DEFAULT_RESPONSES[0]["response"],
        "suggestions": SUGGESTED_QUESTIONS[:4],
        "category": "general"
    }


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/chatbot", response_model=ChatResponse)
async def chat(data: ChatRequest):
    """AI Safety Assistant - answers questions about job scams and fraud prevention"""
    if not data.message or len(data.message.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please enter a message")

    result = get_chatbot_response(data.message)
    return ChatResponse(**result)


@router.get("/chatbot/suggestions")
async def get_suggestions():
    """Get suggested questions for the chatbot"""
    return {"suggestions": SUGGESTED_QUESTIONS}
