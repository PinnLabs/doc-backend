import stripe

from app.core.config import Settings
from app.services.supabase_service import supabase

settings = Settings()
stripe.api_key = settings.STRIPE_SECRET_KEY


def get_or_create_customer(uid: str, email: str) -> str:
    user = supabase.table("users").select("*").eq("uid", uid).single().execute().data
    customer_id = user.get("stripe_customer_id")
    if customer_id:
        return customer_id

    customer = stripe.Customer.create(email=email)
    supabase.table("users").update({"stripe_customer_id": customer.id}).eq(
        "uid", uid
    ).execute()
    return customer.id


def create_checkout_session(uid: str, email: str, plan: str) -> str:
    customer_id = get_or_create_customer(uid, email)

    price_map = {
        "starter": settings.STRIPE_PRICE_ID_STARTER,
        "pro": settings.STRIPE_PRICE_ID_PRO,
        "unlimited": settings.STRIPE_PRICE_ID_UNLIMITED,
    }

    if plan not in price_map:
        raise ValueError("Invalid plan")

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_map[plan], "quantity": 1}],
        mode="subscription",
        success_url=f"{settings.FRONTEND_URL}/auth/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.FRONTEND_URL}/cancel",
    )

    return session.url


def create_guest_checkout_session(email: str, plan: str) -> str:
    customer = stripe.Customer.create(email=email)

    price_map = {
        "starter": settings.STRIPE_PRICE_ID_STARTER,
        "pro": settings.STRIPE_PRICE_ID_PRO,
        "unlimited": settings.STRIPE_PRICE_ID_UNLIMITED,
    }

    if plan not in price_map:
        raise ValueError("Invalid plan")

    session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        line_items=[{"price": price_map[plan], "quantity": 1}],
        mode="subscription",
        success_url=f"{settings.FRONTEND_URL}/auth/post-checkout?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.FRONTEND_URL}/cancel",
        metadata={"guest_email": email},
    )

    return session.url
