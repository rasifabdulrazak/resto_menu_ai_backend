from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.cors import setup_cors
from app.core.exception import setup_exception_handlers
from app.core.lifespan import lifespan

from app.db.session import engine
from app.core.debug.db_profiler import setup_db_profiling
from app.middleware.debug_toolbar import DebugToolbarMiddleware
from fastapi.openapi.utils import get_openapi


def create_app() -> FastAPI:
    setup_logging(settings.DEBUG)

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        swagger_ui_parameters={
        "persistAuthorization": True,  # THIS IS THE KEY
    },
    )

    # DB profiling (DEV only)
    if settings.ENVIRONMENT == "development":
        setup_db_profiling(engine)
        app.add_middleware(DebugToolbarMiddleware)
    # Middlewares
    setup_cors(app)

    # Exception handlers
    setup_exception_handlers(app)

    # Health check
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "success",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    return app




app = create_app()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Resto Menu AI API",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi