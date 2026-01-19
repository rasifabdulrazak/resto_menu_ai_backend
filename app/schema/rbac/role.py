from datetime import datetime
from pydantic import BaseModel
from app.schema.base import BaseSchema


class RoleCreate(BaseModel):
    name: str
    code: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None


class RoleResponse(BaseSchema):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
