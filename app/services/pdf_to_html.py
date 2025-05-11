import fitz  # PyMuPDF
from html import escape


class PDFToHTMLConverter:
    def __init__(self):
        pass

    def convert(self, pdf_bytes: bytes) -> str:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        html_parts = [
            "<html><head><meta charset='utf-8'><style>div.page { position: relative; width: 100%; height: auto; } .text { position: absolute; white-space: pre; }</style></head><body>"
        ]

        for page_num, page in enumerate(doc):
            text_blocks = page.get_text("dict")["blocks"]
            page_html = '<div class="page">'
            for block in text_blocks:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        x = span["bbox"][0]
                        y = span["bbox"][1]
                        font_size = span["size"]
                        color = "#{:06x}".format(span["color"])
                        font = span["font"]

                        page_html += (
                            f'<div class="text" '
                            f'style="left:{x}px; top:{y}px; '
                            f'font-size:{font_size}px; color:{color}; font-family:{font};">'
                            f"{escape(span['text'])}</div>"
                        )
            page_html += "</div>"
            html_parts.append(page_html)

        html_parts.append("</body></html>")
        return "\n".join(html_parts)
