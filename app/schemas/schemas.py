from pydantic import BaseModel


class MarkdownInput(BaseModel):
    markdown: str


class HTMLResponse(BaseModel):
    html: str
