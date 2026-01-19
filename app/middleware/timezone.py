from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from zoneinfo import ZoneInfo
from contextvars import ContextVar

# Request-scoped timezone
request_timezone: ContextVar[str] = ContextVar(
    "request_timezone",
    default="UTC"
)


class TimezoneMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tz = request.headers.get("X-Timezone", "UTC")

        try:
            ZoneInfo(tz)  # validate
            request_timezone.set(tz)
        except Exception:
            request_timezone.set("UTC")

        response = await call_next(request)
        return response
