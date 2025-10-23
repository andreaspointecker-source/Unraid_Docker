"""Download API endpoints."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.download import (
    DownloadActionResponse,
    DownloadBulkCreate,
    DownloadCreate,
    DownloadResponse,
    DownloadStats,
)
from app.services.download_service import DownloadService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_download_service(db: Session = Depends(get_db)) -> DownloadService:
    """Get download service dependency."""
    return DownloadService(db)


@router.post("/", response_model=DownloadResponse, status_code=201)
async def add_download(
    data: DownloadCreate,
    service: DownloadService = Depends(get_download_service),
):
    """
    Add a new download.

    - **url**: URL to download
    - **premium_account_id**: Optional premium account to use
    """
    try:
        download = service.add_download(
            url=data.url,
            premium_account_id=data.premium_account_id,
        )
        return download
    except Exception as e:
        logger.error(f"Failed to add download: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk", response_model=List[DownloadResponse], status_code=201)
async def add_downloads_bulk(
    data: DownloadBulkCreate,
    service: DownloadService = Depends(get_download_service),
):
    """
    Add multiple downloads at once.

    - **urls**: List of URLs to download
    - **premium_account_id**: Optional premium account to use for all
    """
    downloads = []
    for url in data.urls:
        try:
            download = service.add_download(
                url=url,
                premium_account_id=data.premium_account_id,
            )
            downloads.append(download)
        except Exception as e:
            logger.error(f"Failed to add download {url}: {e}")
            # Continue with other downloads

    return downloads


@router.get("/", response_model=List[DownloadResponse])
async def list_downloads(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: DownloadService = Depends(get_download_service),
):
    """
    List downloads with optional filtering.

    - **status**: Filter by status (pending, queued, downloading, completed, failed, etc.)
    - **limit**: Maximum number of results (1-1000)
    - **offset**: Offset for pagination
    """
    downloads = service.list_downloads(status=status, limit=limit, offset=offset)

    # Update status from aria2c for active downloads
    for download in downloads:
        if download.status in ["queued", "downloading", "paused"]:
            service.update_download_status(download.id)

    return downloads


@router.get("/stats", response_model=DownloadStats)
async def get_download_stats(
    service: DownloadService = Depends(get_download_service),
):
    """
    Get global download statistics.

    Returns statistics about all downloads and current activity.
    """
    stats = service.get_global_stats()
    return stats


@router.get("/{download_id}", response_model=DownloadResponse)
async def get_download(
    download_id: int,
    service: DownloadService = Depends(get_download_service),
):
    """
    Get a specific download by ID.

    - **download_id**: Download ID
    """
    download = service.get_download(download_id)
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")

    # Update status from aria2c if active
    if download.status in ["queued", "downloading", "paused"]:
        service.update_download_status(download_id)

    return download


@router.post("/{download_id}/pause", response_model=DownloadActionResponse)
async def pause_download(
    download_id: int,
    service: DownloadService = Depends(get_download_service),
):
    """
    Pause a download.

    - **download_id**: Download ID
    """
    success = service.pause_download(download_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to pause download")

    download = service.get_download(download_id)
    return DownloadActionResponse(
        success=True,
        message="Download paused successfully",
        download=download,
    )


@router.post("/{download_id}/resume", response_model=DownloadActionResponse)
async def resume_download(
    download_id: int,
    service: DownloadService = Depends(get_download_service),
):
    """
    Resume a paused download.

    - **download_id**: Download ID
    """
    success = service.resume_download(download_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to resume download")

    download = service.get_download(download_id)
    return DownloadActionResponse(
        success=True,
        message="Download resumed successfully",
        download=download,
    )


@router.post("/{download_id}/cancel", response_model=DownloadActionResponse)
async def cancel_download(
    download_id: int,
    service: DownloadService = Depends(get_download_service),
):
    """
    Cancel a download.

    - **download_id**: Download ID
    """
    success = service.cancel_download(download_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to cancel download")

    download = service.get_download(download_id)
    return DownloadActionResponse(
        success=True,
        message="Download cancelled successfully",
        download=download,
    )


@router.post("/{download_id}/retry", response_model=DownloadActionResponse)
async def retry_download(
    download_id: int,
    service: DownloadService = Depends(get_download_service),
):
    """
    Retry a failed download.

    - **download_id**: Download ID
    """
    download = service.retry_download(download_id)
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")

    return DownloadActionResponse(
        success=True,
        message="Download retry initiated",
        download=download,
    )


@router.delete("/{download_id}", status_code=204)
async def delete_download(
    download_id: int,
    service: DownloadService = Depends(get_download_service),
):
    """
    Delete a download.

    - **download_id**: Download ID
    """
    success = service.delete_download(download_id)
    if not success:
        raise HTTPException(status_code=404, detail="Download not found")

    return None
