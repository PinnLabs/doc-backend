import io

from fastapi.testclient import TestClient
from pdfminer.high_level import extract_text

from app.services.html_to_pdf import HTMLToPDFConverter
from main import app

client = TestClient(app)


def extract_pdf_text(pdf_bytes: bytes) -> str:
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
