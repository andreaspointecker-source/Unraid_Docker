"""Container service for managing download packages."""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.container import Container
from app.models.download import Download
from app.services.link_grabber_service import LinkGrabberService
from app.services.download_service import DownloadService

logger = logging.getLogger(__name__)


class ContainerService:
    """Service for managing download containers (packages)."""

    def __init__(self, db: Session):
        self.db = db
        self.link_grabber = LinkGrabberService()
        self.download_service = DownloadService(db)

    def create_container_from_url(
        self,
        url: str,
        premium_account_id: Optional[int] = None,
        custom_name: Optional[str] = None,
        custom_folder: Optional[str] = None,
    ) -> Container:
        """
        Create a container from a URL (FileCrypt.cc, etc.) and extract all links.

        Args:
            url: Container URL
            premium_account_id: Optional premium account to use for downloads
            custom_name: Optional custom name for the container
            custom_folder: Optional custom folder name

        Returns:
            Created container with all downloads
        """
        try:
            logger.info(f"Creating container from URL: {url}")

            # Extract links from URL
            extracted = self.link_grabber.extract_links(url)

            # Check if captcha is required - JDownloader style
            if extracted.get("requires_captcha"):
                logger.info(f"Container requires captcha: {extracted.get('captcha_type')}")
                container = Container(
                    name=custom_name or extracted["name"],
                    url=url,
                    source=extracted["source"],
                    folder_name=custom_folder or self._sanitize_folder_name(extracted["name"]),
                    total_links=0,
                    status="pending_captcha",
                    description=f"Captcha required: {extracted.get('captcha_type')}",
                    extra_data=str(extracted),
                )
                self.db.add(container)
                self.db.commit()
                self.db.refresh(container)
                logger.info(f"Container {container.id} waiting for captcha resolution")
                return container

            # Check if password is required
            if extracted.get("requires_password"):
                logger.info("Container requires password")
                container = Container(
                    name=custom_name or extracted["name"],
                    url=url,
                    source=extracted["source"],
                    folder_name=custom_folder or self._sanitize_folder_name(extracted["name"]),
                    total_links=0,
                    status="pending_password",
                    description="Password required",
                    extra_data=str(extracted),
                )
                self.db.add(container)
                self.db.commit()
                self.db.refresh(container)
                logger.info(f"Container {container.id} waiting for password")
                return container

            # Create container with extracted links
            container = Container(
                name=custom_name or extracted["name"],
                url=url,
                source=extracted["source"],
                folder_name=custom_folder or self._sanitize_folder_name(extracted["name"]),
                total_links=extracted["total_links"],
                password=extracted.get("password"),
                status="pending",
            )

            self.db.add(container)
            self.db.commit()
            self.db.refresh(container)

            logger.info(f"Created container {container.id}: {container.name}")

            # Add all downloads
            for link_url in extracted["links"]:
                try:
                    download = self.download_service.add_download(
                        url=link_url,
                        premium_account_id=premium_account_id,
                        container_id=container.id,
                    )
                    logger.info(f"Added download {download.id} to container {container.id}")
                except Exception as e:
                    logger.error(f"Failed to add download {link_url}: {e}")
                    container.failed_links += 1

            # Update container status
            if container.total_links > 0:
                container.status = "active"
            else:
                container.status = "failed"

            self.db.commit()
            self.db.refresh(container)

            return container

        except Exception as e:
            logger.error(f"Failed to create container from URL: {e}")
            self.db.rollback()
            raise

    def create_container_manual(
        self,
        name: str,
        urls: List[str],
        folder_name: Optional[str] = None,
        premium_account_id: Optional[int] = None,
        password: Optional[str] = None,
    ) -> Container:
        """
        Create a container manually with direct download links.

        Args:
            name: Container name
            urls: List of download URLs
            folder_name: Optional custom folder name
            premium_account_id: Optional premium account to use
            password: Optional archive password

        Returns:
            Created container with all downloads
        """
        try:
            logger.info(f"Creating manual container: {name} with {len(urls)} URLs")

            # Create container
            container = Container(
                name=name,
                source="manual",
                folder_name=folder_name or self._sanitize_folder_name(name),
                total_links=len(urls),
                password=password,
                status="pending",
            )

            self.db.add(container)
            self.db.commit()
            self.db.refresh(container)

            logger.info(f"Created container {container.id}: {container.name}")

            # Add all downloads
            for url in urls:
                try:
                    download = self.download_service.add_download(
                        url=url,
                        premium_account_id=premium_account_id,
                        container_id=container.id,
                    )
                    logger.info(f"Added download {download.id} to container {container.id}")
                except Exception as e:
                    logger.error(f"Failed to add download {url}: {e}")
                    container.failed_links += 1

            # Update container status
            if container.total_links > 0:
                container.status = "active"
            else:
                container.status = "failed"

            self.db.commit()
            self.db.refresh(container)

            return container

        except Exception as e:
            logger.error(f"Failed to create manual container: {e}")
            self.db.rollback()
            raise

    def get_container(self, container_id: int) -> Optional[Container]:
        """Get container by ID."""
        return self.db.query(Container).filter(Container.id == container_id).first()

    def list_containers(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Container]:
        """
        List containers with optional filtering.

        Args:
            status: Filter by status
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of containers
        """
        query = self.db.query(Container)

        if status:
            query = query.filter(Container.status == status)

        query = query.order_by(Container.created_at.desc())
        query = query.limit(limit).offset(offset)

        return query.all()

    def update_container_status(self, container_id: int) -> Optional[Container]:
        """
        Update container status based on download states.

        Args:
            container_id: Container ID

        Returns:
            Updated container or None
        """
        container = self.get_container(container_id)
        if not container:
            return None

        # Count download statuses
        completed = 0
        failed = 0
        active = 0

        for download in container.downloads:
            if download.status == "completed":
                completed += 1
            elif download.status == "failed":
                failed += 1
            elif download.status in ["downloading", "queued", "pending"]:
                active += 1

        # Update container
        container.completed_links = completed
        container.failed_links = failed

        # Update status
        if completed == container.total_links:
            container.status = "completed"
        elif failed == container.total_links:
            container.status = "failed"
        elif active > 0:
            container.status = "active"
        else:
            container.status = "pending"

        self.db.commit()
        return container

    def delete_container(self, container_id: int) -> bool:
        """
        Delete container and all associated downloads.

        Args:
            container_id: Container ID

        Returns:
            True if deleted, False if not found
        """
        container = self.get_container(container_id)
        if not container:
            return False

        self.db.delete(container)
        self.db.commit()
        return True

    def _sanitize_folder_name(self, name: str) -> str:
        """
        Sanitize folder name by removing invalid characters.

        Args:
            name: Original name

        Returns:
            Sanitized folder name
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")

        # Remove leading/trailing spaces and dots
        name = name.strip(" .")

        # Limit length
        if len(name) > 200:
            name = name[:200]

        return name or "container"
