from fastapi import FastAPI

from app.routers import html, markdown, pdf

app = FastAPI()

app.include_router(markdown.router)
app.include_router(pdf.router)
app.include_router(html.router)
