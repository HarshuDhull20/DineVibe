from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete"
    )
