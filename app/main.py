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
from app.middleware.timezone import TimezoneMiddleware
from app.i18n.translator import translate
from app.middleware.locale import LocaleMiddleware
from fastapi import Depends
from app.dependencies.header import TimezoneHeader, LanguageHeader
from app.api.v1.rbac.role import router as role_router





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

    # Ensure components
    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault("securitySchemes", {})

    # -------------------------
    # Bearer Auth
    # -------------------------
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    # -------------------------
    # Timezone (API Key Header)
    # -------------------------
    openapi_schema["components"]["securitySchemes"]["TimezoneHeader"] = {
        "type": "apiKey",
        "in": "header",
        "name": "X-Timezone",
        "description": "Client timezone (IANA format, e.g. Asia/Kolkata)",
    }

    # -------------------------
    # Locale (API Key Header)
    # -------------------------
    openapi_schema["components"]["securitySchemes"]["LocaleHeader"] = {
        "type": "apiKey",
        "in": "header",
        "name": "Accept-Language",
        "description": "Response language (e.g. en, en-IN, ar)",
    }

    # -------------------------
    # Apply globally (THIS IS KEY)
    # -------------------------
    openapi_schema["security"] = [
        {"BearerAuth": []},
        {"TimezoneHeader": []},
        {"LocaleHeader": []},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.add_middleware(TimezoneMiddleware)
app.add_middleware(LocaleMiddleware)


@app.get("/health", tags=["Health"])
async def health_check():
        return {
            "status": "success",
            "message":translate("health.success"),
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }
        
app.include_router(role_router)