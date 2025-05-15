import stripe
from fastapi import APIRouter, Header, HTTPException, Request

from app.core.config import Settings
from app.services.supabase_service import supabase

router = APIRouter(prefix="/webhook", tags=["Stripe Webhook"])

settings = Settings()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]

        # Fetch subscription
        subscription = stripe.Subscription.retrieve(session["subscription"])
        price_id = subscription["items"]["data"][0]["price"]["id"]

        # Determine plan
        price_plan_map = {
            settings.STRIPE_PRICE_ID_STARTER: "starter",
            settings.STRIPE_PRICE_ID_PRO: "pro",
            settings.STRIPE_PRICE_ID_UNLIMITED: "unlimited",
        }
        plan = price_plan_map.get(price_id, "free")

        # Update Supabase user
        user = (
            supabase.table("users")
            .select("*")
            .eq("stripe_customer_id", customer_id)
            .single()
            .execute()
            .data
        )
        if user:
            supabase.table("users").update(
                {
                    "plan": plan,
                    "subscription_status": "active",
                    "current_period_end": subscription["current_period_end"],
                }
            ).eq("uid", user["uid"]).execute()

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]

        user = (
            supabase.table("users")
            .select("*")
            .eq("stripe_customer_id", customer_id)
            .single()
            .execute()
            .data
        )
        if user:
            supabase.table("users").update(
                {"plan": "free", "subscription_status": "canceled"}
            ).eq("uid", user["uid"]).execute()

    return {"status": "success"}
