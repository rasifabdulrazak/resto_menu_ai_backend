from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.model.base import Base
from app.model.mixin import active,soft_delete



class User(Base,active.ActiveMixin,soft_delete.SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(150))
    hashed_password = Column(String(255))

    roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    permissions = relationship(
        "UserPermission",
        back_populates="user",
        cascade="all, delete-orphan",
    )