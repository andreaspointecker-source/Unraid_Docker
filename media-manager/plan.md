# Docker Media Manager - Project Plan

## Projektübersicht

Ein Docker-Container für Unraid, der automatisiertes Downloaden, Entpacken, Video-Konvertierung und Medien-Management kombiniert. Ähnlich wie JDownloader + TinyMediaManager + FFmpeg in einer modernen Web-Anwendung.

## Zielgruppe

- Unraid-Server-Nutzer
- Mediensammler mit Premium-Filehosting-Accounts
- User mit separatem Encoding-PC für Hardware-Beschleunigung

## Hauptfunktionen

### 1. Download-Manager
- **Link-Grabber**: Automatische Link-Erkennung aus Text/URLs
- **Premium-Support**: RapidGator, DDownload Integration
- **Multi-Threading**: aria2c für schnelle, zuverlässige Downloads
- **Queue-Management**: Prioritäten, Pause/Resume, Auto-Retry
- **Account-Management**: Mehrere Premium-Accounts verwaltbar

### 2. Archiv-Extraktion
- **Format-Support**: ZIP, RAR, 7z, und verschachtelte Archive
- **Passwort-Manager**: Mehrere Passwörter speichern & automatisch ausprobieren
- **Fehlerbehandlung**: Beschädigte Archive in Quarantäne verschieben
- **Automatische Bereinigung**: Temp-Dateien nach erfolgreicher Extraktion löschen

### 3. Video-Konvertierung
- **Codec**: HEVC/H.265 mit konfigurierbaren Presets
- **Komprimierung**: CRF, Bitrate, 2-Pass, Custom-Settings
- **Verteiltes Encoding**:
  - Automatische Worker-Auswahl (Server vs. Remote-PC)
  - Hardware-Beschleunigung (NVENC, QSV, AMF)
  - Fallback-Logik bei Worker-Ausfall
- **Presets**: System-Presets + Custom-Presets (Import/Export)
- **Granulare Kontrolle**: Alle FFmpeg-Parameter konfigurierbar

### 4. TMDB-Integration
- **Automatische Erkennung**: Film/Serien-Matching via API
- **Metadaten-Download**: Poster, Fanart, NFO-Dateien
- **Manuelle Auswahl**: Bei mehrdeutigen Ergebnissen
- **NFO-Format**: Kompatibel mit Kodi/Plex/Jellyfin

### 5. Dateiorganisation
- **Automatisches Umbenennen**: Nach konfigurierbaren Schemas
- **Strukturierte Ablage**:
  - Filme: `Filmname (Jahr)/Filmname (Jahr).mkv`
  - Serien: `Serienname/XX/SXXEXX - Episodentitel.mkv`
- **Cleanup**: Originaldateien nach erfolgreicher Verarbeitung löschen
- **Fehler-Quarantäne**: Problematische Dateien isolieren

### 6. Web-Interface
- **Dashboard**: Übersicht über aktive Downloads/Tasks
- **Queue-View**: Download/Encoding/TMDB-Warteschlangen
- **Settings**: Umfassende Konfigurationsmöglichkeiten
- **Logs**: Fehlerübersicht und Debug-Informationen
- **Dark/Light Mode**: Benutzerfreundliches, modernes UI

## Technologie-Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
  - Beste async/await Performance für I/O-intensive Operationen
  - Automatische API-Dokumentation (OpenAPI/Swagger)
  - Type Hints für Code-Sicherheit
  - WebSocket-Support für Echtzeit-Updates

- **Download-Engine**: aria2c
  - Multi-threaded, sehr zuverlässig
  - Pause/Resume Support
  - RPC-Interface für Python-Integration

- **Task Queue**: Celery + Redis
  - Asynchrone Background-Tasks
  - Retry-Logik und Error-Handling
  - Distributed Task Execution

- **Datenbank**: SQLite
  - Leichtgewichtig, keine externe DB nötig
  - Speichert: Download-History, Settings, Passwörter, Accounts

