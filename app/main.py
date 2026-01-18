from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "success",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }