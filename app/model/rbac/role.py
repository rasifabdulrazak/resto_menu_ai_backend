from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.model.base import Base
from app.model.mixin.active import ActiveMixin


class Role(Base, ActiveMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(String(255))

    users = relationship("UserRole", back_populates="role")
    permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("code", name="uq_role_code"),
    )
