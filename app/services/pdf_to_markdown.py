import io

from pdfminer.high_level import extract_text


class PDFToMarkdownConverter:
    def __init__(self):
        pass  # Reserved for future config (e.g. custom sanitization, formatting)

    def convert(self, pdf_bytes: bytes) -> str:
        """
        Convert raw PDF bytes into a markdown-friendly plain text structure.
        """
        text = self._extract_text(pdf_bytes)
        markdown = self._format_as_markdown(text)
        return markdown

    def _extract_text(self, pdf_bytes: bytes) -> str:
        with io.BytesIO(pdf_bytes) as pdf_file:
            return extract_text(pdf_file)

    def _format_as_markdown(self, text: str) -> str:
        # Naive formatting: Replace multiple newlines with double newline
        # (basic paragraph split). You can improve this as needed.
        cleaned = "\n\n".join(
            [line.strip() for line in text.splitlines() if line.strip()]
        )
        return cleaned
