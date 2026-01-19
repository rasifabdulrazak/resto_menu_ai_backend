from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from contextvars import ContextVar

# Request-scoped language
request_language: ContextVar[str] = ContextVar(
    "request_language",
    default="en"
)


class LocaleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        lang = request.headers.get("Accept-Language", "en")

        # Normalize: "en-IN,en;q=0.9" → "en-IN"
        lang = lang.split(",")[0].strip()

        request_language.set(lang)
        return await call_next(request)
