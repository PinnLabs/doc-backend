from fastapi import FastAPI

from app.routers import auth, html, markdown, pdf

app = FastAPI()

app.include_router(markdown.router)
app.include_router(pdf.router)
app.include_router(html.router)
app.include_router(auth.router)
