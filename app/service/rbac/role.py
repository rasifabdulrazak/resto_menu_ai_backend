from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.model.rbac.role import Role
from app.schema.rbac.role import RoleCreate, RoleUpdate
from fastapi import HTTPException, status


class RoleService:

    @staticmethod
    async def create(db: AsyncSession, payload: RoleCreate) -> Role:
        role = Role(**payload.model_dump())
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def get(db: AsyncSession, role_id: int) -> Role:
        role = await db.get(Role, role_id)
        print(role,"============")
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "ROLE_NOT_FOUND",
                    "details": f"Role with id={role_id} not found",
                },
            )
        return role

    @staticmethod
    async def update(db: AsyncSession, role_id: int, payload: RoleUpdate) -> Role:
        role = await RoleService.get(db, role_id)

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(role, key, value)

        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def delete(db: AsyncSession, role_id: int) -> None:
        role = await RoleService.get(db, role_id)
        await db.delete(role)
        await db.commit()

    @staticmethod
    async def list(
        db: AsyncSession,
        page: int,
        page_size: int,
    ) -> tuple[list[Role], int]:

        stmt = select(Role).offset((page - 1) * page_size).limit(page_size)
        count_stmt = select(func.count(Role.id))

        roles = (await db.execute(stmt)).scalars().all()
        total = (await db.execute(count_stmt)).scalar_one()

        return roles, total 
