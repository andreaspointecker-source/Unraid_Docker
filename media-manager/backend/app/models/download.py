"""Download database model."""

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base
from app.models.base import DownloadStatus, TimestampMixin


class Download(Base, TimestampMixin):
    """Download model."""

    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    filename = Column(String(500))
    status = Column(String(20), default=DownloadStatus.PENDING.value, index=True)

    # Progress tracking
    progress = Column(Float, default=0.0)  # Percentage 0-100
    speed = Column(Float, default=0.0)  # Bytes per second
    size_total = Column(Integer)  # Total size in bytes
    size_downloaded = Column(Integer, default=0)  # Downloaded size in bytes
    eta = Column(Integer)  # Estimated time remaining in seconds

    # Download details
    aria2_gid = Column(String(50), unique=True, index=True)  # aria2c download GID
    premium_account_id = Column(Integer, nullable=True)  # FK to premium account

    # File info
    file_path = Column(Text)  # Path where file is/will be stored
    file_hash = Column(String(64))  # SHA-256 hash for verification

    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)

    # Metadata
    headers = Column(JSON)  # HTTP headers as JSON
    cookies = Column(JSON)  # Cookies as JSON
    extra_data = Column(JSON)  # Additional data

    def __repr__(self):
        return f"<Download(id={self.id}, filename={self.filename}, status={self.status})>"
