import fitz


class PDFToHTMLConverter:
    def __init__(self):
        pass

    def convert(self, pdf_bytes: bytes) -> str:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        custom_css = """
        body {
          font-family: "Helvetica", "Arial", sans-serif;
          font-size: 12pt;
          line-height: 1.6;
          margin: 2cm;
          color: #333;
        }

        h1, h2, h3 {
          color: #2c3e50;
        }

        code, pre {
          background: #f4f4f4;
          padding: 0.2em 0.4em;
          border-radius: 4px;
          font-family: "Courier New", Courier, monospace;
        }

        table {
          width: 100%;
          border-collapse: collapse;
        }

        table, th, td {
          border: 1px solid #ddd;
          padding: 8px;
        }
        """

        html_parts = [
            "<html><head><meta charset='utf-8'>",
            f"<style>{custom_css}</style>",
            "</head><body>",
        ]

        for page in doc:
            page_html = page.get_text("html")
            html_parts.append(page_html)

        html_parts.append("</body></html>")
        return "\n".join(html_parts)
