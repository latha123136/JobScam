"""
Authentication API Routes
User registration, login, and profile management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime
from database.connection import users_collection
from auth.jwt_handler import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter()
security = HTTPBearer()


# ─── Schemas ───────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str


# ─── Helper ────────────────────────────────────────────────────────────────────

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract current user from JWT token"""
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await users_collection.find_one({"email": payload.get("sub")})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ─── Routes ────────────────────────────────────────────────────────────────────

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """Register a new user"""
    # Check if user exists
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user document
    user_doc = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": "user",
        "created_at": datetime.utcnow().isoformat(),
        "scan_count": 0,
        "scams_detected": 0
    }

    result = await users_collection.insert_one(user_doc)

    # Generate token
    token = create_access_token(data={"sub": user.email})

    return {
        "message": "Registration successful",
        "token": token,
        "user": {
            "id": str(result.inserted_id),
            "name": user.name,
            "email": user.email,
            "role": "user"
        }
    }


@router.post("/login")
async def login(user: UserLogin):
    """Authenticate user and return JWT token"""
    # Find user
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate token
    token = create_access_token(data={"sub": user.email})

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(db_user["_id"]),
            "name": db_user["name"],
            "email": db_user["email"],
            "role": db_user["role"]
        }
    }


@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "scan_count": current_user.get("scan_count", 0),
        "scams_detected": current_user.get("scams_detected", 0),
        "created_at": current_user.get("created_at", "")
    }
