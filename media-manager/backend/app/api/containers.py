"""Container API endpoints."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.container import (
    ContainerCreate,
    ContainerCreateManual,
    ContainerResponse,
    ContainerWithDownloads,
    ContainerStats,
)
from app.services.container_service import ContainerService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_container_service(db: Session = Depends(get_db)) -> ContainerService:
    """Get container service dependency."""
    return ContainerService(db)


@router.post("/", response_model=ContainerResponse, status_code=201)
async def create_container(
    data: ContainerCreate,
    service: ContainerService = Depends(get_container_service),
):
    """
    Create a container from a URL (FileCrypt.cc, etc.).

    Automatically extracts all download links and creates downloads.

    - **url**: Container URL (e.g., https://filecrypt.cc/Container/XXX.html)
    - **premium_account_id**: Optional premium account to use for all downloads
    - **custom_name**: Optional custom name for the container
    - **custom_folder**: Optional custom folder name for downloads
    """
    try:
        container = service.create_container_from_url(
            url=data.url,
            premium_account_id=data.premium_account_id,
            custom_name=data.custom_name,
            custom_folder=data.custom_folder,
        )
        return container
    except Exception as e:
        logger.error(f"Failed to create container: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/manual", response_model=ContainerResponse, status_code=201)
async def create_container_manual(
    data: ContainerCreateManual,
    service: ContainerService = Depends(get_container_service),
):
    """
    Create a container manually with direct download links.

    Perfect for when you already have the download links (e.g., copied from FileCrypt.cc).

    - **name**: Container name (e.g., "Movie Pack", "Season 1")
    - **urls**: List of download URLs (RapidGator, DDownload, etc.)
    - **folder_name**: Optional custom folder for downloads
    - **premium_account_id**: Optional premium account to use
    - **password**: Optional archive password
    """
    try:
        container = service.create_container_manual(
            name=data.name,
            urls=data.urls,
            folder_name=data.folder_name,
            premium_account_id=data.premium_account_id,
            password=data.password,
        )
        return container
    except Exception as e:
        logger.error(f"Failed to create manual container: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ContainerResponse])
async def list_containers(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ContainerService = Depends(get_container_service),
):
    """
    List containers with optional filtering.

    - **status**: Filter by status (pending, active, completed, failed)
    - **limit**: Maximum number of results (1-1000)
    - **offset**: Offset for pagination
    """
    containers = service.list_containers(status=status, limit=limit, offset=offset)

    # Update status for active containers
    for container in containers:
        if container.status in ["active", "pending"]:
            service.update_container_status(container.id)

    return containers


@router.get("/stats", response_model=ContainerStats)
async def get_container_stats(
    service: ContainerService = Depends(get_container_service),
):
    """
    Get container statistics.

    Returns counts of containers by status.
    """
    from app.models.container import Container

    db = service.db

    total = db.query(Container).count()
    active = db.query(Container).filter(Container.status == "active").count()
    completed = db.query(Container).filter(Container.status == "completed").count()
    failed = db.query(Container).filter(Container.status == "failed").count()

    return {
        "total_containers": total,
        "active_containers": active,
        "completed_containers": completed,
        "failed_containers": failed,
    }


@router.get("/{container_id}")
async def get_container(
    container_id: int,
    service: ContainerService = Depends(get_container_service),
):
    """
    Get a specific container by ID with all downloads.

    - **container_id**: Container ID
    """
    from app.schemas.download import DownloadResponse

    container = service.get_container(container_id)
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Update status
    service.update_container_status(container_id)

    # Serialize downloads manually
    downloads = [DownloadResponse.model_validate(d) for d in container.downloads]

    return {
        "id": container.id,
        "name": container.name,
        "url": container.url,
        "source": container.source,
        "folder_name": container.folder_name,
        "status": container.status,
        "total_links": container.total_links,
        "completed_links": container.completed_links,
        "failed_links": container.failed_links,
        "description": container.description,
        "password": container.password,
        "created_at": container.created_at,
        "updated_at": container.updated_at,
        "downloads": downloads,
    }


@router.delete("/{container_id}", status_code=204)
async def delete_container(
    container_id: int,
    service: ContainerService = Depends(get_container_service),
):
    """
    Delete a container and all associated downloads.

    - **container_id**: Container ID
    """
    success = service.delete_container(container_id)
    if not success:
        raise HTTPException(status_code=404, detail="Container not found")
