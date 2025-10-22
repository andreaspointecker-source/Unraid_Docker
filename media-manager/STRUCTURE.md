# Project Structure

This document describes the complete folder structure of the Docker Media Manager project.

## Root Directory

```
docker-media-manager/
├── backend/                    # Python FastAPI backend
├── frontend/                   # React TypeScript frontend
├── worker/                     # Remote encoding worker
├── docker/                     # Docker configuration files
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── config/                     # Configuration files
├── data/                       # Runtime data (not in git)
├── logs/                       # Application logs (not in git)
├── .github/                    # GitHub workflows
├── plan.md                     # Project plan and architecture
├── tasks.md                    # Development tasks and roadmap
├── ai.md                       # AI assistant instructions
├── README.md                   # Project overview
├── STRUCTURE.md                # This file
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
├── Dockerfile                  # Main Docker image
├── docker-compose.yml          # Docker Compose configuration
└── LICENSE                     # License file
```

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection and setup
│   │
│   ├── api/                    # REST API endpoints
│   │   ├── __init__.py
│   │   ├── downloads.py        # Download management endpoints
│   │   ├── encoding.py         # Encoding management endpoints
│   │   ├── tmdb.py             # TMDB integration endpoints
│   │   ├── settings.py         # Settings management endpoints
│   │   ├── accounts.py         # Premium account endpoints
│   │   ├── passwords.py        # Password management endpoints
│   │   ├── workers.py          # Remote worker endpoints
│   │   ├── organize.py         # File organization endpoints
│   │   ├── health.py           # Health check endpoint
│   │   └── websocket.py        # WebSocket handlers
│   │
│   ├── models/                 # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── download.py         # Download model
│   │   ├── encoding.py         # Encoding job model
│   │   ├── metadata.py         # TMDB metadata model
│   │   ├── account.py          # Premium account model
│   │   ├── password.py         # Archive password model
│   │   ├── preset.py           # Encoding preset model
│   │   ├── worker.py           # Remote worker model
│   │   └── settings.py         # Application settings model
│   │
│   ├── schemas/                # Pydantic schemas for API validation
│   │   ├── __init__.py
│   │   ├── download.py         # Download request/response schemas
│   │   ├── encoding.py         # Encoding schemas
│   │   ├── tmdb.py             # TMDB schemas
│   │   ├── account.py          # Account schemas
│   │   ├── password.py         # Password schemas
│   │   ├── preset.py           # Preset schemas
│   │   ├── worker.py           # Worker schemas
│   │   └── settings.py         # Settings schemas
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── download_service.py         # Download management
│   │   ├── extraction_service.py       # Archive extraction
│   │   ├── encoding_service.py         # Video encoding
│   │   ├── tmdb_service.py             # TMDB metadata fetching
│   │   ├── organization_service.py     # File organization
│   │   ├── worker_service.py           # Remote worker management
│   │   ├── account_service.py          # Premium account management
│   │   ├── password_service.py         # Password management
│   │   └── filehoster/                 # Filehoster integrations
│   │       ├── __init__.py
│   │       ├── base.py                 # Base filehoster class
│   │       ├── rapidgator.py           # RapidGator implementation
│   │       └── ddownload.py            # DDownload implementation
│   │
│   ├── workers/                # Celery background tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py       # Celery configuration
│   │   ├── download_worker.py  # Download monitoring tasks
│   │   ├── encoding_worker.py  # Encoding tasks
│   │   ├── pipeline_worker.py  # Pipeline orchestration
│   │   └── cleanup_worker.py   # Cleanup tasks
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── encryption.py       # Password/API key encryption
│       ├── filename.py         # Filename parsing and generation
│       ├── validation.py       # Input validation helpers
│       ├── formatting.py       # Data formatting (bytes, time, etc.)
│       ├── ffmpeg.py           # FFmpeg command builder
│       └── helpers.py          # Generic helper functions
│
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures
│   ├── test_downloads.py       # Download service tests
│   ├── test_extraction.py      # Extraction service tests
│   ├── test_encoding.py        # Encoding service tests
│   ├── test_tmdb.py            # TMDB service tests
│   ├── test_organization.py    # Organization service tests
│   └── test_api/               # API endpoint tests
│       ├── test_downloads_api.py
│       ├── test_encoding_api.py
│       └── test_settings_api.py
│
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
│
├── requirements.txt            # Python dependencies
└── pytest.ini                  # Pytest configuration
```

## Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx                # Application entry point
│   ├── App.tsx                 # Root component
│   ├── theme.ts                # MUI theme configuration
│   │
│   ├── pages/                  # Page components
│   │   ├── Dashboard.tsx       # Main dashboard
│   │   ├── Queue.tsx           # Queue management page
│   │   ├── Settings.tsx        # Settings page
│   │   ├── Logs.tsx            # Logs viewer
│   │   └── NotFound.tsx        # 404 page
│   │
│   ├── components/             # Reusable components
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── MainLayout.tsx
│   │   │
│   │   ├── Downloads/
│   │   │   ├── DownloadList.tsx
│   │   │   ├── DownloadItem.tsx
│   │   │   ├── AddDownloadModal.tsx
│   │   │   └── DownloadStats.tsx
│   │   │
│   │   ├── Encoding/
│   │   │   ├── EncodingQueue.tsx
│   │   │   ├── EncodingItem.tsx
│   │   │   ├── EncodingSettings.tsx
│   │   │   ├── PresetManager.tsx
│   │   │   ├── PresetEditor.tsx
│   │   │   └── WorkerStatus.tsx
│   │   │
│   │   ├── TMDB/
│   │   │   ├── MetadataMatch.tsx
│   │   │   ├── MetadataPreview.tsx
│   │   │   └── ManualSearch.tsx
│   │   │
│   │   └── Common/
│   │       ├── ProgressBar.tsx
│   │       ├── StatusBadge.tsx
│   │       ├── ConfirmDialog.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── ErrorBoundary.tsx
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useDownloads.ts     # Download management hook
│   │   ├── useEncoding.ts      # Encoding management hook
│   │   ├── useWebSocket.ts     # WebSocket connection hook
│   │   ├── useSettings.ts      # Settings management hook
│   │   └── useTheme.ts         # Theme management hook
│   │
│   ├── store/                  # Zustand state management
│   │   ├── downloads.ts        # Download state
│   │   ├── encoding.ts         # Encoding state
│   │   ├── settings.ts         # Settings state
│   │   ├── notifications.ts    # Notifications state
│   │   └── theme.ts            # Theme state
│   │
│   ├── api/                    # API client layer
│   │   ├── client.ts           # Axios configuration
│   │   ├── downloads.ts        # Download API calls
│   │   ├── encoding.ts         # Encoding API calls
│   │   ├── tmdb.ts             # TMDB API calls
│   │   ├── settings.ts         # Settings API calls
│   │   ├── accounts.ts         # Account API calls
│   │   ├── passwords.ts        # Password API calls
│   │   └── workers.ts          # Worker API calls
│   │
│   ├── types/                  # TypeScript type definitions
│   │   ├── download.ts         # Download types
│   │   ├── encoding.ts         # Encoding types
│   │   ├── tmdb.ts             # TMDB types
│   │   ├── settings.ts         # Settings types
│   │   ├── account.ts          # Account types
│   │   ├── password.ts         # Password types
│   │   └── common.ts           # Common types
│   │
│   └── utils/                  # Utility functions
│       ├── format.ts           # Formatting functions (bytes, time, etc.)
│       ├── validation.ts       # Form validation
│       └── constants.ts        # Constants and enums
│
├── public/                     # Static assets
│   ├── favicon.ico
│   └── logo.png
│
├── package.json                # NPM dependencies
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript configuration
└── tsconfig.node.json          # TypeScript node configuration
```

