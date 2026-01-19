from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schema.common import APIResponse, MetaSchema
from app.schema.rbac.role import RoleCreate, RoleUpdate, RoleResponse
from app.service.rbac.role import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post(
    "",
    response_model=APIResponse[RoleResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    payload: RoleCreate,
    db: AsyncSession = Depends(get_db),
):
    role = await RoleService.create(db, payload)
    return APIResponse(
        success=True,
        message="Role created successfully",
        data=role,
    )


@router.get(
    "/{role_id}",
    response_model=APIResponse[RoleResponse],
)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
):
    role = await RoleService.get(db, role_id)
    return APIResponse(
        success=True,
        message="Role fetched successfully",
        data=role,
    )


@router.put(
    "/{role_id}",
    response_model=APIResponse[RoleResponse],
)
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: AsyncSession = Depends(get_db),
):
    role = await RoleService.update(db, role_id, payload)
    return APIResponse(
        success=True,
        message="Role updated successfully",
        data=role,
    )


@router.delete(
    "/{role_id}",
    response_model=APIResponse[None],
)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
):
    await RoleService.delete(db, role_id)
    return APIResponse(
        success=True,
        message="Role deleted successfully",
    )


@router.get(
    "",
    response_model=APIResponse[list[RoleResponse]],
)
async def list_roles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db),
):
    roles, total = await RoleService.list(db, page, page_size)

    return APIResponse(
        success=True,
        message="Roles fetched successfully",
        data=roles,
        meta=MetaSchema(
            page=page,
            page_size=page_size,
            total=total,
        ),
    )
