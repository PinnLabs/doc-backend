import os
import subprocess
from pathlib import Path


class PDFtoHTMLConverter:
    def __init__(self, pdf2htmlex_path: str = "pdf2htmlEX"):
        self.pdf2htmlex_path = pdf2htmlex_path

    def convert(self, pdf_input_path: str, html_output_path: str = None) -> str:
        """
        Converte um arquivo PDF em HTML com alta fidelidade, preservando layout, fontes e estilos.

        :param pdf_input_path: Caminho absoluto ou relativo para o arquivo PDF de entrada.
        :param html_output_path: Caminho do arquivo HTML de saída (opcional). Se não for passado, será no mesmo diretório com extensão .html.
        :return: Caminho do arquivo HTML gerado.
        :raises FileNotFoundError: Se o arquivo PDF não existir.
        :raises RuntimeError: Se a conversão falhar.
        """
        input_path = Path(pdf_input_path).resolve()

        if not input_path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {input_path}")

        output_path = (
            Path(html_output_path).resolve()
            if html_output_path
            else input_path.with_suffix(".html")
        )

        try:
            command = [
                self.pdf2htmlex_path,
                "--embed-css",
                "1",
                "--embed-font",
                "1",
                "--embed-image",
                "1",
                "--embed-javascript",
                "1",
                "--zoom",
                "1.3",
                "--dest-dir",
                str(output_path.parent),
                str(input_path),
            ]

            subprocess.run(command, check=True)

            return str(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro ao converter PDF para HTML: {e}")
