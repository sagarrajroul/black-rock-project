from fastapi import FastAPI
from .routers import api_router

def create_app():
    app = FastAPI(app_name="FastAPI app for Black Rock", version="1.0.0")
    app.include_router(api_router, prefix="/api/blackrock/challenge/v1")
    return app
app = create_app()
