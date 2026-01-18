import time
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine
from contextvars import ContextVar

query_count_ctx: ContextVar[int] = ContextVar("query_count", default=0)
query_time_ctx: ContextVar[float] = ContextVar("query_time", default=0.0)


def reset_query_stats():
    query_count_ctx.set(0)
    query_time_ctx.set(0.0)


def get_query_stats():
    return {
        "count": query_count_ctx.get(),
        "time_ms": round(query_time_ctx.get() * 1000, 2),
    }


def setup_db_profiling(engine: AsyncEngine):
    @event.listens_for(engine.sync_engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        context._query_start_time = time.perf_counter()

    @event.listens_for(engine.sync_engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        duration = time.perf_counter() - context._query_start_time
        query_count_ctx.set(query_count_ctx.get() + 1)
        query_time_ctx.set(query_time_ctx.get() + duration)
