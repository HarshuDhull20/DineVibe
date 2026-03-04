from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.user import UserRole

class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(Enum(UserRole), nullable=False)