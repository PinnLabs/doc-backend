import io
import subprocess
import tempfile
from pathlib import Path


class PDFToHTMLConverter:
    def convert(self, pdf_bytes: bytes) -> bytes:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.pdf"
            output_path = Path(tmpdir) / "output.html"

            input_path.write_bytes(pdf_bytes)

            result = subprocess.run(
                [
                    "pdf2htmlEX",
                    "--embed-css",
                    "1",
                    "--embed-image",
                    "1",
                    "--embed-font",
                    "1",
                    "--dest-dir",
                    tmpdir,
                    "--output",
                    str(output_path.name),
                    str(input_path),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            return output_path.read_bytes()
