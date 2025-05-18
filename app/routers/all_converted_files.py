from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.services.auth_service import get_current_user
from app.services.supabase_service import list_user_documents, supabase

router = APIRouter()


@router.get("/api/v1/documents/")
async def get_user_documents(user=Depends(get_current_user)):
    docs = list_user_documents(user["sub"])
    return docs


@router.get("/api/v1/files/{filename:path}")
async def get_signed_download_url(filename: str, user=Depends(get_current_user)):
    bucket = "converted-files"

    res = (
        supabase.from_("documents")
        .select("*")
        .eq("file_path", filename)
        .eq("user_id", user["sub"])
        .limit(1)
        .execute()
    )

    if not res.data:
        raise HTTPException(
            status_code=404, detail="Arquivo não encontrado ou acesso negado"
        )

    signed_url_res = supabase.storage.from_(bucket).create_signed_url(filename, 60)

    if not signed_url_res.get("signedURL"):
        raise HTTPException(status_code=500, detail="Erro ao gerar link de download")

    return RedirectResponse(url=signed_url_res["signedURL"])
