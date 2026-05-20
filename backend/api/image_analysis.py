"""
Image & Logo Verification API
Analyzes uploaded images for manipulation, fake logos, and suspicious content
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import io
import re

router = APIRouter()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class ImageAnalysisResponse(BaseModel):
    filename: str
    file_size_kb: float
    dimensions: str
    format: str
    trust_score: int
    risk_indicators: List[str]
    trust_indicators: List[str]
    verdict: str
    analysis_details: dict


# ─── Analysis Logic ────────────────────────────────────────────────────────────

class ImageAnalyzer:
    """Image and document fraud detection analyzer"""

    # Minimum dimensions for legitimate company logos
    MIN_LOGO_SIZE = 50
    MAX_LOGO_SIZE = 5000

    # Suspicious file characteristics
    SUSPICIOUS_METADATA_KEYS = ["software", "creator", "producer"]

    def analyze_image(self, image_bytes: bytes, filename: str) -> dict:
        """Analyze an uploaded image for fraud indicators"""
        risk_indicators = []
        trust_indicators = []
        trust_score = 50
        analysis_details = {}

        try:
            img = Image.open(io.BytesIO(image_bytes))
        except Exception:
            return {
                "filename": filename,
                "file_size_kb": len(image_bytes) / 1024,
                "dimensions": "N/A",
                "format": "Unknown",
                "trust_score": 10,
                "risk_indicators": ["File could not be opened as a valid image"],
                "trust_indicators": [],
                "verdict": "Invalid Image File",
                "analysis_details": {}
            }

        width, height = img.size
        img_format = img.format or "Unknown"
        file_size_kb = len(image_bytes) / 1024

        analysis_details["width"] = width
        analysis_details["height"] = height
        analysis_details["mode"] = img.mode
        analysis_details["format"] = img_format

        # ─── Resolution Analysis ──────────────────────────────────────────
        if width < self.MIN_LOGO_SIZE or height < self.MIN_LOGO_SIZE:
            trust_score -= 15
            risk_indicators.append("Very low resolution - possibly cropped or fake")
        elif width > 200 and height > 200:
            trust_score += 10
            trust_indicators.append("Adequate resolution for legitimate document")

        # ─── File Size Analysis ───────────────────────────────────────────
        if file_size_kb < 5:
            trust_score -= 10
            risk_indicators.append("Extremely small file size - may be low quality screenshot")
        elif file_size_kb > 10000:
            trust_score -= 5
            risk_indicators.append("Unusually large file - may contain hidden data")
        else:
            trust_indicators.append("Normal file size")

        # ─── Aspect Ratio Analysis ────────────────────────────────────────
        aspect_ratio = width / max(height, 1)
        analysis_details["aspect_ratio"] = round(aspect_ratio, 2)

        if aspect_ratio > 5 or aspect_ratio < 0.2:
            trust_score -= 10
            risk_indicators.append("Unusual aspect ratio - may be manipulated")

        # ─── Color Analysis ───────────────────────────────────────────────
        if img.mode == "RGBA":
            trust_indicators.append("Has transparency layer (common for logos)")
            trust_score += 5
        elif img.mode == "L":
            risk_indicators.append("Grayscale image - may be a photocopy or scan")

        # ─── Format Analysis ──────────────────────────────────────────────
        if img_format in ["PNG", "SVG"]:
            trust_indicators.append(f"Professional format ({img_format})")
            trust_score += 5
        elif img_format == "JPEG":
            trust_indicators.append("Standard JPEG format")

        # ─── Filename Analysis ────────────────────────────────────────────
        filename_lower = filename.lower()
        suspicious_names = ["screenshot", "whatsapp", "telegram", "received",
                           "img_", "photo_", "image_"]
        for name in suspicious_names:
            if name in filename_lower:
                trust_score -= 10
                risk_indicators.append(f"Filename suggests informal source: '{name}'")
                break

        if re.search(r"offer.*letter|appointment|joining", filename_lower):
            analysis_details["document_type"] = "Offer/Appointment Letter"
            trust_indicators.append("Filename suggests official document")

        # ─── Metadata Check ───────────────────────────────────────────────
        exif_data = {}
        try:
            if hasattr(img, '_getexif') and img._getexif():
                exif_data = img._getexif()
                trust_indicators.append("Contains EXIF metadata")
                trust_score += 5
        except Exception:
            pass

        if not exif_data:
            risk_indicators.append("No metadata found - may have been stripped")

        # ─── Uniform Color Detection (blank/fake) ─────────────────────────
        try:
            colors = img.getcolors(maxcolors=100)
            if colors and len(colors) < 5:
                trust_score -= 15
                risk_indicators.append("Very few colors detected - may be fabricated")
            elif colors and len(colors) > 50:
                trust_indicators.append("Rich color palette - appears to be genuine image")
                trust_score += 5
        except Exception:
            pass

        # Clamp score
        trust_score = max(0, min(100, trust_score))

        # Verdict
        if trust_score >= 70:
            verdict = "Likely Authentic"
        elif trust_score >= 45:
            verdict = "Uncertain - Manual Review Recommended"
        elif trust_score >= 25:
            verdict = "Suspicious - Possible Manipulation"
        else:
            verdict = "Likely Fake or Manipulated"

        return {
            "filename": filename,
            "file_size_kb": round(file_size_kb, 2),
            "dimensions": f"{width}x{height}",
            "format": img_format,
            "trust_score": trust_score,
            "risk_indicators": risk_indicators,
            "trust_indicators": trust_indicators,
            "verdict": verdict,
            "analysis_details": analysis_details
        }


image_analyzer = ImageAnalyzer()


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze an uploaded image/logo/document for authenticity"""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: JPEG, PNG, GIF, WebP, BMP"
        )

    # Read file (limit to 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")

    results = image_analyzer.analyze_image(contents, file.filename)
    return ImageAnalysisResponse(**results)
