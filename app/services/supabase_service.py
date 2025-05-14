from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from supabase import Client, create_client

from app.core.config import Settings

settings = Settings()

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

PLAN_EXPIRATION_DAYS = {
    "Free": 1,
    "Starter": 7,
    "Pro": 30,
    "Unlimited": None,
}


def get_expiration_date(plan_name: str) -> Optional[str]:
    days = PLAN_EXPIRATION_DAYS.get(plan_name)
    if days is None:
        return None
    expires_at = datetime.utcnow() + timedelta(days=days)
    return expires_at.isoformat()


def store_converted_document(
    uid: str,
    file_bytes: bytes,
    original_filename: str,
    target_extension: str,
    source_type: str,
    target_type: str,
    plan_name: str,
) -> str:
    filename_base = (
        original_filename.rsplit(".", 1)[0]
        if "." in original_filename
        else original_filename
    )
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{uid}/{filename_base}_{timestamp}.{target_extension}"
    bucket = "converted-files"

    supabase.storage.from_(bucket).upload(
        path=filename,
        file=file_bytes,
        file_options={"content-type": _guess_content_type(target_extension)},
    )

    expires_at = get_expiration_date(plan_name)

    supabase.from_("documents").insert(
        {
            "user_id": uid,
            "file_path": filename,
            "original_filename": original_filename,
            "source_type": source_type,
            "target_type": target_type,
            "expires_at": expires_at,
        }
    ).execute()

    return filename


def _guess_content_type(extension: str) -> str:
    return {
        "pdf": "application/pdf",
        "html": "text/html",
        "md": "text/markdown",
    }.get(extension.lower(), "application/octet-stream")


def check_and_increment_usage(uid: str) -> str:
    user_res = (
        supabase.from_("users")
        .select("*, plans!fk_plan(*)")
        .eq("uid", uid)
        .single()
        .execute()
    )
    user = user_res.data

    now = datetime.utcnow()
    last_reset = datetime.fromisoformat(user["last_conversion_reset"])

    if now - last_reset > timedelta(days=30):
        user["conversions_this_month"] = 0
        user["last_conversion_reset"] = now.isoformat()

    plan = user["plans"]
    limit = plan["conversion_limit"]

    if limit is not None and user["conversions_this_month"] >= limit:
        raise HTTPException(status_code=403, detail="Monthly conversion limit reached")

    supabase.from_("users").update(
        {
            "conversions_this_month": user["conversions_this_month"] + 1,
            "last_conversion_reset": user["last_conversion_reset"],
        }
    ).eq("uid", uid).execute()

    return plan["name"]
