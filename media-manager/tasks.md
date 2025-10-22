# Docker Media Manager - Development Tasks

## Development Phases

### Phase 1: Project Setup & Core Infrastructure (Week 1)

#### 1.1 Project Initialization
- [x] Create project folder structure
- [x] Create documentation (plan.md, tasks.md, ai.md, STRUCTURE.md)
- [x] Initialize Git repository
- [x] Setup .gitignore (Python, Node, Docker, IDE files)
- [x] Setup .gitattributes for line endings
- [x] Create README.md with project description

#### 1.2 Docker Infrastructure
- [x] Create base Dockerfile (multi-stage build)
- [x] Create docker-compose.yml for production
- [x] Create docker-compose.dev.yml for development
- [x] Create Dockerfile.dev for development hot-reload
- [x] Configure volume mappings
- [x] Setup environment variables template (.env.example)
- [x] Create entrypoint.sh script
- [x] Create supervisord.conf for process management
- [x] Create aria2.conf configuration
- [ ] Test Docker build and startup

#### 1.3 Backend Foundation
- [x] Create requirements.txt with all dependencies
- [x] Initialize FastAPI application structure (main.py)
- [x] Create config.py for settings management
- [x] Setup database.py with SQLAlchemy
- [x] Create database models:
  - [x] Base models and enums
  - [x] Download model
  - [x] Encoding models (Job, Preset)
  - [x] Metadata model
  - [x] Account model
  - [x] Password model
  - [x] Worker model
- [x] Create health check endpoint
- [x] Implement logging configuration
- [ ] Create database migration system (Alembic) - deferred to Phase 2

#### 1.4 Frontend Foundation
- [x] Initialize Vite + React project (package.json, vite.config.ts)
- [x] Create TypeScript configuration (tsconfig.json)
- [x] Setup MUI theme (light & dark mode)
- [x] Create App.tsx with routing
- [x] Setup basic routing (/, /queue, /settings, /logs)
- [x] Create MainLayout component (Header, Sidebar)
- [x] Create all page components:
  - [x] Dashboard (with health check integration)
  - [x] Queue (with tabs for different queue types)
  - [x] Settings (placeholder)
  - [x] Logs (placeholder)
  - [x] NotFound (404 page)
- [x] Implement Dark/Light theme toggle
- [x] Setup React Query for API calls

---

### Phase 2: Download-Manager (Week 2-3)

#### 2.1 aria2c Integration
- [ ] Install and configure aria2c in Docker
- [ ] Create aria2c RPC client wrapper
- [ ] Implement download service:
  - Add download
  - Pause/Resume
  - Cancel
  - Get status/progress
- [ ] Setup aria2c configuration (connections, chunk size)
- [ ] Test multi-threaded downloads

#### 2.2 Link-Grabber
- [ ] Implement URL pattern detection
- [ ] Create link extraction from text/HTML
- [ ] Support for:
  - Direct links
  - RapidGator links
  - DDownload links
- [ ] Bulk link import (paste multiple URLs)
- [ ] Link validation

#### 2.3 Premium Account Management
- [ ] Create account storage model (encrypted)
- [ ] Implement RapidGator API integration:
  - Login/Session management
  - Premium link generation
  - Account status check
- [ ] Implement DDownload API integration:
  - Login/Session management
  - Premium link generation
  - Account status check
- [ ] Account rotation (multiple accounts)
- [ ] Account health monitoring

#### 2.4 Download Queue & Management
- [ ] Create download queue model
- [ ] Implement queue prioritization
- [ ] Add download history
- [ ] Retry logic for failed downloads
- [ ] Bandwidth limiting (optional)
- [ ] Schedule downloads (optional)

#### 2.5 Frontend: Download Manager
- [ ] Create "Add Download" modal/form
- [ ] Build download queue view with:
  - Status (queued, downloading, completed, failed)
  - Progress bars
  - Speed & ETA
  - Actions (pause, resume, cancel, retry)
- [ ] Implement real-time updates via WebSocket
- [ ] Create download history page
- [ ] Account management UI

#### 2.6 API Endpoints
- [ ] POST /api/downloads/add
- [ ] GET /api/downloads/list
- [ ] GET /api/downloads/{id}
- [ ] POST /api/downloads/{id}/pause
- [ ] POST /api/downloads/{id}/resume
- [ ] DELETE /api/downloads/{id}
- [ ] GET /api/downloads/history
- [ ] POST /api/accounts/add
- [ ] GET /api/accounts/list
- [ ] DELETE /api/accounts/{id}

