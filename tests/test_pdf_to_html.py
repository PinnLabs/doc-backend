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
