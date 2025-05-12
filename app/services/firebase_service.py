from fastapi import HTTPException
from firebase_admin import auth as firebase_auth


def verify_firebase_token(id_token: str) -> dict:
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
