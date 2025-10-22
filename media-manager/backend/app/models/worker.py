"""Remote worker database model."""

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from app.database import Base
from app.models.base import TimestampMixin, WorkerStatus, WorkerType


class Worker(Base, TimestampMixin):
    """Remote encoding worker model."""

    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    worker_type = Column(String(20), default=WorkerType.SERVER.value)

    # Connection
    host = Column(String(255))  # URL or IP
    port = Column(Integer, default=5000)
    api_key = Column(Text)  # Encrypted API key
    use_https = Column(Boolean, default=False)

    # Status
    status = Column(String(20), default=WorkerStatus.OFFLINE.value, index=True)
    last_seen = Column(DateTime(timezone=True))
    last_health_check = Column(DateTime(timezone=True))

    # Capabilities
    hardware_accel = Column(String(20))  # nvenc, qsv, amf, none
    max_parallel_jobs = Column(Integer, default=1)
    current_jobs = Column(Integer, default=0)

    # Performance tracking
    total_jobs = Column(Integer, default=0)
    successful_jobs = Column(Integer, default=0)
    failed_jobs = Column(Integer, default=0)
    average_speed = Column(Float)  # Average encoding speed multiplier

    # Load
    cpu_usage = Column(Float)
    ram_usage = Column(Float)
    gpu_usage = Column(Float)

    # Network share
    use_network_share = Column(Boolean, default=False)
    share_path = Column(Text)

    # Enabled
    is_enabled = Column(Boolean, default=True)

    # Priority (higher = preferred)
    priority = Column(Integer, default=0)

    def __repr__(self):
        return f"<Worker(id={self.id}, name={self.name}, status={self.status})>"

    @property
    def url(self) -> str:
        """Get worker URL."""
        protocol = "https" if self.use_https else "http"
        return f"{protocol}://{self.host}:{self.port}"

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_jobs == 0:
            return 0.0
        return self.successful_jobs / self.total_jobs