## Worker Structure

```
worker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Worker API server
│   ├── config.py               # Worker configuration
│   ├── encoding.py             # Encoding logic
│   └── utils.py                # Utility functions
│
├── Dockerfile                  # Worker Docker image
├── docker-compose.yml          # Worker Docker Compose
├── requirements.txt            # Worker dependencies
└── README.md                   # Worker setup instructions
```

## Docker Configuration

```
docker/
├── entrypoint.sh               # Container entrypoint script
├── supervisord.conf            # Supervisor configuration
├── aria2.conf                  # aria2c configuration
└── nginx.conf                  # Nginx configuration (optional)
```

## Documentation

```
docs/
├── installation.md             # Installation guide
├── configuration.md            # Configuration guide
├── user-guide.md               # User guide
├── api.md                      # API documentation
├── remote-worker.md            # Remote worker setup
├── troubleshooting.md          # Troubleshooting guide
└── development.md              # Development guide
```

## Scripts

```
scripts/
├── build.sh                    # Build Docker image
├── test.sh                     # Run tests
├── migrate.sh                  # Run database migrations
└── on-download-complete.sh     # aria2c download complete hook
```

## Data Directories (Not in Git)

```
data/
├── downloads/                  # Download storage
│   ├── incomplete/             # Active downloads
│   ├── complete/               # Completed downloads
│   ├── extracted/              # Extracted files
│   └── quarantine/             # Failed/corrupted files
│
├── media/                      # Organized media
│   ├── movies/                 # Movies
│   │   └── Filmname (Jahr)/
│   │       ├── Filmname (Jahr).mkv
│   │       ├── poster.jpg
│   │       ├── fanart.jpg
│   │       └── movie.nfo
│   │
│   └── tv/                     # TV Shows
│       └── Serienname/
│           ├── poster.jpg
│           ├── fanart.jpg
│           ├── tvshow.nfo
│           └── 01/
│               ├── S01E01 - Episodentitel.mkv
│               └── S01E01.nfo
│
└── cache/                      # Cache storage
    ├── tmdb/                   # TMDB API cache
    └── thumbnails/             # Video thumbnails
```

## Configuration Directory

```
config/
├── database.db                 # SQLite database
├── passwords.enc               # Encrypted passwords
├── accounts.enc                # Encrypted accounts
├── encryption.key              # Encryption key
├── aria2.session               # aria2c session
├── presets/                    # Custom encoding presets
│   ├── my-preset-1.json
│   └── my-preset-2.json
└── logs/                       # Application logs
    ├── app.log
    ├── download.log
    ├── encoding.log
    └── tmdb.log
```

## GitHub Workflows

```
.github/
└── workflows/
    ├── test.yml                # Run tests on push
    ├── build.yml               # Build Docker image
    └── release.yml             # Create release
```

---

## Key Design Principles

1. **Separation of Concerns**: Backend, frontend, and worker are separate components
2. **Modular Architecture**: Services, models, and API endpoints are cleanly separated
3. **Type Safety**: TypeScript for frontend, type hints for Python backend
4. **Testability**: Clear structure with dedicated test directories
5. **Scalability**: Background workers for heavy tasks, WebSocket for real-time updates
6. **Security**: Encrypted storage for sensitive data, validation at API boundaries
7. **Docker-First**: Everything runs in containers for easy deployment

---

**Last Updated**: 2025-10-22
**Version**: 1.0
