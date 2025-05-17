import asyncio
import tempfile
import uuid
import os


class PDFToHTMLConverter:
    async def convert(self, pdf_bytes: bytes) -> str:
        with tempfile.TemporaryDirectory() as tmp_dir:
            unique_id = str(uuid.uuid4())
            input_filename = f"{unique_id}.pdf"
            output_filename = f"{unique_id}.html"
            input_path = os.path.join(tmp_dir, input_filename)

            with open(input_path, "wb") as f:
                f.write(pdf_bytes)

            process = await asyncio.create_subprocess_exec(
                "pdf2htmlEX",
                "--embed-css",
                "1",
                "--embed-image",
                "1",
                "--embed-font",
                "1",
                "--optimize-text",
                "1",
                "--zoom",
                "1.3",
                input_filename,
                output_filename,
                cwd=tmp_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"Erro na conversão do PDF: {stderr.decode()}")

            output_path = os.path.join(tmp_dir, output_filename)

            with open(output_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        return html_content
