import io

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.services.pdf_to_markdown import PDFToMarkdownConverter
from main import app

client = TestClient(app)


def generate_pdf(text: str) -> bytes:
    """Generate a simple PDF with ReportLab."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    for i, line in enumerate(text.splitlines()):
        c.drawString(100, 800 - i * 15, line)
    c.save()
    buffer.seek(0)
    return buffer.read()


def test_pdf_to_markdown_basic_extraction():
    text = "Hello PDF\nThis is a test."
    pdf_bytes = generate_pdf(text)
    converter = PDFToMarkdownConverter()
    markdown = converter.convert(pdf_bytes)

    assert "Hello PDF" in markdown
    assert "This is a test." in markdown


def test_pdf_to_markdown_removes_blank_lines():
    text = "Line 1\n\n\nLine 2"
    pdf_bytes = generate_pdf(text)
    converter = PDFToMarkdownConverter()
    markdown = converter.convert(pdf_bytes)

    assert markdown.count("Line 1") == 1
    assert markdown.count("Line 2") == 1
    assert markdown.count("\n\n") == 1  # Paragraph split


def test_convert_pdf_to_markdown_endpoint():
    text = "FastAPI PDF\nIntegration Test"
    pdf_bytes = generate_pdf(text)
    file = io.BytesIO(pdf_bytes)

    response = client.post(
        "/api/v1/markdown/convert-pdf-to-markdown/",
        files={"file": ("sample.pdf", file, "application/pdf")},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/markdown")
    assert "FastAPI PDF" in response.text
    assert "Integration Test" in response.text
