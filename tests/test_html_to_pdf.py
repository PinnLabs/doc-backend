import io

from fastapi.testclient import TestClient
from pdfminer.high_level import extract_text

from app.services.html_to_pdf import HTMLToPDFConverter
from main import app

client = TestClient(app)


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extracts readable text from a PDF byte stream for test assertions."""
    with io.BytesIO(pdf_bytes) as pdf_file:
        return extract_text(pdf_file)


def test_html_to_pdf_basic_conversion():
    html = "<h1>Hello World</h1><p>This is a PDF test.</p>"
    converter = HTMLToPDFConverter()
    pdf_bytes = converter.convert(html)

    extracted = extract_pdf_text(pdf_bytes)
    assert "Hello World" in extracted
    assert "This is a PDF test." in extracted


def test_html_to_pdf_removes_script_tags():
    html = "<script>alert('XSS')</script><p>Content</p>"
    converter = HTMLToPDFConverter()
    pdf_bytes = converter.convert(html)

    extracted = extract_pdf_text(pdf_bytes)
    assert "alert" not in extracted
    assert "Content" in extracted


def test_html_to_pdf_with_custom_css():
    html = "<p class='highlight'>Styled paragraph</p>"
    css = ".highlight { color: red; }"
    converter = HTMLToPDFConverter(default_css=css)
    pdf_bytes = converter.convert(html)

    extracted = extract_pdf_text(pdf_bytes)
    assert "Styled paragraph" in extracted


def test_convert_html_file_to_pdf(client):
    html_content = b"<h2>Title</h2><p>PDF paragraph.</p>"
    file = io.BytesIO(html_content)

    response = client.post(
        "/api/v1/html/convert-to-pdf/",
        files={"file": ("example.html", file, "text/html")},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert response.content[:4] == b"%PDF"

    extracted = extract_pdf_text(response.content)
    assert "Title" in extracted
    assert "PDF paragraph." in extracted


def test_convert_html_with_script_is_sanitized(client):
    html_content = b"<script>evil()</script><p>Safe content</p>"
    file = io.BytesIO(html_content)

    response = client.post(
        "/api/v1/html/convert-to-pdf/",
        files={"file": ("scripted.html", file, "text/html")},
    )

    assert response.status_code == 200

    extracted = extract_pdf_text(response.content)
    assert "Safe content" in extracted
    assert "evil" not in extracted
    assert "script" not in extracted
