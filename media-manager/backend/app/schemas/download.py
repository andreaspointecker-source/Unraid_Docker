"""Download schemas for API validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class DownloadCreate(BaseModel):
    """Schema for creating a new download."""

    url: str = Field(..., description="URL to download")
    premium_account_id: Optional[int] = Field(None, description="Premium account ID to use")


class DownloadBulkCreate(BaseModel):
    """Schema for creating multiple downloads."""

    urls: list[str] = Field(..., description="List of URLs to download")
    premium_account_id: Optional[int] = Field(None, description="Premium account ID to use")


class DownloadResponse(BaseModel):
    """Schema for download response."""

    id: int
    url: str
    filename: Optional[str] = None
    status: str
    progress: float
    speed: float
    size_total: Optional[int] = None
    size_downloaded: int
    eta: Optional[int] = None
    aria2_gid: Optional[str] = None
    premium_account_id: Optional[int] = None
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DownloadUpdate(BaseModel):
    """Schema for updating a download."""

    status: Optional[str] = None
    filename: Optional[str] = None
    file_path: Optional[str] = None


class DownloadStats(BaseModel):
    """Schema for global download statistics."""

    total_downloads: int
    completed_downloads: int
    failed_downloads: int
    active_downloads: int
    current_speed: float
    num_active: int
    num_waiting: int


class DownloadActionResponse(BaseModel):
    """Schema for download action responses."""

    success: bool
    message: str
    download: Optional[DownloadResponse] = None
