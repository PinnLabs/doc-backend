from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from secure import SecureHeaders

from app.core.config import Settings
from app.routers import (
    all_converted_files,
    auth,
    billing,
    dashboard,
    html,
    markdown,
    pdf,
    subscrition,
    webhook,
)

settings = Settings()
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    penapi_url=None,
)

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
app.include_router(dashboard.router)
app.include_router(all_converted_files.router)
app.include_router(subscrition.router)
