from bs4 import BeautifulSoup
from weasyprint import CSS, HTML


class HTMLToPDFConverter:
    def __init__(self, default_css: str = ""):
        self.default_css = default_css

    def _sanitize_html(self, html_text: str) -> str:
        """
        Clean the HTML and optionally remove unsupported elements like <script>.
        """
        soup = BeautifulSoup(html_text, "html.parser")

        for script in soup(["script"]):
            script.decompose()

        return str(soup)

    def convert(self, html_text: str) -> bytes:
        sanitized_html = self._sanitize_html(html_text)
        html_obj = HTML(string=sanitized_html)

        if self.default_css:
            css_obj = CSS(string=self.default_css)
            return html_obj.write_pdf(stylesheets=[css_obj])
        return html_obj.write_pdf()
