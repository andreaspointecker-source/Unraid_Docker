"""TMDB metadata database model."""

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base
from app.models.base import MediaType, MetadataStatus, TimestampMixin


class MediaMetadata(Base, TimestampMixin):
    """TMDB metadata model."""

    __tablename__ = "media_metadata"

    id = Column(Integer, primary_key=True, index=True)
    download_id = Column(Integer, index=True)  # FK to download

    # File info
    file_path = Column(Text, nullable=False)
    original_filename = Column(String(500))

    # Detected info (from filename)
    detected_title = Column(String(500))
    detected_year = Column(Integer)
    detected_season = Column(Integer)
    detected_episode = Column(Integer)

    # Media type
    media_type = Column(String(20), default=MediaType.UNKNOWN.value)  # movie, tv, unknown

    # TMDB info
    tmdb_id = Column(Integer, index=True)
    imdb_id = Column(String(20))
    title = Column(String(500))
    original_title = Column(String(500))
    year = Column(Integer)
    overview = Column(Text)
    tagline = Column(Text)

    # TV-specific
    tv_show_id = Column(Integer)  # TMDB TV show ID
    season_number = Column(Integer)
    episode_number = Column(Integer)
    episode_title = Column(String(500))

    # Media details
    runtime = Column(Integer)  # Minutes
    genres = Column(JSON)  # List of genre names
    rating = Column(Float)  # TMDB vote average
    vote_count = Column(Integer)

    # Images
    poster_url = Column(Text)
    poster_path = Column(Text)  # Local path after download
    fanart_url = Column(Text)
    fanart_path = Column(Text)  # Local path after download

    # Status
    status = Column(String(20), default=MetadataStatus.PENDING.value, index=True)
    confidence = Column(Float, default=0.0)  # Match confidence 0-1
    manual_selection = Column(Integer)  # Set if user manually selected from results

    # Multiple results for manual selection
    search_results = Column(JSON)  # List of potential matches

    # Generated NFO path
    nfo_path = Column(Text)

    # Error handling
    error_message = Column(Text)

    def __repr__(self):
        return f"<MediaMetadata(id={self.id}, title={self.title}, status={self.status})>"
