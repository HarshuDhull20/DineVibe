from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.user import UserRole


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)

    role = Column(
        SQLAlchemyEnum(UserRole, name="user_roles"),
        nullable=False
    )

    permission_id = Column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False
    )

    permission = relationship(
        "Permission",
        back_populates="role_permissions"
    )
