from datetime import datetime, timedelta

from fastapi import HTTPException
from supabase import Client, create_client

from app.core.config import Settings

settings = Settings()

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def check_and_increment_usage(uid: str):
    user_res = (
        supabase.from_("users").select("*, plan(*)").eq("uid", uid).single().execute()
    )
    user = user_res.data

    now = datetime.utcnow()
    last_reset = datetime.fromisoformat(user["last_conversion_reset"])

    # Reset monthly counter if needed
    if now - last_reset > timedelta(days=30):
        user["conversions_this_month"] = 0
        user["last_conversion_reset"] = now.isoformat()

    plan = user["plan"]
    limit = plan["conversion_limit"]

    if limit is not None and user["conversions_this_month"] >= limit:
        raise HTTPException(status_code=403, detail="Monthly conversion limit reached")

    # Update usage
    supabase.from_("users").update(
        {
            "conversions_this_month": user["conversions_this_month"] + 1,
            "last_conversion_reset": user["last_conversion_reset"],
        }
    ).eq("uid", uid).execute()
