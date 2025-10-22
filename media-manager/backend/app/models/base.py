"""Base models and enums for database."""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from app.database import Base


class TimestampMixin:
    """Mixin for adding timestamp columns."""

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TaskStatus(str, PyEnum):
    """Status for various tasks."""

    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class DownloadStatus(str, PyEnum):
    """Download status."""

    PENDING = "pending"
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class ExtractionStatus(str, PyEnum):
    """Extraction status."""

    PENDING = "pending"
    EXTRACTING = "extracting"
    COMPLETED = "completed"
    FAILED = "failed"
    PASSWORD_REQUIRED = "password_required"


class EncodingStatus(str, PyEnum):
    """Encoding status."""

    PENDING = "pending"
    QUEUED = "queued"
    ENCODING = "encoding"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MetadataStatus(str, PyEnum):
    """TMDB metadata status."""

    PENDING = "pending"
    SEARCHING = "searching"
    FOUND = "found"
    MANUAL_REQUIRED = "manual_required"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class MediaType(str, PyEnum):
    """Media type."""

    MOVIE = "movie"
    TV = "tv"
    UNKNOWN = "unknown"


class WorkerType(str, PyEnum):
    """Worker type."""

    SERVER = "server"
    REMOTE = "remote"


class WorkerStatus(str, PyEnum):
    """Worker status."""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"