---

### Phase 3: Archive Extraction (Week 3-4)

#### 3.1 Extraction Service
- [ ] Install extraction tools in Docker (unrar, 7zip, unzip)
- [ ] Implement extraction service using patool
- [ ] Support formats: ZIP, RAR, 7z, TAR, GZ
- [ ] Handle nested archives (recursive extraction)
- [ ] Detect archive passwords

#### 3.2 Password Management
- [ ] Create password storage model (encrypted)
- [ ] Implement password try logic:
  - Try all stored passwords
  - Track which password worked
  - Learn successful passwords
- [ ] Add new passwords from UI
- [ ] Password success statistics

#### 3.3 Error Handling
- [ ] Detect corrupted archives
- [ ] Move failed files to quarantine
- [ ] Retry extraction with different tools
- [ ] Log extraction errors with details

#### 3.4 Frontend: Extraction
- [ ] Show extraction status in queue
- [ ] Password manager UI
- [ ] Quarantine file viewer
- [ ] Manual password input for failed extractions

#### 3.5 API Endpoints
- [ ] POST /api/passwords/add
- [ ] GET /api/passwords/list
- [ ] DELETE /api/passwords/{id}
- [ ] GET /api/quarantine/list
- [ ] POST /api/quarantine/{id}/retry

---

### Phase 4: Video Conversion - Local (Week 4-5)

#### 4.1 FFmpeg Integration
- [ ] Install FFmpeg in Docker with codecs:
  - libx265 (HEVC)
  - libx264 (H.264)
  - libaom-av1 (AV1, optional)
  - Hardware encoder support (NVENC, QSV, AMF)
- [ ] Create FFmpeg wrapper service
- [ ] Implement video analysis:
  - Duration, resolution, codec
  - Bitrate, frame rate
  - Audio tracks, subtitles

#### 4.2 Encoding Presets
- [ ] Define system presets:
  - High Quality (CRF 20, slow, 2-pass)
  - Balanced (CRF 23, medium, 1-pass)
  - High Compression (CRF 26, slow, 2-pass)
  - Fast (CRF 25, veryfast, 1-pass)
- [ ] Create preset model and storage
- [ ] Implement preset CRUD operations
- [ ] Preset import/export (JSON)

#### 4.3 Encoding Service
- [ ] Implement encoding pipeline:
  - Video codec (HEVC/H.264/AV1)
  - Quality mode (CRF/Bitrate/File size)
  - Preset (ultrafast → veryslow)
  - Resolution scaling
  - Audio codec & bitrate
  - Subtitle handling
- [ ] Two-pass encoding support
- [ ] Progress tracking (percentage, FPS, ETA)
- [ ] Hardware acceleration detection & usage
- [ ] Error handling & retry logic

#### 4.4 Encoding Queue
- [ ] Create encoding queue model
- [ ] Priority management
- [ ] Parallel encoding limit
- [ ] Worker status (idle, busy, failed)
- [ ] Encoding history & statistics

#### 4.5 Frontend: Encoding Settings
- [ ] Build comprehensive settings UI:
  - Preset selector
  - Video codec & quality sliders
  - Resolution dropdown
  - Audio settings
  - Advanced FFmpeg options
- [ ] Preset management page:
  - Create, edit, delete custom presets
  - Import/export presets
  - Duplicate system presets
- [ ] FFmpeg command preview
- [ ] Encoding queue view with progress
- [ ] Per-download encoding override

#### 4.6 API Endpoints
- [ ] GET /api/encoding/presets
- [ ] POST /api/encoding/presets
- [ ] PUT /api/encoding/presets/{id}
- [ ] DELETE /api/encoding/presets/{id}
- [ ] POST /api/encoding/presets/import
- [ ] GET /api/encoding/presets/{id}/export
- [ ] GET /api/encoding/queue
- [ ] POST /api/encoding/start
- [ ] POST /api/encoding/{id}/cancel
- [ ] GET /api/encoding/{id}/progress

---

### Phase 5: Video Conversion - Remote Worker (Week 5-6)

#### 5.1 Remote Worker Architecture
- [ ] Design worker API specification
- [ ] Create separate worker project:
  - Lightweight FastAPI server
  - FFmpeg integration
  - File transfer handling
  - Progress reporting
