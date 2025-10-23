"""Container schemas for API validation."""

from datetime import datetime
from typing import Any, List, Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.download import DownloadResponse


class ContainerCreate(BaseModel):
    """Schema for creating a container from URL."""

    url: str = Field(..., description="Container URL (FileCrypt.cc, etc.)")
    premium_account_id: Optional[int] = Field(None, description="Premium account ID to use")
    custom_name: Optional[str] = Field(None, description="Custom name for the container")
    custom_folder: Optional[str] = Field(None, description="Custom folder name")


class ContainerCreateManual(BaseModel):
    """Schema for creating a container manually with direct links."""

    name: str = Field(..., description="Container name")
    urls: List[str] = Field(..., description="List of download URLs")
    folder_name: Optional[str] = Field(None, description="Custom folder name")
    premium_account_id: Optional[int] = Field(None, description="Premium account ID to use")
    password: Optional[str] = Field(None, description="Archive password if needed")


class ContainerResponse(BaseModel):
    """Schema for container response."""

    id: int
    name: str
    url: Optional[str]
    source: Optional[str]
    folder_name: Optional[str]
    status: str
    total_links: int
    completed_links: int
    failed_links: int
    description: Optional[str]
    password: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContainerWithDownloads(ContainerResponse):
    """Schema for container with downloads."""

    downloads: List[Any] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ContainerStats(BaseModel):
    """Schema for container statistics."""

    total_containers: int
    active_containers: int
    completed_containers: int
    failed_containers: int
