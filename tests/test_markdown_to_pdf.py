import pytest

from app.services.markdown_to_pdf import MarkdownPDFConverter


def test_markdown_to_html_basic():
    converter = MarkdownPDFConverter()
    markdown = "# Hello World"
    html = converter.markdown_to_html(markdown)

    assert "<h1>Hello World</h1>" in html
    assert "<style>" in html  # CSS was injected
    assert "<html>" in html and "</html>" in html


def test_html_to_pdf_generation():
    converter = MarkdownPDFConverter()
    html = "<html><body><h1>Test</h1></body></html>"
    pdf = converter.html_to_pdf(html)

    assert isinstance(pdf, bytes)
    assert pdf[:5] == b"%PDF-"  # Valid PDF header


def test_markdown_to_pdf_conversion():
    converter = MarkdownPDFConverter()
    markdown = "# Title\n\nSome text."
    pdf = converter.convert(markdown)

    assert isinstance(pdf, bytes)
    assert pdf[:5] == b"%PDF-"
