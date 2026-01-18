from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.model.base import Base
from app.model.mixin.active import ActiveMixin


class Permission(Base,ActiveMixin):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    code = Column(String(100), nullable=False)
    description = Column(String(255))

    roles = relationship("RolePermission", back_populates="permission")
    users = relationship("UserPermission", back_populates="permission")

    __table_args__ = (
        UniqueConstraint("code", name="uq_permission_code"),
    )