- [ ] Implement authentication (API key)
- [ ] WebSocket for real-time updates

#### 5.2 Worker Communication
- [ ] Create worker client in main app
- [ ] Implement worker discovery/registration
- [ ] Health check / heartbeat system (30s interval)
- [ ] Job submission to worker
- [ ] Progress tracking from worker
- [ ] File transfer (chunked upload/download)

#### 5.3 Encoding Strategy
- [ ] Implement worker selection logic:
  - Prefer Remote PC
  - Remote Only
  - Server Only
  - Load Balancing
- [ ] Automatic fallback on worker failure
- [ ] Job migration (PC → Server)
- [ ] Network share support (no transfer)

#### 5.4 Worker Deployment
- [ ] Create worker Dockerfile
- [ ] Create docker-compose for worker
- [ ] Windows standalone script
- [ ] Worker configuration (hardware accel)
- [ ] Worker documentation

#### 5.5 Frontend: Worker Management
- [ ] Worker status dashboard:
  - Online/Offline status
  - Current load
  - Active jobs
  - Hardware info
- [ ] Worker configuration UI:
  - Add/remove workers
  - Test connection
  - Set hardware acceleration
- [ ] Encoding strategy selector
- [ ] Worker logs viewer

#### 5.6 API Endpoints (Main App)
- [ ] GET /api/workers/list
- [ ] POST /api/workers/add
- [ ] DELETE /api/workers/{id}
- [ ] POST /api/workers/{id}/test
- [ ] GET /api/workers/{id}/status

#### 5.7 API Endpoints (Worker)
- [ ] POST /api/worker/auth
- [ ] POST /api/worker/job
- [ ] GET /api/worker/job/{id}/status
- [ ] POST /api/worker/job/{id}/cancel
- [ ] POST /api/worker/upload (chunked)
- [ ] GET /api/worker/download/{id} (chunked)
- [ ] GET /api/worker/health

---

### Phase 6: TMDB Integration (Week 6-7)

#### 6.1 TMDB Service
- [ ] Setup TMDB API client (tmdbsimple)
- [ ] Implement search functionality:
  - Movie search by title + year
  - TV show search by title
  - Multi-search (auto-detect)
- [ ] Get detailed metadata:
  - Title, year, overview
  - Genres, cast, crew
  - Ratings, runtime
- [ ] Download images:
  - Poster (multiple sizes)
  - Fanart/Backdrop
  - Season/Episode images (TV)
- [ ] Generate NFO files (Kodi/Plex format)

#### 6.2 Filename Parsing
- [ ] Implement guessit integration
- [ ] Extract from filename:
  - Title
  - Year
  - Season/Episode (TV)
  - Quality (1080p, 4K, etc.)
  - Release group
- [ ] Confidence scoring
- [ ] Manual override option

#### 6.3 Metadata Management
- [ ] Create metadata model
- [ ] Implement metadata matching logic:
  - Automatic match (high confidence)
  - Manual selection (multiple results)
  - Skip (no match)
- [ ] Metadata cache (avoid duplicate API calls)
- [ ] Language preference

#### 6.4 NFO Generation
- [ ] Movie NFO format (Kodi/Plex compatible)
- [ ] TV Show NFO format
- [ ] Episode NFO format
- [ ] Include all relevant metadata fields

#### 6.5 Frontend: TMDB Integration
- [ ] Metadata matching interface:
  - Show detected info
  - Display TMDB search results
  - Manual selection UI
  - Preview metadata + images
- [ ] Metadata queue view
- [ ] Failed matches list (manual intervention)
- [ ] TMDB settings:
  - API key configuration
  - Language preference
  - Auto-match threshold

#### 6.6 API Endpoints
- [ ] POST /api/tmdb/search/movie
- [ ] POST /api/tmdb/search/tv
- [ ] GET /api/tmdb/movie/{id}
- [ ] GET /api/tmdb/tv/{id}
- [ ] POST /api/metadata/match
- [ ] POST /api/metadata/{id}/manual-select
- [ ] GET /api/metadata/queue
- [ ] GET /api/metadata/failed

---

### Phase 7: File Organization (Week 7)

#### 7.1 File Organization Service
- [ ] Implement file moving/copying
- [ ] Generate destination paths:
  - Movies: `Filmname (Jahr)/Filmname (Jahr).mkv`
  - TV: `Serienname/XX/SXXEXX - Episodentitel.mkv`
