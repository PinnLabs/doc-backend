import io

from fastapi.testclient import TestClient

from app.services.html_to_markdown import HTMLToMarkdownConverter
from main import app

client = TestClient(app)


def test_basic_html_conversion():
    html = "<h1>Hello</h1><p>This is a test.</p>"
    converter = HTMLToMarkdownConverter()
    md = converter.convert(html)
    assert "# Hello" in md
    assert "This is a test." in md


def test_removes_inline_styles_by_default():
    html = '<p style="color: red;">Styled text</p>'
    converter = HTMLToMarkdownConverter()
    cleaned = converter.convert(html)
    assert "style=" not in cleaned
    assert "Styled text" in cleaned


def test_preserves_inline_styles_if_configured():
    html = '<p style="color: red;">Styled text</p>'
    converter = HTMLToMarkdownConverter(keep_styles=True)
    cleaned = converter.convert(html)
    assert "style=" in cleaned or "Styled text" in cleaned


def test_removes_style_tags():
    html = "<style>p {color: red;}</style><p>Text</p>"
    converter = HTMLToMarkdownConverter()
    markdown = converter.convert(html)
    assert "Text" in markdown
    assert "style" not in markdown