- **Libraries**:
  - `pymediainfo`: Video-File-Analyse
  - `patool`: Universal Archive-Extraktion
  - `tmdbsimple`: TMDB-API-Client
  - `guessit`: Film/Serien-Erkennung aus Dateinamen
  - `cryptography`: Passwort/API-Key-Verschlüsselung

### Frontend
- **Framework**: React 18 + Vite
  - Schnelles Development und Build
  - Hot Module Replacement
  - Modern JavaScript/TypeScript

- **UI-Library**: Material-UI (MUI)
  - Professionelles, konsistentes Design
  - Responsive Components
  - Dark/Light Theme Support

- **State Management**: Zustand
  - Leichtgewichtig, einfache API
  - TypeScript-First

- **API-Client**: Axios + React Query
  - Automatisches Caching
  - Optimistic Updates
  - Error Handling

- **Real-time**: Socket.IO-Client
  - Echtzeit-Updates für Downloads/Encoding-Progress
  - Automatische Reconnection

### DevOps
- **Containerization**: Docker + Docker Compose
  - Multi-stage Builds für kleinere Images
  - Volume-Mapping für Unraid
  - Health Checks

- **Reverse Proxy**: Nginx (optional)
  - Serving static Frontend-Files
  - API-Proxying

- **Logging**: Python logging + rotating file handler
  - Structured Logs (JSON)
  - Log-Levels konfigurierbar

## Architektur

```
┌─────────────────────────────────────────────────────────┐
│                     Web Browser                         │
│              (React Frontend - Port 8080)               │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/WebSocket
┌─────────────────▼───────────────────────────────────────┐
│                  FastAPI Backend                        │
│  ┌──────────┬──────────┬──────────┬──────────────────┐  │
│  │   API    │ WebSocket│  Static  │   Auth/Session   │  │
│  │ Endpoints│  Server  │   Files  │                  │  │
│  └──────────┴──────────┴──────────┴──────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Service Layer                         │  │
│  │  ┌──────────┬──────────┬──────────┬─────────────┐ │  │
│  │  │ Download │ Extract  │ Encoding │    TMDB     │ │  │
│  │  │ Service  │ Service  │ Service  │   Service   │ │  │
│  │  └──────────┴──────────┴──────────┴─────────────┘ │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │            Celery Task Queue                       │  │
│  │        (Background Workers + Scheduler)            │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │         SQLite Database + Redis Cache              │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┬──────────────────┐
    │             │             │                  │
┌───▼────┐  ┌────▼─────┐  ┌────▼─────┐  ┌────────▼────────┐
│ aria2c │  │  FFmpeg  │  │  TMDB    │  │  Remote Worker  │
│  RPC   │  │  (Local) │  │   API    │  │  (Optional PC)  │
└────────┘  └──────────┘  └──────────┘  └─────────────────┘
```

## Workflow-Pipeline

```
1. Link hinzufügen
   ↓
2. Link-Grabber analysiert URLs
   ↓
3. Download startet (aria2c)
   ↓ [Status: Downloading]
4. Download abgeschlossen
   ↓
5. Archive extrahieren (mit Passwort-Try)
   ↓ [Status: Extracting]
6. Extraktion erfolgreich
   ↓
7. [Optional] Video konvertieren
   ↓ [Status: Encoding on Server/PC]
   │ ┌─ Worker-Auswahl:
   │ ├─ PC online? → Send to PC
   │ ├─ PC offline? → Use Server
   │ └─ PC failed? → Fallback to Server
   ↓
8. TMDB-Scan & Metadaten-Download
   ↓ [Status: Fetching Metadata]
   │ ┌─ Automatische Erkennung
   │ ├─ Falls mehrdeutig → User-Auswahl
   │ └─ Poster/Fanart/NFO herunterladen
   ↓
9. Datei organisieren & umbenennen
   ↓ [Status: Organizing]
   │ ┌─ Film → /media/movies/Filmname (Jahr)/
   │ └─ Serie → /media/tv/Serienname/XX/
   ↓
10. Cleanup: Temp-Dateien löschen
    ↓ [Status: Cleaning up]
11. Fertig ✓
    ↓ [Status: Completed]
```

Jeder Schritt kann in Settings aktiviert/deaktiviert werden.

