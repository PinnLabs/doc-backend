import io

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from app.services.auth_service import get_current_user
from app.services.markdown_to_html import MarkdownHTMLConverter
from app.services.markdown_to_pdf import MarkdownPDFConverter
from app.services.supabase_service import check_and_increment_usage

router = APIRouter(prefix="/api/v1/markdown", tags=["Markdown"])


@router.post("/convert-to-pdf/")
async def convert_markdown_to_pdf(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    check_and_increment_usage(user["sub"])
    markdown_content = await file.read()
    converter = MarkdownPDFConverter()
    pdf_bytes = converter.convert(markdown_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}.pdf"'},
    )


@router.post("/convert-to-html/")
async def convert_markdown_to_html(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    check_and_increment_usage(user["sub"])
    markdown_content = await file.read()
    converter = MarkdownHTMLConverter()
    html = converter.convert(markdown_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    return StreamingResponse(
        io.BytesIO(html.encode("utf-8")),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}.html"'},
    )
