"""Container model for organizing related downloads (e.g., from FileCrypt.cc)."""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Container(Base):
    """
    Container model for organizing related downloads as a package.

    Used for:
    - FileCrypt.cc containers
    - Multi-part archives
    - Season packs
    - Any grouped downloads that belong together
    """

    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    url = Column(String(500), nullable=True)  # Original container URL (e.g., FileCrypt.cc)
    source = Column(String(100), nullable=True)  # Source type: filecrypt, manual, etc.
    folder_name = Column(String(255), nullable=True)  # Folder name for downloads
    status = Column(String(50), default="pending", index=True)  # pending, active, completed, failed
    total_links = Column(Integer, default=0)
    completed_links = Column(Integer, default=0)
    failed_links = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    password = Column(String(255), nullable=True)  # Container password if needed
    extra_data = Column(Text, nullable=True)  # JSON for additional metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to downloads
    downloads = relationship("Download", back_populates="container", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Container {self.id}: {self.name} ({self.status})>"
