from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.services.auth_service import get_current_user
from app.services.supabase_service import supabase

router = APIRouter(prefix="/api/v1", tags=["Dashboard"])


@router.get("/me/usage")
async def get_user_usage(user_data=Depends(get_current_user)):
    uid = user_data.get("sub")
    if not uid:
        raise HTTPException(
            status_code=401, detail="Invalid session token: UID missing"
        )

    total_res = (
        supabase.from_("documents")
        .select("id", count="exact")
        .eq("user_id", uid)
        .execute()
    )
    total_conversions = total_res.count or 0

    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1).isoformat()

    month_res = (
        supabase.from_("documents")
        .select("id", count="exact")
        .eq("user_id", uid)
        .gte("created_at", month_start)
        .execute()
    )
    conversions_this_month = month_res.count or 0

    user_res = (
        supabase.from_("users")
        .select("plans!fk_plan(conversion_limit)")
        .eq("uid", uid)
        .single()
        .execute()
    )

    if not user_res.data:
        raise HTTPException(status_code=404, detail="User not found")

    plan_limit = user_res.data["plans"]["conversion_limit"]

    return {
        "used_total": total_conversions,
        "used_this_month": conversions_this_month,
        "limit": plan_limit,
    }
