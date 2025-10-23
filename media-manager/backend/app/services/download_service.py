"""Download management service."""

import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Download, DownloadStatus
from app.services.aria2_service import get_aria2_service

logger = logging.getLogger(__name__)


class DownloadService:
    """Service for managing downloads."""

    def __init__(self, db: Session):
        """
        Initialize download service.

        Args:
            db: Database session
        """
        self.db = db
        self.aria2 = get_aria2_service()

    def add_download(
        self,
        url: str,
        premium_account_id: Optional[int] = None,
        container_id: Optional[int] = None,
    ) -> Download:
        """
        Add a new download.

        Args:
            url: Download URL
            premium_account_id: Optional premium account ID
            container_id: Optional container ID for grouping

        Returns:
            Download: Created download object
        """
        # Create database entry
        download = Download(
            url=url,
            status=DownloadStatus.PENDING.value,
            premium_account_id=premium_account_id,
            container_id=container_id,
        )
        self.db.add(download)
        self.db.commit()
        self.db.refresh(download)

        # Add to aria2c
        gid = self.aria2.add_download(url)
        if gid:
            download.aria2_gid = gid
            download.status = DownloadStatus.QUEUED.value
            self.db.commit()
            logger.info(f"Download added: {url} (ID: {download.id}, GID: {gid})")
        else:
            download.status = DownloadStatus.FAILED.value
            download.error_message = "Failed to add to aria2c"
            self.db.commit()
            logger.error(f"Failed to add download to aria2c: {url}")

        return download

    def get_download(self, download_id: int) -> Optional[Download]:
        """
        Get download by ID.

        Args:
            download_id: Download ID

        Returns:
            Download object or None
        """
        return self.db.query(Download).filter(Download.id == download_id).first()

    def get_download_by_gid(self, gid: str) -> Optional[Download]:
        """
        Get download by aria2c GID.

        Args:
            gid: aria2c GID

        Returns:
            Download object or None
        """
        return self.db.query(Download).filter(Download.aria2_gid == gid).first()

    def list_downloads(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Download]:
        """
        List downloads with optional filtering.

        Args:
            status: Filter by status
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of downloads
        """
        query = self.db.query(Download)

        if status:
            query = query.filter(Download.status == status)

        query = query.order_by(Download.created_at.desc())
        return query.offset(offset).limit(limit).all()

    def update_download_status(self, download_id: int) -> Optional[Download]:
        """
        Update download status from aria2c.

        Args:
            download_id: Download ID

        Returns:
            Updated download or None
        """
        download = self.get_download(download_id)
        if not download or not download.aria2_gid:
            return None

        # Get status from aria2c
        status = self.aria2.get_download_status(download.aria2_gid)
        if not status:
            return download

        # Update download
        download.progress = status.get("progress", 0.0)
        download.speed = status.get("download_speed", 0)
        download.size_total = status.get("total_length", 0)
        download.size_downloaded = status.get("completed_length", 0)

        # Map aria2c status to our status
        aria2_status = status.get("status", "")
        if aria2_status == "active":
            download.status = DownloadStatus.DOWNLOADING.value
        elif aria2_status == "complete":
            download.status = DownloadStatus.COMPLETED.value
            # Set file path from aria2c
            if status.get("files") and len(status["files"]) > 0:
                download.file_path = str(status["files"][0]["path"])
                download.filename = status.get("name", "")
        elif aria2_status == "error":
            download.status = DownloadStatus.FAILED.value
            download.error_message = "Download error in aria2c"
        elif aria2_status == "paused":
            download.status = DownloadStatus.PAUSED.value

        self.db.commit()
        return download

    def pause_download(self, download_id: int) -> bool:
        """
        Pause a download.

        Args:
            download_id: Download ID

        Returns:
            bool: True if successful
        """
        download = self.get_download(download_id)
        if not download or not download.aria2_gid:
            return False

        if self.aria2.pause_download(download.aria2_gid):
            download.status = DownloadStatus.PAUSED.value
            self.db.commit()
            return True
        return False

    def resume_download(self, download_id: int) -> bool:
        """
        Resume a paused download.

        Args:
            download_id: Download ID

        Returns:
            bool: True if successful
        """
        download = self.get_download(download_id)
        if not download or not download.aria2_gid:
            return False

        if self.aria2.resume_download(download.aria2_gid):
            download.status = DownloadStatus.DOWNLOADING.value
            self.db.commit()
            return True
        return False

    def cancel_download(self, download_id: int) -> bool:
        """
        Cancel a download.

        Args:
            download_id: Download ID

        Returns:
            bool: True if successful
        """
        download = self.get_download(download_id)
        if not download or not download.aria2_gid:
            return False

        if self.aria2.remove_download(download.aria2_gid, force=True):
            download.status = DownloadStatus.CANCELLED.value
            self.db.commit()
            return True
        return False

    def delete_download(self, download_id: int) -> bool:
        """
        Delete a download from database.

        Args:
            download_id: Download ID

        Returns:
            bool: True if successful
        """
        download = self.get_download(download_id)
        if not download:
            return False

        # Remove from aria2c if still active
        if download.aria2_gid:
            self.aria2.remove_download(download.aria2_gid, force=True)

        self.db.delete(download)
        self.db.commit()
        return True

    def retry_download(self, download_id: int) -> Optional[Download]:
        """
        Retry a failed download.

        Args:
            download_id: Download ID

        Returns:
            Download object or None
        """
        download = self.get_download(download_id)
        if not download:
            return None

        # Remove old aria2c entry if exists
        if download.aria2_gid:
            self.aria2.remove_download(download.aria2_gid, force=True)

        # Re-add to aria2c
        gid = self.aria2.add_download(download.url)
        if gid:
            download.aria2_gid = gid
            download.status = DownloadStatus.QUEUED.value
            download.retry_count = (download.retry_count or 0) + 1
            download.error_message = None
            self.db.commit()
            logger.info(f"Retry download {download_id} (attempt {download.retry_count})")
            return download
        else:
            download.status = DownloadStatus.FAILED.value
            download.error_message = "Failed to retry in aria2c"
            self.db.commit()
            return download

    def get_global_stats(self) -> dict:
        """
        Get global download statistics.

        Returns:
            dict: Global stats
        """
        # Get from aria2c
        aria2_stats = self.aria2.get_global_stats()

        # Get from database
        total = self.db.query(Download).count()
        completed = self.db.query(Download).filter(
            Download.status == DownloadStatus.COMPLETED.value
        ).count()
        failed = self.db.query(Download).filter(
            Download.status == DownloadStatus.FAILED.value
        ).count()
        active = self.db.query(Download).filter(
            Download.status.in_([
                DownloadStatus.DOWNLOADING.value,
                DownloadStatus.QUEUED.value
            ])
        ).count()

        return {
            "total_downloads": total,
            "completed_downloads": completed,
            "failed_downloads": failed,
            "active_downloads": active,
            "current_speed": aria2_stats.get("download_speed", 0),
            "num_active": aria2_stats.get("num_active", 0),
            "num_waiting": aria2_stats.get("num_waiting", 0),
        }
