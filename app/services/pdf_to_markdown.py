import os
import asyncio
import tempfile
from pdf2docx import Converter


class PDFToMarkdownConverter:
    def __init__(self):
        self.pandoc_cmd = "pandoc"

    async def convert(self, pdf_bytes: bytes) -> str:
        if not pdf_bytes.startswith(b"%PDF"):
            raise ValueError("O arquivo enviado não é um PDF válido.")
        return await self._convert_async(pdf_bytes)

    async def _convert_async(self, pdf_bytes: bytes) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, "input.pdf")
            docx_path = os.path.join(tmpdir, "output.docx")

            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)

            await asyncio.to_thread(self._convert_pdf_to_docx, pdf_path, docx_path)

            markdown = await self._convert_docx_to_md(docx_path)

            return markdown

    def _convert_pdf_to_docx(self, pdf_path: str, docx_path: str):
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"Arquivo DOCX não foi gerado em: {docx_path}")

    async def _convert_docx_to_md(self, docx_path: str) -> str:
        md_output_path = docx_path.replace(".docx", ".md")
        process = await asyncio.create_subprocess_exec(
            self.pandoc_cmd,
            docx_path,
            "-f",
            "docx",
            "-t",
            "gfm",  # GitHub-flavored Markdown
            "-o",
            md_output_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Pandoc conversion failed:\n{stderr.decode()}")

        if not os.path.exists(md_output_path):
            raise FileNotFoundError(f"Markdown não gerado: {md_output_path}")

        with open(md_output_path, "r", encoding="utf-8") as f:
            return f.read()
