import io

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.services.auth_service import get_current_user
from app.services.pdf_to_html import PDFToHTMLConverter
from app.services.pdf_to_markdown import PDFToMarkdownConverter
from app.services.supabase_service import check_and_increment_usage

router = APIRouter(prefix="/api/v1/pdf", tags=["PDF"])


@router.post("/convert-to-markdown/")
async def convert_pdf_to_markdown(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    check_and_increment_usage(user["sub"])
    pdf_bytes = await file.read()

    converter = PDFToMarkdownConverter()
    markdown_text = converter.convert(pdf_bytes)

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    return PlainTextResponse(
        content=markdown_text,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}.md"'},
    )


@router.post("/convert-to-html/")
async def convert_pdf_to_html(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    check_and_increment_usage(user["sub"])
    pdf_bytes = await file.read()
    converter = PDFToHTMLConverter()
    html_output = converter.convert(pdf_bytes)

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    return StreamingResponse(
        content=io.BytesIO(html_output.encode("utf-8")),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}.html"'},
    )
