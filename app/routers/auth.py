from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.schemas.auth import LoginRequest
from app.services.auth_service import create_session_token, get_current_user
from app.services.firebase_service import verify_firebase_token
from app.services.supabase_service import supabase

router = APIRouter(prefix="/api/v1", tags=["Auth"])


@router.post("/login")
async def login(payload: LoginRequest, response: Response):
    firebase_user = verify_firebase_token(payload.idToken)
    session_token = create_session_token(firebase_user)

    uid = firebase_user["uid"]
    email = firebase_user["email"]

    existing = supabase.table("users").select("*").eq("uid", uid).execute()
    if not existing.data:
        supabase.table("users").insert(
            {"uid": uid, "email": email, "plan": "free"}
        ).execute()

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
        path="/",
    )
    return response


@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("session")
    return response


@router.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello, {user['email']}"}
