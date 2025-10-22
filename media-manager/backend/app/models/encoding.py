"""Encoding database models."""

from sqlalchemy import Boolean, Column, Float, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base
from app.models.base import EncodingStatus, TimestampMixin, WorkerType


class EncodingPreset(Base, TimestampMixin):
    """Encoding preset model."""

    __tablename__ = "encoding_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    is_system = Column(Boolean, default=False)  # System presets can't be deleted

    # Video settings
    video_codec = Column(String(20), default="hevc")  # hevc, h264, av1
    video_encoder = Column(String(50), default="libx265")  # libx265, hevc_nvenc, etc.
    quality_mode = Column(String(20), default="crf")  # crf, bitrate, filesize
    crf = Column(Integer, default=23)
    bitrate = Column(Integer)  # Target bitrate in kbps
    preset = Column(String(20), default="medium")  # ultrafast to veryslow
    tune = Column(String(20))  # film, animation, grain, etc.
    two_pass = Column(Boolean, default=False)

    # Resolution
    target_resolution = Column(String(20))  # original, 4k, 1080p, 720p, custom
    scale_algorithm = Column(String(20), default="lanczos")

    # Audio settings
    audio_codec = Column(String(20), default="aac")  # aac, opus, ac3, copy
    audio_bitrate = Column(Integer, default=192)  # kbps
    audio_channels = Column(String(20), default="original")  # original, stereo, 5.1, 7.1
    keep_all_audio = Column(Boolean, default=True)

    # Subtitle settings
    keep_all_subtitles = Column(Boolean, default=True)
    subtitle_languages = Column(JSON)  # List of language codes
    burn_subtitles = Column(Boolean, default=False)

    # Container
    output_format = Column(String(10), default="mkv")  # mkv, mp4, webm
    copy_metadata = Column(Boolean, default=True)
    copy_chapters = Column(Boolean, default=True)

    # Advanced
    custom_ffmpeg_params = Column(Text)  # Custom FFmpeg parameters

    # Full configuration as JSON for easy import/export
    config_json = Column(JSON)

    def __repr__(self):
        return f"<EncodingPreset(id={self.id}, name={self.name})>"


class EncodingJob(Base, TimestampMixin):
    """Encoding job model."""

    __tablename__ = "encoding_jobs"

    id = Column(Integer, primary_key=True, index=True)
    download_id = Column(Integer, index=True)  # FK to download
    preset_id = Column(Integer, index=True)  # FK to preset

    # File info
    input_file = Column(Text, nullable=False)
    output_file = Column(Text, nullable=False)
    input_size = Column(Integer)  # Bytes
    output_size = Column(Integer)  # Bytes

    # Status
    status = Column(String(20), default=EncodingStatus.PENDING.value, index=True)
    progress = Column(Float, default=0.0)  # Percentage 0-100
    fps = Column(Float)  # Current encoding FPS
    eta = Column(Integer)  # Estimated time remaining in seconds
    speed = Column(Float)  # Encoding speed multiplier (e.g., 1.5x)

    # Worker
    worker_type = Column(String(20), default=WorkerType.SERVER.value)
    worker_id = Column(Integer)  # FK to worker
    worker_host = Column(String(255))

    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)

    # Statistics
    duration = Column(Integer)  # Encoding duration in seconds
    compression_ratio = Column(Float)  # output_size / input_size

    # FFmpeg command for reference/debugging
    ffmpeg_command = Column(Text)

    def __repr__(self):
        return f"<EncodingJob(id={self.id}, status={self.status}, progress={self.progress}%)>"
