# Docker Media Manager

A comprehensive Docker container for Unraid that combines automated downloading, archive extraction, video conversion, and media management into a modern web application.

## Features

### Download Manager
- **Link Grabber**: Automatically detect and extract download links from text
- **Premium Support**: RapidGator and DDownload integration
- **Multi-threaded Downloads**: Fast, reliable downloads using aria2c
- **Queue Management**: Prioritize, pause, resume, and retry downloads
- **Multiple Accounts**: Manage and rotate premium accounts

### Archive Extraction
- **Format Support**: ZIP, RAR, 7z, TAR, and nested archives
- **Password Manager**: Store and automatically try multiple passwords
- **Error Handling**: Quarantine corrupted files for manual review
- **Auto-cleanup**: Remove temporary files after successful extraction

### Video Conversion
- **HEVC/H.265**: High-quality video encoding with configurable presets
- **Flexible Compression**: CRF, bitrate, and custom FFmpeg options
- **Distributed Encoding**: Offload encoding to remote PC with hardware acceleration
- **Custom Presets**: Create, import, and export your own encoding profiles
- **Hardware Acceleration**: Support for NVENC, QSV, and AMF

### TMDB Integration
- **Auto-detection**: Automatically identify movies and TV shows
- **Rich Metadata**: Download posters, fanart, and NFO files
- **Manual Selection**: Choose the correct match when automatic detection is ambiguous
- **Kodi/Plex Compatible**: Generate NFO files compatible with popular media servers

### File Organization
- **Automatic Renaming**: Organize files with configurable naming schemas
- **Structured Storage**:
  - Movies: `Filmname (Jahr)/Filmname (Jahr).mkv`
  - TV Shows: `Serienname/XX/SXXEXX - Episodentitel.mkv`
- **Smart Cleanup**: Remove original files after successful processing

### Modern Web Interface
- **Dashboard**: Real-time overview of downloads, encoding, and tasks
- **Queue Management**: Monitor and control all processing stages
- **Comprehensive Settings**: Configure every aspect of the application
- **Dark/Light Mode**: Choose your preferred theme
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Docker Compose

```yaml
version: '3.8'

services:
  docker-media-manager:
    image: docker-media-manager:latest
    container_name: docker-media-manager
    ports:
      - "8080:8080"
    volumes:
      - ./config:/config
      - ./downloads:/downloads
      - ./media:/media
      - ./cache:/cache
    environment:
      - PUID=99
      - PGID=100
      - TZ=Europe/Berlin
      - TMDB_API_KEY=your_api_key_here
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

Access the web interface at: http://localhost:8080

## Documentation

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Configuration Guide](docs/configuration.md) - Configure settings and features
- [User Guide](docs/user-guide.md) - How to use the application
- [API Documentation](docs/api.md) - REST API reference
- [Remote Worker Setup](docs/remote-worker.md) - Set up distributed encoding

## Requirements

- Docker 20.10+
- Docker Compose 1.29+ (for Docker Compose setup)
- 2GB RAM minimum (4GB+ recommended)
- 10GB free disk space (for downloads and processing)

### Optional
- TMDB API Key (free, required for metadata features)
- Premium filehosting accounts (RapidGator, DDownload)
- Remote PC for hardware-accelerated encoding

## Technology Stack

**Backend**:
- Python 3.11+ with FastAPI
- SQLite database
- Celery for background tasks
- aria2c for downloads
- FFmpeg for video conversion

**Frontend**:
- React 18 with TypeScript
- Material-UI for components
- Vite for building
- Socket.IO for real-time updates

## Project Status

**Current Version**: Development (v1.0-alpha)

See [tasks.md](tasks.md) for development progress and roadmap.

## Contributing

This is currently in active development. Contributions, bug reports, and feature requests are welcome!

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/yourusername/docker-media-manager/issues)
- Documentation: [docs/](docs/)

## Acknowledgments

- FastAPI for the excellent Python web framework
- aria2 for reliable download management
- FFmpeg for powerful video processing
- TMDB for comprehensive movie/TV metadata

---

Built with ❤️ for the Unraid community