## Volume-Struktur

```
/data/
├── downloads/          # Temporäre Downloads & Extraktion
│   ├── incomplete/     # Laufende Downloads
│   ├── complete/       # Fertige Downloads
│   ├── extracted/      # Entpackte Dateien
│   └── quarantine/     # Fehlerhafte Dateien
│
├── media/
│   ├── movies/         # Finale Filme
│   │   └── Filmname (Jahr)/
│   │       ├── Filmname (Jahr).mkv
│   │       ├── poster.jpg
│   │       ├── fanart.jpg
│   │       └── movie.nfo
│   │
│   └── tv/             # Finale Serien
│       └── Serienname/
│           ├── poster.jpg
│           ├── fanart.jpg
│           ├── tvshow.nfo
│           └── 01/
│               ├── S01E01 - Episodentitel.mkv
│               └── S01E01.nfo
│
├── config/             # Konfiguration & Datenbank
│   ├── settings.db     # SQLite-Datenbank
│   ├── passwords.enc   # Verschlüsselte Passwörter
│   ├── accounts.enc    # Verschlüsselte Premium-Accounts
│   ├── presets/        # Custom Encoding-Presets
│   │   └── *.json
│   └── logs/           # Application Logs
│       ├── app.log
│       ├── download.log
│       ├── encoding.log
│       └── tmdb.log
│
└── cache/              # Temporärer Cache
    ├── tmdb/           # TMDB-API-Responses
    └── thumbnails/     # Video-Thumbnails
```

## Docker-Konfiguration

### Environment Variables
```bash
# TMDB API
TMDB_API_KEY=your_api_key_here

# User/Group (Unraid)
PUID=99
PGID=100

# Timezone
TZ=Europe/Berlin

# Remote Worker (Optional)
REMOTE_WORKER_ENABLED=true
REMOTE_WORKER_URL=http://192.168.1.100:5000
REMOTE_WORKER_API_KEY=your_worker_api_key

# Encoding Strategy
ENCODING_STRATEGY=prefer_remote  # prefer_remote|remote_only|server_only|load_balance

# Security
SECRET_KEY=random_secret_key_for_jwt
```

### Ports
- `8080`: Web-Interface (HTTP)
- `6800`: aria2c RPC (internal)
- `5000`: Remote Worker API (optional, external)

### Volumes
```yaml
volumes:
  - /mnt/user/appdata/docker-media-manager/config:/config
  - /mnt/user/downloads:/downloads
  - /mnt/user/media:/media
  - /mnt/user/cache:/cache  # optional
```

## Remote Worker Setup

Separater Docker-Container oder Python-Script für Remote-PC:

### Worker-Funktionen
- Nimmt Encoding-Jobs via REST API entgegen
- Nutzt lokale Hardware-Beschleunigung (NVENC/QSV/AMF)
- Sendet Progress-Updates via WebSocket
- Uploaded fertige Datei zurück (oder nutzt Network Share)

### Worker-Deployment-Optionen

**Option 1**: Docker auf Windows/Linux
```bash
docker run -d \
  --name media-worker \
  -p 5000:5000 \
  -e API_KEY=your_api_key \
  -e HARDWARE_ACCEL=nvenc \
  --gpus all \
  -v /path/to/temp:/temp \
  docker-media-worker:latest
```

**Option 2**: Python-Script (standalone)
```bash
pip install -r worker-requirements.txt
python worker.py --api-key=xxx --hardware=nvenc
```

**Option 3**: Network Share (kein Transfer)
- Beide Workers mounten gleichen Share
- Encoding direkt auf Shared Storage
- Keine Datei-Übertragung nötig

## Sicherheit

### Passwort-Verschlüsselung
- Fernet (symmetric encryption) für gespeicherte Passwörter
- API-Keys verschlüsselt in Datenbank
- Master-Key aus Environment oder generiert

### API-Authentifizierung
- JWT-Tokens für Frontend-Backend-Kommunikation
- API-Key für Remote-Worker-Kommunikation
- Rate-Limiting gegen Brute-Force

