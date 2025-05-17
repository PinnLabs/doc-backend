import io
import tempfile

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.services.auth_service import get_current_user
from app.services.pdf_to_html import PDFtoHTMLConverter
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
    markdown_text = converter.convert(pdf_bytes)
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

    # Salvar PDF em um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf_bytes = await file.read()
        tmp_pdf.write(pdf_bytes)
        tmp_pdf_path = tmp_pdf.name

    # Inicializar e converter
    converter = PDFtoHTMLConverter()
    html_path = converter.convert(tmp_pdf_path)

    # Ler HTML gerado
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    html_bytes = html_content.encode("utf-8")
    filename = file.filename.rsplit(".", 1)[0] if file.filename else "document"

    # Armazenar
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
