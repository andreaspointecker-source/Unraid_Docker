"""Application configuration management."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_name: str = "Docker Media Manager"
    app_env: str = "production"
    secret_key: str
    debug: bool = False
    log_level: str = "INFO"

    # Server
    host: str = "0.0.0.0"
    port: int = 8080
    web_port: int = 8080

    # User/Group
    puid: int = 99
    pgid: int = 100
    tz: str = "Europe/Berlin"

    # Database
    database_url: str = "sqlite:////config/database.db"

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: str = "redis://redis:6379/0"

    # TMDB
    tmdb_api_key: Optional[str] = None
    tmdb_language: str = "de-DE"
    tmdb_cache_ttl: int = 24  # hours

    # aria2c
    aria2c_host: str = "localhost"
    aria2c_port: int = 6800
    aria2c_secret: str = ""
    max_concurrent_downloads: int = 3
    max_download_speed: int = 0  # 0 = unlimited

    # Premium Accounts (optional)
    rapidgator_username: Optional[str] = None
    rapidgator_password: Optional[str] = None
    ddownload_username: Optional[str] = None
    ddownload_password: Optional[str] = None

    # Encoding
    encoding_strategy: str = "prefer_remote"  # prefer_remote, remote_only, server_only, load_balance
    max_parallel_encodings: int = 2
    hardware_accel: str = "auto"  # auto, nvenc, qsv, amf, none

    # Remote Worker
    remote_worker_enabled: bool = False
    remote_worker_url: Optional[str] = None
    remote_worker_api_key: Optional[str] = None
    remote_worker_use_share: bool = False
    remote_worker_share_path: str = "/mnt/shared"

    # File Organization
    auto_organize: bool = True
    delete_original_after_conversion: bool = True
    delete_temp_files: bool = True

    # Paths
    downloads_path: Path = Path("/downloads")
    media_path: Path = Path("/media")
    config_path: Path = Path("/config")
    cache_path: Path = Path("/cache")

    # Web Interface
    enable_cors: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]

    # Security
    jwt_expiration: int = 60  # minutes
    enable_api_auth: bool = True
    api_rate_limit: int = 60  # requests per minute

    # Advanced
    celery_workers: int = 4
    cleanup_interval: int = 24  # hours

    @property
    def downloads_incomplete_path(self) -> Path:
        """Get path for incomplete downloads."""
        return self.downloads_path / "incomplete"

    @property
    def downloads_complete_path(self) -> Path:
        """Get path for complete downloads."""
        return self.downloads_path / "complete"

    @property
    def downloads_extracted_path(self) -> Path:
        """Get path for extracted files."""
        return self.downloads_path / "extracted"

    @property
    def downloads_quarantine_path(self) -> Path:
        """Get path for quarantined files."""
        return self.downloads_path / "quarantine"

    @property
    def movies_path(self) -> Path:
        """Get path for movies."""
        return self.media_path / "movies"

    @property
    def tv_path(self) -> Path:
        """Get path for TV shows."""
        return self.media_path / "tv"

    @property
    def tmdb_cache_path(self) -> Path:
        """Get path for TMDB cache."""
        return self.cache_path / "tmdb"

    @property
    def thumbnails_cache_path(self) -> Path:
        """Get path for thumbnails cache."""
        return self.cache_path / "thumbnails"

    @property
    def presets_path(self) -> Path:
        """Get path for encoding presets."""
        return self.config_path / "presets"

    @property
    def logs_path(self) -> Path:
        """Get path for logs."""
        return self.config_path / "logs"

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.downloads_incomplete_path,
            self.downloads_complete_path,
            self.downloads_extracted_path,
            self.downloads_quarantine_path,
            self.movies_path,
            self.tv_path,
            self.tmdb_cache_path,
            self.thumbnails_cache_path,
            self.presets_path,
            self.logs_path,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: Application settings
    """
    return Settings()


# Convenience export
settings = get_settings()
