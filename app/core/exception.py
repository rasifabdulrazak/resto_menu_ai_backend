from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import asyncpg
import logging

from app.schema.common import APIResponse, ErrorSchema

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:

    # -------------------------
    # Database constraint errors
    # -------------------------
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.exception("Database integrity error")

        # Friendly, safe messages only
        if isinstance(exc.orig, asyncpg.UniqueViolationError):
            message = "Resource already exists"
            code = "RESOURCE_EXISTS"

        elif isinstance(exc.orig, asyncpg.NotNullViolationError):
            message = "Required field is missing"
            code = "REQUIRED_FIELD_MISSING"

        elif isinstance(exc.orig, asyncpg.ForeignKeyViolationError):
            message = "Invalid reference"
            code = "INVALID_REFERENCE"

        else:
            message = "Invalid data"
            code = "INVALID_DATA"

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=APIResponse(
                success=False,
                message=message,
                errors=ErrorSchema(code=code),
            ).model_dump(),
        )

    # -------------------------
    # HTTPException (404, 403)
    # -------------------------
    from fastapi import HTTPException

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=APIResponse(
                success=False,
                message=exc.detail if isinstance(exc.detail, str) else "Request failed",
                errors=ErrorSchema(code="HTTP_ERROR"),
            ).model_dump(),
        )

    # -------------------------
    # Catch-all (VERY IMPORTANT)
    # -------------------------
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled system error")

        # DO NOT expose details
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse(
                success=False,
                message="Internal server error",
                errors=ErrorSchema(code="INTERNAL_SERVER_ERROR"),
            ).model_dump(),
        )