from fastapi import FastAPI

from app.routers import markdown

app = FastAPI()

app.include_router(markdown.router)
