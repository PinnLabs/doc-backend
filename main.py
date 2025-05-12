from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from secure import SecureHeaders

from app.routers import auth, html, markdown, pdf

app = FastAPI()

secure_headers = SecureHeaders()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
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
