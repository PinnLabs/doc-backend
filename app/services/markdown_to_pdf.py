import os

from jinja2 import Template
from markdown_it import MarkdownIt
from weasyprint import HTML


class MarkdownPDFConverter:
    def __init__(self, css: str = ""):
        self.md_parser = MarkdownIt()
        self.css = css or self._load_default_css()

    def _load_default_css(self):
        path = "app/templates/default.css"
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
        return ""

    def markdown_to_html(self, markdown_text: str) -> str:
        body = self.md_parser.render(markdown_text)
        template = Template(
            """
            <html>
                <head>
                    <meta charset="utf-8">
                    <style>{{ css }}</style>
                </head>
                <body>{{ body | safe }}</body>
            </html>
            """
        )
        return template.render(body=body, css=self.css)

    def html_to_pdf(self, html: str) -> bytes:
        return HTML(string=html).write_pdf()

    def convert(self, markdown_text: str) -> bytes:
        html = self.markdown_to_html(markdown_text)
        return self.html_to_pdf(html)
