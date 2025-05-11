import os

from jinja2 import Template
from markdown_it import MarkdownIt


class MarkdownHTMLConverter:
    def __init__(self, css_path: str = "app/templates/default_html.css"):
        self.md_parser = MarkdownIt("gfm-like")
        self.css = self._load_css(css_path)

    def _load_css(self, path: str) -> str:
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
        return ""

    def convert(self, markdown_text: str) -> str:
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
