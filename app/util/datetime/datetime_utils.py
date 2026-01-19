from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.middleware.timezone import request_timezone


def ensure_utc(dt: datetime) -> datetime:
    """Ensure datetime is UTC-aware"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_client_timezone(dt: datetime) -> datetime:
    """Convert UTC datetime to client timezone"""
    if not dt:
        return dt

    tz = request_timezone.get()
    client_tz = ZoneInfo(tz)

    return ensure_utc(dt).astimezone(client_tz)
