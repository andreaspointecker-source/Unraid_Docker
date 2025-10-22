"""Archive password database model."""

from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base
from app.models.base import TimestampMixin


class ArchivePassword(Base, TimestampMixin):
    """Archive password model for automatic extraction."""

    __tablename__ = "archive_passwords"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), unique=True, nullable=False, index=True)

    # Statistics
    success_count = Column(Integer, default=0)  # How many times it worked
    fail_count = Column(Integer, default=0)  # How many times it failed
    priority = Column(Integer, default=0)  # Higher priority = tried first

    # Status
    is_active = Column(Boolean, default=True)  # Can be disabled without deleting

    # Source tracking
    source = Column(String(100))  # Where the password came from (user, auto-learned, etc.)

    def __repr__(self):
        return f"<ArchivePassword(id={self.id}, success_count={self.success_count})>"
