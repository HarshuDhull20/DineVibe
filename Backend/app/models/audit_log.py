from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class AuditLog(Base):
    """
    Stores security-sensitive and role-related actions
    across the platform.

    Used for:
    - Security activity log
    - Role change history
    - Account status changes
    - Admin actions
    """

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # User who triggered the action
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Type of action performed
    action = Column(String(50), nullable=False)
    # Examples:
    # LOGIN_SUCCESS
    # LOGIN_FAILED
    # PASSWORD_CHANGED
    # ROLE_CHANGED
    # ACCOUNT_DEACTIVATED
    # MFA_ENABLED
    # MFA_DISABLED
    # FORCE_LOGOUT
    # ADMIN_APPROVAL

    # Human-readable description
    details = Column(Text, nullable=True)

    # When the action happened
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to User
    user = relationship("User", back_populates="audit_logs")
