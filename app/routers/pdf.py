import io

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from app.services.auth_service import get_current_user
from app.services.pdf_to_html import PDFToHTMLConverter
from app.services.pdf_to_markdown import PDFToMarkdownConverter
from app.services.supabase_service import (
    check_and_increment_usage,
    store_converted_document,
)

router = APIRouter(prefix="/api/v1/pdf", tags=["PDF"])


@router.post("/convert-to-markdown/")
async def convert_pdf_to_markdown(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    plan_name = check_and_increment_usage(user["sub"])
    pdf_bytes = await file.read()

    converter = PDFToMarkdownConverter()
    markdown_text = await converter.convert(pdf_bytes)
    markdown_bytes = markdown_text.encode("utf-8")
    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    store_converted_document(
        uid=user["sub"],
        file_bytes=markdown_bytes,
        original_filename=filename,
        target_extension="md",
        source_type="pdf",
        target_type="pdf-to-markdown",
        plan_name=plan_name,
    )

    return StreamingResponse(
        content=io.BytesIO(markdown_bytes),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}.md"'},
    )


@router.post("/convert-to-html/")
async def convert_pdf_to_html(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    plan_name = check_and_increment_usage(user["sub"])
    pdf_bytes = await file.read()

    converter = PDFToHTMLConverter()
    html_output = await converter.convert(pdf_bytes)
    html_bytes = html_output.encode("utf-8")
    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    store_converted_document(
        uid=user["sub"],
        file_bytes=html_bytes,
        original_filename=filename,
        target_extension="html",
        source_type="pdf",
        target_type="pdf-to-html",
        plan_name=plan_name,
    )

    return StreamingResponse(
        content=io.BytesIO(html_bytes),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}.html"'},
    )
