from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from secure import SecureHeaders

from app.core.config import Settings
from app.routers import auth, billing, html, markdown, pdf, webhook

settings = Settings()
app = FastAPI()

secure_headers = SecureHeaders()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.starlette(response)
    return response


app.include_router(markdown.router)
app.include_router(pdf.router)
app.include_router(html.router)
app.include_router(auth.router)
app.include_router(billing.router)
app.include_router(webhook.router)
