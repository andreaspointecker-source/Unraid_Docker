"""Premium account database model."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base
from app.models.base import TimestampMixin


class PremiumAccount(Base, TimestampMixin):
    """Premium filehosting account model."""

    __tablename__ = "premium_accounts"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False, index=True)  # rapidgator, ddownload, etc.
    name = Column(String(100))  # User-friendly name
    username = Column(String(255), nullable=False)
    password_encrypted = Column(Text, nullable=False)  # Encrypted password

    # Status
    is_active = Column(Boolean, default=True)
    is_valid = Column(Boolean, default=True)  # Set to False if login fails
    last_validated = Column(DateTime(timezone=True))

    # Usage tracking
    last_used = Column(DateTime(timezone=True))
    use_count = Column(Integer, default=0)

    # Account limits (if applicable)
    daily_limit = Column(Integer)  # Daily download limit in bytes
    daily_used = Column(Integer, default=0)
    limit_reset_at = Column(DateTime(timezone=True))

    # Premium status
    premium_until = Column(DateTime(timezone=True))
    traffic_left = Column(Integer)  # Remaining traffic in bytes

    # Additional data
    api_key = Column(Text)  # Some providers use API keys
    cookies = Column(Text)  # Stored session cookies (encrypted)
    extra_data = Column(Text)  # JSON for provider-specific data

    def __repr__(self):
        return f"<PremiumAccount(id={self.id}, provider={self.provider}, username={self.username})>"
