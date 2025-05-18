import stripe
from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.services.auth_service import get_current_user
from app.services.supabase_service import supabase

router = APIRouter(prefix="/api/v1", tags=["Billing"])
settings = Settings()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.get("/subscription")
def get_subscription(user=Depends(get_current_user)):
    # Buscar dados do usuário no Supabase
    user_data = (
        supabase.table("users")
        .select("*")
        .eq("uid", user["sub"])
        .single()
        .execute()
        .data
    )
    if not user_data:
        return {"plan": "free", "subscription_status": "none", "payments": []}

    # Se tiver stripe_customer_id, buscar invoices
    payments = []
    if user_data.get("stripe_customer_id"):
        invoices = stripe.Invoice.list(
            customer=user_data["stripe_customer_id"], limit=10
        )
        payments = [
            {
                "id": inv.id,
                "amount_paid": inv.amount_paid / 100,
                "currency": inv.currency.upper(),
                "status": inv.status,
                "date": inv.created,
            }
            for inv in invoices.data
        ]

    return {
        "plan": user_data.get("plan", "free"),
        "subscription_status": user_data.get("subscription_status", "none"),
        "current_period_end": user_data.get("current_period_end"),
        "payments": payments,
    }
