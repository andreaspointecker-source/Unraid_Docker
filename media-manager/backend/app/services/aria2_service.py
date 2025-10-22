"""aria2c RPC client service."""

import logging
from typing import Dict, List, Optional

import aria2p

from app.config import settings

logger = logging.getLogger(__name__)


class Aria2Service:
    """Service for interacting with aria2c via RPC."""

    def __init__(self):
        """Initialize aria2c client."""
        self.client: Optional[aria2p.API] = None
        self._connect()

    def _connect(self) -> None:
        """Connect to aria2c RPC server."""
        try:
            # Create aria2c client
            self.client = aria2p.API(
                aria2p.Client(
                    host=f"http://{settings.aria2c_host}",
                    port=settings.aria2c_port,
                    secret=settings.aria2c_secret if settings.aria2c_secret else "",
                )
            )
            logger.info(f"Connected to aria2c at {settings.aria2c_host}:{settings.aria2c_port}")
        except Exception as e:
            logger.error(f"Failed to connect to aria2c: {e}")
            self.client = None

    def add_download(
        self,
        url: str,
        options: Optional[Dict] = None,
    ) -> Optional[str]:
        """
        Add a new download to aria2c.

        Args:
            url: Download URL
            options: aria2c options dict

        Returns:
            str: Download GID (identifier) or None if failed
        """
        if not self.client:
            logger.error("aria2c client not connected")
            return None

        try:
            default_options = {
                "dir": str(settings.downloads_incomplete_path),
                "max-connection-per-server": "16",
                "split": "16",
                "min-split-size": "1M",
                "continue": "true",
            }

            if settings.max_download_speed > 0:
                default_options["max-download-limit"] = str(settings.max_download_speed * 1024)

            if options:
                default_options.update(options)

            download = self.client.add_uris([url], options=default_options)
            logger.info(f"Added download: {url} (GID: {download.gid})")
            return download.gid
        except Exception as e:
            logger.error(f"Failed to add download {url}: {e}")
            return None

    def get_download(self, gid: str) -> Optional[aria2p.Download]:
        """
        Get download by GID.

        Args:
            gid: Download GID

        Returns:
            Download object or None
        """
        if not self.client:
            return None

        try:
            downloads = self.client.get_downloads([gid])
            return downloads[0] if downloads else None
        except Exception as e:
            logger.error(f"Failed to get download {gid}: {e}")
            return None

    def get_all_downloads(self) -> List[aria2p.Download]:
        """
        Get all downloads.

        Returns:
            List of Download objects
        """
        if not self.client:
            return []

        try:
            return self.client.get_downloads()
        except Exception as e:
            logger.error(f"Failed to get downloads: {e}")
            return []

    def pause_download(self, gid: str) -> bool:
        """
        Pause a download.

        Args:
            gid: Download GID

        Returns:
            bool: True if successful
        """
        if not self.client:
            return False

        try:
            download = self.get_download(gid)
            if download:
                download.pause()
                logger.info(f"Paused download {gid}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to pause download {gid}: {e}")
            return False

    def resume_download(self, gid: str) -> bool:
        """
        Resume a paused download.

        Args:
            gid: Download GID

        Returns:
            bool: True if successful
        """
        if not self.client:
            return False

        try:
            download = self.get_download(gid)
            if download:
                download.resume()
                logger.info(f"Resumed download {gid}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to resume download {gid}: {e}")
            return False

    def remove_download(self, gid: str, force: bool = False) -> bool:
        """
        Remove a download.

        Args:
            gid: Download GID
            force: Force removal even if downloading

        Returns:
            bool: True if successful
        """
        if not self.client:
            return False

        try:
            download = self.get_download(gid)
            if download:
                if force:
                    download.remove(force=True)
                else:
                    download.remove()
                logger.info(f"Removed download {gid}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove download {gid}: {e}")
            return False

    def get_download_status(self, gid: str) -> Optional[Dict]:
        """
        Get detailed download status.

        Args:
            gid: Download GID

        Returns:
            dict: Download status information
        """
        download = self.get_download(gid)
        if not download:
            return None

        try:
            return {
                "gid": download.gid,
                "status": download.status,
                "total_length": download.total_length,
                "completed_length": download.completed_length,
                "download_speed": download.download_speed,
                "upload_speed": download.upload_speed,
                "progress": download.progress,
                "eta": download.eta_string,
                "name": download.name,
                "files": [
                    {
                        "path": f.path,
                        "length": f.length,
                        "completed_length": f.completed_length,
                    }
                    for f in download.files
                ],
            }
        except Exception as e:
            logger.error(f"Failed to get status for {gid}: {e}")
            return None

    def get_global_stats(self) -> Dict:
        """
        Get global aria2c statistics.

        Returns:
            dict: Global stats
        """
        if not self.client:
            return {}

        try:
            stats = self.client.get_stats()
            return {
                "download_speed": stats.download_speed,
                "upload_speed": stats.upload_speed,
                "num_active": stats.num_active,
                "num_waiting": stats.num_waiting,
                "num_stopped": stats.num_stopped,
            }
        except Exception as e:
            logger.error(f"Failed to get global stats: {e}")
            return {}


# Global instance
_aria2_service: Optional[Aria2Service] = None


def get_aria2_service() -> Aria2Service:
    """
    Get or create aria2c service instance.

    Returns:
        Aria2Service: Service instance
    """
    global _aria2_service
    if _aria2_service is None:
        _aria2_service = Aria2Service()
    return _aria2_service
