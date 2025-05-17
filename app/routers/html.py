import io

from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.services.auth_service import get_current_user
from app.services.html_to_markdown import HTMLToMarkdownConverter
from app.services.html_to_pdf import HTMLToPDFConverter
from app.services.supabase_service import (
    check_and_increment_usage,
    store_converted_document,
)

router = APIRouter(prefix="/api/v1/html", tags=["HTML"])


@router.post("/convert-to-md/")
async def convert_html_to_markdown(
    file: UploadFile = File(...),
    keep_styles: bool = Query(
        default=False, description="Preserve inline styles as-is"
    ),
    user=Depends(get_current_user),
):
    plan_name = check_and_increment_usage(user["sub"])
    html_content = await file.read()
    converter = HTMLToMarkdownConverter(keep_styles=keep_styles)
    markdown_text = converter.convert(html_content.decode())
    markdown_bytes = markdown_text.encode("utf-8")

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    store_converted_document(
        uid=user["sub"],
        file_bytes=markdown_bytes,
        original_filename=filename,
        target_extension="md",
        source_type="html",
        target_type="html-to-markdown",
        plan_name=plan_name,
    )

    return StreamingResponse(
        io.BytesIO(markdown_bytes),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}.md"'},
    )


@router.post("/convert-to-pdf/")
async def convert_html_to_pdf(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    plan_name = check_and_increment_usage(user["sub"])
    html_content = await file.read()
    converter = HTMLToPDFConverter()
    pdf_bytes = converter.convert(html_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    store_converted_document(
        uid=user["sub"],
        file_bytes=pdf_bytes,
        original_filename=filename,
        target_extension="pdf",
        source_type="html",
        target_type="html-to-pdf",
        plan_name=plan_name,
    )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}.pdf"'},
    )