- [ ] Handle name collisions (append number)
- [ ] Verify file integrity after move
- [ ] Atomic operations (move = copy + verify + delete)

#### 7.2 Naming Schemas
- [ ] Create configurable naming templates:
  - Movie: `{title} ({year})`
  - TV Show: `S{season:02d}E{episode:02d} - {title}`
- [ ] Support variables:
  - {title}, {year}, {season}, {episode}
  - {quality}, {codec}, {audio}
- [ ] Preview renaming before execution

#### 7.3 Cleanup Service
- [ ] Delete original files after successful processing
- [ ] Delete temporary files (extracted archives)
- [ ] Delete empty directories
- [ ] Configurable retention policy:
  - Keep original always
  - Keep original only on error
  - Always delete original
- [ ] Backup option (move to backup dir instead of delete)

#### 7.4 Frontend: File Organization
- [ ] Organization settings:
  - Naming schema templates
  - Movie/TV folder paths
  - Cleanup policy
- [ ] Organization preview (before execution)
- [ ] Manual organize trigger

#### 7.5 API Endpoints
- [ ] POST /api/organize/preview
- [ ] POST /api/organize/execute
- [ ] GET /api/organize/settings
- [ ] PUT /api/organize/settings

---

### Phase 8: Pipeline Automation (Week 8)

#### 8.1 Pipeline Orchestration
- [ ] Create pipeline orchestrator:
  - Download → Extract → Encode → TMDB → Organize
- [ ] Step configuration (enable/disable each step)
- [ ] Automatic progression through pipeline
- [ ] Error handling at each step
- [ ] Retry logic with backoff

#### 8.2 Background Tasks
- [ ] Setup Celery workers for:
  - Download monitoring
  - Extraction tasks
  - Encoding tasks
  - TMDB tasks
  - Organization tasks
  - Cleanup tasks
- [ ] Task scheduling (periodic checks)
- [ ] Task chaining (download → extract → ...)
- [ ] Task result tracking

#### 8.3 State Management
- [ ] Create state machine for files:
  - NEW → DOWNLOADING → DOWNLOADED
  - DOWNLOADED → EXTRACTING → EXTRACTED
  - EXTRACTED → ENCODING → ENCODED
  - ENCODED → MATCHING → MATCHED
  - MATCHED → ORGANIZING → COMPLETED
  - ANY → FAILED
- [ ] State transitions and validation
- [ ] State persistence in database

#### 8.4 Error Recovery
- [ ] Implement retry strategies:
  - Download failures: 3x retry
  - Extraction failures: try different tools
  - Encoding failures: fallback to server
  - TMDB failures: manual intervention
- [ ] Error notifications in UI
- [ ] Manual retry triggers

#### 8.5 Frontend: Pipeline View
- [ ] Visual pipeline status:
  - Show current step for each item
  - Progress within step
  - Overall progress
- [ ] Pipeline configuration toggle:
  - Enable/disable steps
  - Configure retry behavior
- [ ] Failed items dashboard

#### 8.6 API Endpoints
- [ ] GET /api/pipeline/status
- [ ] GET /api/pipeline/settings
- [ ] PUT /api/pipeline/settings
- [ ] POST /api/pipeline/{id}/retry

---

### Phase 9: Web Interface Polish (Week 9)

#### 9.1 Dashboard
- [ ] Create main dashboard with:
  - Active downloads (count + total speed)
  - Encoding queue (count + progress)
  - Recent completions
  - Disk space usage
  - Error summary
- [ ] Real-time updates via WebSocket
- [ ] Quick actions (add download, view queue)

#### 9.2 Queue Management
- [ ] Unified queue view with tabs:
  - Downloads
  - Extractions
  - Encodings
  - TMDB Matching
  - Organizing
- [ ] Sorting and filtering
- [ ] Bulk actions (pause all, retry all failed)
- [ ] Search functionality

#### 9.3 Settings Page
- [ ] Organize settings into sections:
  - General (timezone, language)
  - Download (aria2c config, accounts)
  - Extraction (passwords, tools)
  - Encoding (presets, workers)
  - TMDB (API key, language)
  - Organization (naming, paths)
  - Pipeline (automation settings)
- [ ] Settings validation
- [ ] Save/Reset functionality
- [ ] Import/Export settings (backup)

