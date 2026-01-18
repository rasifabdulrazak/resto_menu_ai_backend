from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from app.core.debug.db_profiler import reset_query_stats, get_query_stats
from app.core.config import settings


class DebugToolbarMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if settings.ENVIRONMENT != "development":
            return await call_next(request)

        reset_query_stats()
        response: Response = await call_next(request)

        stats = get_query_stats()

        # Add debug headers (like Django toolbar)
        response.headers["X-DB-Query-Count"] = str(stats["count"])
        response.headers["X-DB-Query-Time-ms"] = str(stats["time_ms"])

        return response
