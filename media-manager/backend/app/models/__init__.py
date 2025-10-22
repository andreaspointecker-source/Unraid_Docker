"""Database models package."""

from app.models.account import PremiumAccount
from app.models.base import (
    DownloadStatus,
    EncodingStatus,
    ExtractionStatus,
    MediaType,
    MetadataStatus,
    TaskStatus,
    TimestampMixin,
    WorkerStatus,
    WorkerType,
)
from app.models.download import Download
from app.models.encoding import EncodingJob, EncodingPreset
from app.models.metadata import MediaMetadata
from app.models.password import ArchivePassword
from app.models.worker import Worker

__all__ = [
    # Models
    "Download",
    "EncodingJob",
    "EncodingPreset",
    "MediaMetadata",
    "PremiumAccount",
    "ArchivePassword",
    "Worker",
    # Enums
    "DownloadStatus",
    "EncodingStatus",
    "ExtractionStatus",
    "MediaType",
    "MetadataStatus",
    "TaskStatus",
    "WorkerStatus",
    "WorkerType",
    # Mixins
    "TimestampMixin",
]