#### 9.4 Logs & Debugging
- [ ] Log viewer in UI:
  - Filter by level (DEBUG, INFO, WARNING, ERROR)
  - Filter by component (download, encoding, etc.)
  - Search logs
  - Export logs
- [ ] Debug mode toggle
- [ ] System info page:
  - Docker version
  - FFmpeg version & codecs
  - Disk space
  - CPU/RAM usage

#### 9.5 UI/UX Improvements
- [ ] Loading states for all actions
- [ ] Error messages with helpful hints
- [ ] Confirmation dialogs for destructive actions
- [ ] Keyboard shortcuts
- [ ] Responsive design (mobile-friendly)
- [ ] Accessibility (ARIA labels)

#### 9.6 Notifications
- [ ] In-app notifications:
  - Download completed
  - Encoding finished
  - Errors occurred
- [ ] Notification center (list of all notifications)
- [ ] Dismiss/Clear notifications

---

### Phase 10: Testing & Quality Assurance (Week 10)

#### 10.1 Unit Tests
- [ ] Backend tests:
  - Service layer tests (download, extract, encode, tmdb)
  - Model tests
  - Utility function tests
  - API endpoint tests
- [ ] Test coverage > 70%
- [ ] Setup pytest fixtures

#### 10.2 Integration Tests
- [ ] Test full pipeline flow
- [ ] Test worker communication
- [ ] Test database operations
- [ ] Test file operations (with temp dirs)
- [ ] Test error scenarios

#### 10.3 End-to-End Tests
- [ ] Frontend E2E tests (Playwright):
  - Add download flow
  - Settings configuration
  - Queue management
- [ ] Test in Docker environment

#### 10.4 Performance Testing
- [ ] Load test with multiple simultaneous downloads
- [ ] Large file handling (> 20GB)
- [ ] Memory leak detection
- [ ] Database query optimization

#### 10.5 Security Testing
- [ ] Input validation (SQL injection, XSS)
- [ ] Authentication/Authorization tests
- [ ] File path traversal prevention
- [ ] Encrypted password storage verification

#### 10.6 Manual Testing
- [ ] Test on Windows Docker Desktop
- [ ] Test with real RapidGator/DDownload accounts
- [ ] Test various video formats
- [ ] Test TMDB matching accuracy
- [ ] Test remote worker setup

---

### Phase 11: Docker & Deployment (Week 11)

#### 11.1 Docker Optimization
- [ ] Multi-stage build optimization:
  - Separate build and runtime stages
  - Minimize image size
  - Layer caching optimization
- [ ] Alpine-based images where possible
- [ ] Non-root user execution
- [ ] Security scanning (Trivy)

#### 11.2 Docker Compose
- [ ] Production docker-compose.yml
- [ ] Development docker-compose.yml (with hot-reload)
- [ ] Environment variable configuration
- [ ] Volume configuration examples
- [ ] Network configuration

#### 11.3 Health Checks
- [ ] Docker HEALTHCHECK directive
- [ ] Health endpoint: GET /api/health
- [ ] Check database connectivity
- [ ] Check aria2c status
- [ ] Check disk space

#### 11.4 Logging & Monitoring
- [ ] Structured JSON logging
- [ ] Log rotation configuration
- [ ] Container logs to stdout/stderr
- [ ] Optional: Prometheus metrics endpoint

#### 11.5 Unraid Integration
- [ ] Create Unraid template XML
- [ ] Define container settings:
  - Name, icon, description
  - Port mappings (default 8080)
  - Volume mappings (with defaults)
  - Environment variables
- [ ] Test installation on Unraid
- [ ] Create Unraid installation guide

---

### Phase 12: Documentation (Week 12)

#### 12.1 README
- [ ] Project description and features
- [ ] Screenshots/GIFs of UI
- [ ] Quick start guide
- [ ] Requirements
- [ ] Links to detailed docs

#### 12.2 Installation Guide
- [ ] Docker Compose installation
- [ ] Unraid installation (step-by-step)
- [ ] Windows Docker Desktop installation
- [ ] Remote worker setup
- [ ] Troubleshooting common issues

#### 12.3 Configuration Guide
- [ ] Environment variables reference
- [ ] Volume structure explanation
- [ ] Settings overview
- [ ] Premium account setup
- [ ] TMDB API key setup

