import logging

from bs4 import BeautifulSoup
from markdownify import markdownify as md

logger = logging.getLogger(__name__)


class HTMLToMarkdownConverter:
    def __init__(self, keep_styles: bool = False):
        """
        :param keep_styles: If True, will attempt to preserve inline styles as comments (or skip handling).
        """
        self.keep_styles = keep_styles

    def clean_html(self, html_text: str) -> str:
        soup = BeautifulSoup(html_text, "html.parser")

        # Log and optionally remove <style> tags
        for style_tag in soup.find_all("style"):
            logger.debug("Removing <style> tag with content: %s", style_tag.text[:100])
            style_tag.decompose()

        if not self.keep_styles:
            for tag in soup(True):  # All tags
                if "style" in tag.attrs:
                    logger.debug("Removing inline style from tag <%s>", tag.name)
                    del tag["style"]

        return str(soup)

    def convert(self, html_text: str) -> str:
        cleaned_html = self.clean_html(html_text)
        markdown = md(cleaned_html, heading_style="ATX")
        return markdown
