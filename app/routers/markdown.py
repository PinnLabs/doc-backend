import io

from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse, StreamingResponse

from app.services.html_to_markdown import HTMLToMarkdownConverter
from app.services.html_to_pdf import HTMLToPDFConverter
from app.services.markdown_to_html import MarkdownHTMLConverter
from app.services.markdown_to_pdf import MarkdownPDFConverter
from app.services.pdf_to_html import PDFToHTMLConverter
from app.services.pdf_to_markdown import PDFToMarkdownConverter

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


@router.post("/convert-to-md/")
async def convert_html_to_markdown(
    file: UploadFile = File(...),
    keep_styles: bool = Query(
        default=False, description="Preserve inline styles as-is"
    ),
):
    html_content = await file.read()
    converter = HTMLToMarkdownConverter(keep_styles=keep_styles)
    markdown_text = converter.convert(html_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"
    return PlainTextResponse(
        content=markdown_text,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}.md"'},
    )


@router.post("/convert-html-to-pdf/")
async def convert_html_to_pdf(file: UploadFile = File(...)):
    html_content = await file.read()
    converter = HTMLToPDFConverter()
    pdf_bytes = converter.convert(html_content.decode())

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}.pdf"'},
    )


@router.post("/convert-pdf-to-markdown/")
async def convert_pdf_to_markdown(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    converter = PDFToMarkdownConverter()
    markdown_text = converter.convert(pdf_bytes)

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    return PlainTextResponse(
        content=markdown_text,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}.md"'},
    )


@router.post("/convert-pdf-to-html/")
async def convert_pdf_to_html(file: UploadFile = File(...)):
    pdf_content = await file.read()
    converter = PDFToHTMLConverter()
    html_bytes = converter.convert(pdf_content)

    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"
    return StreamingResponse(
        io.BytesIO(html_bytes),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{filename}.html"'},
    )
