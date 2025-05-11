import io

import pytest
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.services.pdf_to_html import PDFToHTMLConverter
from main import app

client = TestClient(app)


@pytest.fixture
def sample_pdf_bytes():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Hello, World!")
    c.save()
    buffer.seek(0)
    return buffer.read()


def test_pdf_to_html_conversion_returns_html(sample_pdf_bytes):
    converter = PDFToHTMLConverter()
    html = converter.convert(sample_pdf_bytes)

    assert html.startswith("<html>")
    assert "</html>" in html
    assert "Hello, World!" in html


def test_pdf_to_html_endpoint(sample_pdf_bytes):
    response = client.post(
        "/api/v1/pdf/convert-to-html/",
        files={"file": ("sample.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
    )

    assert response.status_code == 200
    assert response.headers["content-disposition"].endswith('.html"')
    assert "<html>" in response.text
    assert "Hello, World!" in response.text