### File-Access
- Sandboxed Paths (keine Zugriffe außerhalb Volumes)
- Input-Validation für alle File-Operationen
- Quarantäne für verdächtige Dateien

## Performance-Optimierungen

### Download
- aria2c: 16 parallele Verbindungen pro Download
- Chunk-Size: 1MB für optimale Speed
- Auto-Resume bei Verbindungsabbruch

### Encoding
- Multi-threaded FFmpeg (auto-detect CPU cores)
- Hardware-Beschleunigung wenn verfügbar
- Chunk-basierter Upload bei Remote-Worker (10MB chunks)

### Database
- SQLite WAL-Mode für bessere Concurrency
- Indizes auf häufig abgefragte Felder
- Regelmäßige VACUUM-Operations

### Caching
- TMDB-API-Responses gecacht (24h)
- Frontend-Assets mit Cache-Headers
- Redis für Session-Storage

## Monitoring & Logging

### Application Logs
- Strukturierte JSON-Logs
- Rotating File Handler (max 10MB, 5 Backups)
- Log-Levels: DEBUG, INFO, WARNING, ERROR

### Metrics (Future)
- Download-Speed & Total Downloaded
- Encoding-Time & Success-Rate
- TMDB-Hit-Rate
- Disk-Space-Usage

### Health Checks
- Docker HEALTHCHECK für Container-Status
- Worker-Availability-Pings (30s Interval)
- Database-Connection-Monitoring

## Erweiterbarkeit

### Plugin-System (Future)
- Custom Download-Provider
- Custom Metadata-Sources
- Custom Post-Processing-Scripts

### API für Externe Tools
- RESTful API dokumentiert (OpenAPI)
- Webhook-Support für Events
- CLI-Tool für Scripting

## Deployment-Strategie

### Phase 1: Local Development
- Docker Compose Setup für lokales Testing
- Hot-Reload für Backend/Frontend
- Sample-Data für UI-Development

### Phase 2: Unraid-Template
- Community Applications Template
- Pre-configured Volume-Mappings
- Default-Settings für typische Use-Cases

### Phase 3: Documentation
- Installation-Guide für Unraid
- Configuration-Examples
- Troubleshooting-Section

### Phase 4: Community
- GitHub-Repository (public)
- Issue-Tracking
- Feature-Requests via Discussions

## Risiken & Mitigations

| Risiko | Auswirkung | Mitigation |
|--------|------------|------------|
| Filehoster ändern API/Limits | Downloads schlagen fehl | Abstraction-Layer, easy Updates |
| FFmpeg-Encoding sehr langsam | Schlechte UX | Remote-Worker-Option, Hardware-Accel |
| TMDB-API-Rate-Limiting | Metadaten-Download fehlschlägt | Caching, Retry mit Backoff |
| Große Video-Dateien > 50GB | Disk-Space-Issues | Disk-Space-Checks, Warnings |
| Corrupt Downloads | Defekte Video-Dateien | Checksum-Validation, Auto-Retry |

## Success Metrics

- **Performance**: Download-to-Final-Media in < 30 Min (für 5GB Film)
- **Reliability**: 95%+ Success-Rate bei Auto-Processing
- **Usability**: Neuer User kann ersten Download in < 5 Min starten
- **Resource-Usage**: < 2GB RAM, < 10% CPU idle state

## Roadmap

### v1.0 (MVP)
- Download-Manager mit RapidGator/DDownload
- Archive-Extraktion mit Passwort-Support
- Basis-Encoding (HEVC, CRF-based)
- TMDB-Integration
- Web-UI (Dashboard, Queue, Settings)

### v1.1
- Remote-Worker-Support
- Custom Encoding-Presets
- Import/Export-Funktionen

### v1.2
- Load-Balancing zwischen Workers
- Advanced FFmpeg-Options
- Subtitle-Download

### v2.0
- Mehr Filehoster (Uploaded, Mega, etc.)
- Plugin-System
- Mobile-App (React Native)
- Notification-System (Email, Telegram, Discord)

---

**Letzte Aktualisierung**: 2025-10-22
**Version**: 1.0-draft
**Autor**: AI Assistant + User Requirements
