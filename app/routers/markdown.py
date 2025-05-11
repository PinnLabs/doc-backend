import io

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from app.services.markdown_to_html import MarkdownHTMLConverter
from app.services.markdown_to_pdf import MarkdownPDFConverter

router = APIRouter(prefix="/api/v1/markdown", tags=["Markdown"])


@router.post("/convert-docs/")
async def convert_markdown_to_pdf(file: UploadFile = File(...)):
    markdown_content = await file.read()
    converter = MarkdownPDFConverter()
    pdf_bytes = converter.convert(markdown_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}.pdf"'},
    )


@router.post("/convert-html/")
async def convert_markdown_to_html(file: UploadFile = File(...)):
    markdown_content = await file.read()
    converter = MarkdownHTMLConverter()
    html = converter.convert(markdown_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    return StreamingResponse(
        io.BytesIO(html.encode("utf-8")),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}.html"'},
    )
