from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request

from app.core.config import Settings

settings = Settings()


def create_session_token(user_data: dict) -> str:
    payload = {
        "sub": user_data["uid"],
        "email": user_data["email"],
        "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_SECONDS),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_session_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request):
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return verify_session_token(token)