#### 12.4 User Guide
- [ ] Adding downloads
- [ ] Managing queue
- [ ] Configuring encoding
- [ ] TMDB matching
- [ ] Organizing media
- [ ] Setting up remote worker

#### 12.5 API Documentation
- [ ] OpenAPI/Swagger auto-generated docs
- [ ] API usage examples
- [ ] Authentication guide
- [ ] Webhook documentation (if implemented)

#### 12.6 Developer Guide
- [ ] Architecture overview
- [ ] Development setup
- [ ] Contributing guidelines
- [ ] Code style guide
- [ ] Testing guide

---

### Phase 13: Release Preparation (Week 13)

#### 13.1 Final Testing
- [ ] Full regression test
- [ ] Test on fresh Unraid installation
- [ ] Test with empty config
- [ ] Test upgrade path (future releases)

#### 13.2 Performance Tuning
- [ ] Profile and optimize bottlenecks
- [ ] Database query optimization
- [ ] Frontend bundle size optimization
- [ ] Docker image size reduction

#### 13.3 Security Audit
- [ ] Review authentication/authorization
- [ ] Check for hardcoded secrets
- [ ] Validate input sanitization
- [ ] Review file permissions

#### 13.4 Versioning
- [ ] Semantic versioning strategy
- [ ] Version displayed in UI
- [ ] CHANGELOG.md creation
- [ ] Git tagging strategy

#### 13.5 Release Assets
- [ ] Build Docker images (multi-arch: amd64, arm64)
- [ ] Push to Docker Hub
- [ ] Create GitHub release
- [ ] Attach binaries (worker script)

#### 13.6 Community Setup
- [ ] Create GitHub repository
- [ ] Setup issue templates
- [ ] Setup pull request template
- [ ] Create Discord/Forum for support
- [ ] Submit to Unraid Community Apps

---

## Post-Release Roadmap (Future Versions)

### v1.1 (Next Priority)
- [ ] More filehoster support (Uploaded, Mega, MediaFire)
- [ ] Subtitle download integration (OpenSubtitles)
- [ ] Notification system (Email, Telegram, Discord, Webhooks)
- [ ] Multi-language UI (i18n)
- [ ] Import from JDownloader (link list)

### v1.2
- [ ] Plugin system (custom download providers)
- [ ] Advanced statistics dashboard
- [ ] Media library viewer (browse organized media)
- [ ] Duplicate detection (skip already downloaded)
- [ ] Bandwidth scheduling (limit speed during hours)

### v2.0 (Major Features)
- [ ] Mobile app (React Native)
- [ ] Browser extension (link capture)
- [ ] Plex/Jellyfin integration (auto-refresh library)
- [ ] AI-powered TMDB matching (ML model)
- [ ] Torrent support (qBittorrent integration)

---

## Current Status

**Phase**: Not Started
**Last Updated**: 2025-10-22
**Current Sprint**: Phase 1 - Project Setup

---

## Task Tracking Legend

- [ ] Not started
- [~] In progress
- [x] Completed
- [!] Blocked
- [-] Skipped/Canceled

---

## Notes for AI Assistant

1. **Task Updates**: Always update this file when completing tasks
2. **New Tasks**: Add discovered tasks in appropriate phase
3. **Blockers**: Mark blocked tasks with [!] and add blocker note
4. **Time Estimates**: Adjust week estimates based on actual progress
5. **Priorities**: Focus on MVP features first (Phase 1-8)
6. **Testing**: Don't skip testing phases - quality is important
7. **Documentation**: Update docs as features are implemented, not at the end

---

## Development Guidelines

### Code Quality
- Follow PEP 8 for Python code
- Use type hints in Python
- Use TypeScript for Frontend (strict mode)
- Write docstrings for all functions
- Keep functions small and focused
- DRY principle (Don't Repeat Yourself)

### Git Workflow
- Feature branches: `feature/download-manager`
- Bugfix branches: `bugfix/aria2c-crash`
- Commit messages: Clear, descriptive (Conventional Commits)
- Squash commits before merge

### Testing Requirements
- Unit tests for all services
- Integration tests for API endpoints
- E2E tests for critical user flows
- Run tests before committing

### Documentation Requirements
- Update README for user-facing changes
- Update API docs for new endpoints
- Add inline comments for complex logic
- Update CHANGELOG for releases

---

**End of Tasks Document**
