from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.model.base import Base


class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)

    is_allowed = Column(Boolean, default=True)

    user = relationship("User", back_populates="permissions")
    permission = relationship("Permission", back_populates="users")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "permission_id",
            name="uq_user_permission",
        ),
    )
