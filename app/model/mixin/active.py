from sqlalchemy import Column, Boolean


class ActiveMixin:
    is_active = Column(Boolean, default=True, nullable=False)