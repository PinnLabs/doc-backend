from fastapi import APIRouter, Depends, HTTPException

from app.services.auth_service import get_current_user
from app.services.payment_service import create_checkout_session

router = APIRouter(prefix="/api/v1", tags=["Billing"])


@router.post("/create-checkout-session")
def checkout(plan: str, user=Depends(get_current_user)):
    try:
        url = create_checkout_session(uid=user["sub"], email=user["email"], plan=plan)
        return {"checkout_url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
