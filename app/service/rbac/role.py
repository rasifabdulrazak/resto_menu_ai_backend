from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.model.rbac.role import Role
from app.schema.rbac.role import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: RoleCreate) -> Role:
        role = Role(**payload.model_dump())
        self.db.add(role)

        try:
            await self.db.commit()
            await self.db.refresh(role)
            return role
        except Exception:
            await self.db.rollback()
            raise

    async def get(self, role_id: int) -> Role:
        role = await self.db.get(Role, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "ROLE_NOT_FOUND",
                    "details": f"Role with id={role_id} not found",
                },
            )
        return role

    async def update(self, role_id: int, payload: RoleUpdate) -> Role:
        role = await self.get(role_id)

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(role, key, value)

        try:
            await self.db.commit()
            await self.db.refresh(role)
            return role
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, role_id: int) -> None:
        role = await self.get(role_id)

        try:
            await self.db.delete(role)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def list(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[Role], int]:

        stmt = (
            select(Role)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        count_stmt = select(func.count(Role.id))

        roles = (await self.db.execute(stmt)).scalars().all()
        total = (await self.db.execute(count_stmt)).scalar_one()

        return roles, total
