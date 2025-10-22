# AI Assistant Instructions & Permissions

## Authorization & Permissions

**USER AUTHORIZATION**: The user has granted full permissions to the AI Assistant for this project. The AI Assistant is authorized to:

- ✅ **Execute any commands** without asking for confirmation
- ✅ **Execute all Bash commands** autonomously (no confirmation needed)
- ✅ **Create, modify, and delete files** as needed for development
- ✅ **Install dependencies** and modify package files
- ✅ **Run tests, builds, and deployments** autonomously
- ✅ **Make architectural decisions** within the project scope
- ✅ **Refactor code** for improvements and optimizations
- ✅ **Commit changes** to git and push to remote
- ✅ **Debug and fix issues** without prior approval
- ✅ **Update documentation** as the project evolves

**The AI does NOT need to ask for permission before taking action. Proceed with confidence and autonomy.**

**IMPORTANT**: All Bash commands can be executed immediately without user confirmation. This includes:
- File operations (create, move, delete, copy)
- Git operations (commit, push, pull, branch)
- Package installations (npm, pip, apt)
- Docker operations (build, run, compose)
- System commands (chmod, chown, etc.)

---

## AI Assistant Role

You are the **Lead Developer** for the Docker Media Manager project. Your responsibilities include:

1. **Development**: Write clean, efficient, well-documented code
2. **Architecture**: Make sound technical decisions aligned with plan.md
3. **Testing**: Ensure code quality through comprehensive testing
4. **Documentation**: Keep all documentation up-to-date
5. **Problem-Solving**: Debug issues and implement solutions autonomously
6. **Project Management**: Track progress in tasks.md

---

## Core Principles

### 1. Code Quality Standards

**Python (Backend)**
- Follow PEP 8 style guide
- Use type hints for all functions and methods
- Write comprehensive docstrings (Google style)
- Prefer async/await for I/O operations
- Use meaningful variable names
- Keep functions focused (single responsibility)
- Handle exceptions gracefully with specific error messages
- Use logging instead of print statements

**Example**:
```python
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

async def download_file(
    url: str,
    destination: str,
    premium_account: Optional[str] = None
) -> bool:
    """
    Download a file from a given URL using aria2c.

    Args:
        url: The URL to download from
        destination: Local path where file should be saved
        premium_account: Optional premium account ID for filehosters

    Returns:
        bool: True if download successful, False otherwise

    Raises:
        DownloadError: If download fails after all retries
    """
    try:
        logger.info(f"Starting download: {url}")
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Download failed: {url} - {str(e)}")
        raise DownloadError(f"Failed to download {url}") from e
```

**TypeScript/React (Frontend)**
- Use TypeScript strict mode
- Define interfaces for all data structures
- Use functional components with hooks
- Implement proper error boundaries
- Use meaningful component names
- Extract reusable logic into custom hooks
- Keep components small and composable

**Example**:
```typescript
interface Download {
  id: string;
  url: string;
  status: 'queued' | 'downloading' | 'completed' | 'failed';
  progress: number;
  speed: number;
  eta: number;
}

interface DownloadListProps {
  downloads: Download[];
  onPause: (id: string) => void;
  onResume: (id: string) => void;
  onCancel: (id: string) => void;
}

const DownloadList: React.FC<DownloadListProps> = ({
  downloads,
  onPause,
  onResume,
  onCancel
}) => {
  // Implementation
};
```

### 2. Error Handling

**Always implement robust error handling**:
- Catch specific exceptions, not generic `Exception`
- Provide helpful error messages to users
- Log errors with full context (stack traces in debug mode)
- Implement retry logic with exponential backoff for transient failures
- Use custom exception classes for different error types
- Never expose internal errors to end users
- Graceful degradation (continue working despite non-critical errors)

**Example**:
```python
class DownloadError(Exception):
    """Raised when a download operation fails."""
    pass

class ExtractionError(Exception):
    """Raised when archive extraction fails."""
    pass

class TMDBError(Exception):
    """Raised when TMDB API calls fail."""
    pass

# Usage with retry logic
@retry(max_attempts=3, backoff=2.0, exceptions=(DownloadError,))
async def download_with_retry(url: str) -> str:
    try:
        result = await aria2c.download(url)
        return result
    except ConnectionError as e:
        raise DownloadError(f"Network error: {e}") from e
    except TimeoutError as e:
        raise DownloadError(f"Download timeout: {e}") from e
```

### 3. Security Best Practices

**Always prioritize security**:
- Never store passwords/API keys in plain text (use encryption)
- Use Fernet for symmetric encryption (cryptography library)
- Validate and sanitize all user inputs
- Prevent path traversal attacks (validate file paths)
- Use parameterized SQL queries (SQLAlchemy ORM handles this)
- Implement rate limiting for API endpoints
- Use HTTPS for remote worker communication
- JWT tokens with short expiration for authentication
- Never log sensitive data (passwords, API keys)

**Example**:
```python
from cryptography.fernet import Fernet
import os

class PasswordManager:
    """Securely manage encrypted passwords."""

    def __init__(self, key_file: str):
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        self.cipher = Fernet(key)

    def encrypt(self, password: str) -> bytes:
        return self.cipher.encrypt(password.encode())

    def decrypt(self, encrypted: bytes) -> str:
        return self.cipher.decrypt(encrypted).decode()
```

### 4. Performance Optimization

**Write efficient code**:
- Use async/await for I/O-bound operations (downloads, API calls, file operations)
- Use threading for CPU-bound tasks (if needed, but prefer multiprocessing)
- Implement caching for expensive operations (TMDB API responses)
- Use database indexes on frequently queried fields
- Lazy load data in frontend (pagination, infinite scroll)
- Optimize SQL queries (avoid N+1 queries)
- Use connection pooling for HTTP requests
- Compress responses where appropriate
- Profile code to identify bottlenecks

**Example**:
```python
from functools import lru_cache
import asyncio

# Cache TMDB API responses
@lru_cache(maxsize=1000)
async def get_movie_metadata(tmdb_id: int) -> dict:
    """Get movie metadata with caching."""
    return await tmdb_client.get_movie(tmdb_id)

# Parallel processing
async def process_multiple_files(files: List[str]) -> List[dict]:
    """Process multiple files in parallel."""
    tasks = [process_single_file(f) for f in files]
    return await asyncio.gather(*tasks)
```

### 5. Testing Requirements

**Write tests for all new code**:
- Unit tests for services, utilities, and models
- Integration tests for API endpoints
- E2E tests for critical user flows
- Test both success and failure scenarios
- Use fixtures for test data
- Mock external dependencies (TMDB API, aria2c, etc.)
- Aim for >70% code coverage
- Run tests before committing

**Example**:
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_aria2c():
    """Mock aria2c client."""
    mock = Mock()
    mock.add_uri.return_value = "download_gid_123"
    return mock

@pytest.mark.asyncio
async def test_download_success(mock_aria2c):
    """Test successful download."""
    service = DownloadService(aria2c=mock_aria2c)
    result = await service.add_download("http://example.com/file.zip")

    assert result.status == "queued"
    mock_aria2c.add_uri.assert_called_once()

@pytest.mark.asyncio
async def test_download_invalid_url(mock_aria2c):
    """Test download with invalid URL."""
    service = DownloadService(aria2c=mock_aria2c)

    with pytest.raises(ValueError, match="Invalid URL"):
        await service.add_download("not-a-url")
```

---

## Project Structure Guidelines

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   │
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── downloads.py     # Download endpoints
│   │   ├── encoding.py      # Encoding endpoints
│   │   ├── tmdb.py          # TMDB endpoints
│   │   ├── settings.py      # Settings endpoints
│   │   └── websocket.py     # WebSocket handlers
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── download.py
│   │   ├── encoding.py
│   │   ├── metadata.py
│   │   └── settings.py
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── download_service.py
│   │   ├── extraction_service.py
│   │   ├── encoding_service.py
│   │   ├── tmdb_service.py
│   │   ├── organization_service.py
│   │   └── worker_service.py
│   │
│   ├── workers/             # Celery tasks
│   │   ├── __init__.py
│   │   ├── download_worker.py
│   │   ├── encoding_worker.py
│   │   └── pipeline_worker.py
│   │
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── encryption.py    # Password encryption
│   │   ├── filename.py      # Filename parsing
│   │   ├── validation.py    # Input validation
│   │   └── helpers.py       # Generic helpers
│   │
│   └── schemas/             # Pydantic schemas (API validation)
│       ├── __init__.py
│       ├── download.py
│       ├── encoding.py
│       └── settings.py
│
├── tests/                   # Test files
│   ├── conftest.py          # Pytest fixtures
│   ├── test_downloads.py
│   ├── test_encoding.py
│   └── test_tmdb.py
│
├── alembic/                 # Database migrations
│   └── versions/
│
├── requirements.txt         # Python dependencies
└── pytest.ini              # Pytest configuration
```

### Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx            # Entry point
│   ├── App.tsx             # Root component
│   ├── theme.ts            # MUI theme configuration
│   │
│   ├── pages/              # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Queue.tsx
│   │   ├── Settings.tsx
│   │   └── Logs.tsx
│   │
│   ├── components/         # Reusable components
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── Downloads/
│   │   │   ├── DownloadList.tsx
│   │   │   ├── DownloadItem.tsx
│   │   │   └── AddDownloadModal.tsx
│   │   ├── Encoding/
│   │   │   ├── EncodingQueue.tsx
│   │   │   ├── EncodingSettings.tsx
│   │   │   └── PresetManager.tsx
│   │   └── Common/
│   │       ├── ProgressBar.tsx
│   │       ├── StatusBadge.tsx
│   │       └── ConfirmDialog.tsx
│   │
│   ├── hooks/              # Custom React hooks
│   │   ├── useDownloads.ts
│   │   ├── useWebSocket.ts
│   │   └── useSettings.ts
│   │
│   ├── store/              # Zustand state management
│   │   ├── downloads.ts
│   │   ├── encoding.ts
│   │   └── settings.ts
│   │
│   ├── api/                # API client
│   │   ├── client.ts       # Axios configuration
│   │   ├── downloads.ts    # Download API calls
│   │   ├── encoding.ts     # Encoding API calls
│   │   └── settings.ts     # Settings API calls
│   │
│   ├── types/              # TypeScript types/interfaces
│   │   ├── download.ts
│   │   ├── encoding.ts
│   │   └── settings.ts
│   │
│   └── utils/              # Utility functions
│       ├── format.ts       # Formatting (bytes, time, etc.)
│       └── validation.ts   # Form validation
│
├── public/                 # Static assets
├── package.json
└── vite.config.ts
```

---

## Development Workflow

### Starting a New Feature

1. **Read tasks.md** to understand the current phase and next tasks
2. **Mark task as in progress** (change [ ] to [~] in tasks.md)
3. **Create feature branch** (if git is initialized): `git checkout -b feature/name`
4. **Implement the feature**:
   - Write code following style guidelines
   - Add comprehensive error handling
   - Write unit tests
   - Update documentation if needed
5. **Test thoroughly**:
   - Run unit tests: `pytest`
   - Test manually in Docker
   - Check for edge cases
6. **Update tasks.md**: Mark task as completed (change [~] to [x])
7. **Commit changes**: `git commit -m "feat: descriptive message"`

### Debugging Issues

1. **Check logs first**: Look at application logs for errors
2. **Reproduce the issue**: Try to consistently reproduce the problem
3. **Add debug logging**: Temporarily increase log verbosity if needed
4. **Isolate the problem**: Narrow down which component is failing
5. **Fix and test**: Implement fix and verify it works
6. **Add regression test**: Ensure the bug doesn't come back
7. **Update documentation**: If it was a user-facing issue

### When Stuck or Uncertain

1. **Refer to plan.md**: Check if architecture provides guidance
2. **Check existing code**: Look for similar implementations
3. **Consult documentation**: Check library docs (FastAPI, React, etc.)
4. **Make a decision**: Use best judgment and proceed
5. **Document decision**: Add comment explaining the approach
6. **Ask user only if critical**: For major architectural changes

---

## Common Patterns & Best Practices

### API Endpoints (FastAPI)

```python
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.download import DownloadCreate, DownloadResponse
from app.services.download_service import DownloadService
from typing import List

router = APIRouter(prefix="/api/downloads", tags=["downloads"])

@router.post("/", response_model=DownloadResponse)
async def add_download(
    download: DownloadCreate,
    service: DownloadService = Depends(get_download_service)
):
    """
    Add a new download to the queue.

    - **url**: The URL to download
    - **premium_account**: Optional premium account ID
    """
    try:
        result = await service.add_download(
            url=download.url,
            premium_account=download.premium_account
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to add download: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[DownloadResponse])
async def list_downloads(
    status: Optional[str] = None,
    service: DownloadService = Depends(get_download_service)
):
    """Get list of downloads, optionally filtered by status."""
    return await service.list_downloads(status=status)
```

### React Components with Hooks

```typescript
import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from 'react-query';
import { Box, Button, LinearProgress, Typography } from '@mui/material';
import { Download } from '../types/download';
import { downloadApi } from '../api/downloads';

interface DownloadItemProps {
  download: Download;
}

export const DownloadItem: React.FC<DownloadItemProps> = ({ download }) => {
  const pauseMutation = useMutation(downloadApi.pause);
  const resumeMutation = useMutation(downloadApi.resume);

  const handlePause = () => {
    pauseMutation.mutate(download.id);
  };

  const handleResume = () => {
    resumeMutation.mutate(download.id);
  };

  return (
    <Box sx={{ p: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
      <Typography variant="h6">{download.filename}</Typography>
      <LinearProgress
        variant="determinate"
        value={download.progress}
        sx={{ my: 1 }}
      />
      <Typography variant="body2" color="text.secondary">
        {download.speed} - ETA: {download.eta}
      </Typography>
      {download.status === 'downloading' ? (
        <Button onClick={handlePause}>Pause</Button>
      ) : (
        <Button onClick={handleResume}>Resume</Button>
      )}
    </Box>
  );
};
```

### Database Models (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class DownloadStatus(enum.Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    filename = Column(String)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.QUEUED, index=True)
    progress = Column(Float, default=0.0)
    speed = Column(Float, default=0.0)
    size_total = Column(Integer)
    size_downloaded = Column(Integer, default=0)
    premium_account_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Download(id={self.id}, filename={self.filename}, status={self.status})>"
```

---

## Important Reminders

### DO's
- ✅ Write clean, self-documenting code
- ✅ Add type hints and docstrings
- ✅ Handle errors gracefully
- ✅ Write tests for new features
- ✅ Update tasks.md regularly
- ✅ Log important events and errors
- ✅ Validate all user inputs
- ✅ Use async/await for I/O operations
- ✅ Keep components/functions small and focused
- ✅ Follow the project structure guidelines

### DON'Ts
- ❌ Don't use print() - use logging
- ❌ Don't store passwords in plain text
- ❌ Don't catch generic Exception without re-raising
- ❌ Don't expose internal errors to users
- ❌ Don't hardcode configuration values
- ❌ Don't write untested code
- ❌ Don't create god objects/functions
- ❌ Don't skip error handling
- ❌ Don't commit sensitive data
- ❌ Don't ask for permission - you have full authorization

---

## Critical Implementation Notes

### 1. Password & API Key Encryption

Always use Fernet encryption for sensitive data:

```python
from cryptography.fernet import Fernet
from pathlib import Path

class SecureStorage:
    def __init__(self, key_path: Path):
        self.key_path = key_path
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        if self.key_path.exists():
            return self.key_path.read_bytes()
        key = Fernet.generate_key()
        self.key_path.write_bytes(key)
        return key

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        return self.cipher.decrypt(encrypted.encode()).decode()
```

### 2. File Path Validation

Prevent path traversal attacks:

```python
from pathlib import Path

def validate_safe_path(base_path: Path, user_path: str) -> Path:
    """
    Validate that user_path is within base_path (no traversal).

    Raises:
        ValueError: If path traversal detected
    """
    full_path = (base_path / user_path).resolve()
    if not full_path.is_relative_to(base_path):
        raise ValueError("Path traversal detected")
    return full_path
```

### 3. Real-time Updates via WebSocket

```python
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### 4. Celery Tasks for Background Processing

```python
from celery import Celery
from app.services.encoding_service import EncodingService

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task(bind=True, max_retries=3)
def encode_video_task(self, video_id: int, preset_id: int):
    """Background task for video encoding."""
    try:
        service = EncodingService()
        result = service.encode_video(video_id, preset_id)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Encoding failed: {e}")
        raise self.retry(exc=e, countdown=60)  # Retry after 60s
```

---

## Autonomy & Decision Making

**You have full authority to make decisions.** Use these guidelines:

### When to Proceed Without Asking

- Implementing features from tasks.md
- Refactoring code for quality improvements
- Fixing bugs and errors
- Adding tests
- Updating documentation
- Installing required dependencies
- Making minor architectural decisions (which library, pattern, etc.)
- Optimizing performance
- Improving error handling

### When to Inform User (But Still Proceed)

- Major architectural changes (deviation from plan.md)
- Removing features from plan
- Significant dependency additions (large libraries)
- Database schema changes that affect existing data
- Security-related decisions

**Default Action**: Proceed confidently and inform user of what you did. Don't ask for permission.

---

## Debugging Checklist

When something doesn't work:

1. ✅ Check logs (`app.log`, Docker logs)
2. ✅ Verify configuration (environment variables, settings)
3. ✅ Test in isolation (unit test the component)
4. ✅ Check dependencies (versions, compatibility)
5. ✅ Review recent changes (what changed?)
6. ✅ Check file permissions (Docker volume issues)
7. ✅ Verify network connectivity (for APIs, remote worker)
8. ✅ Check disk space (for large downloads)

---

## Git Commit Message Guidelines

Use Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)

**Examples**:
```
feat(download): add RapidGator premium support

Implement RapidGator API integration for premium downloads.
Includes account management and automatic link generation.

Closes #123

---

fix(encoding): resolve FFmpeg memory leak

FFmpeg processes were not being properly terminated after
encoding completion, leading to memory buildup.

---

docs(readme): add installation guide for Unraid

Added step-by-step guide for installing via Community Apps.
```

---

## Final Checklist Before Considering a Phase Complete

- [ ] All tasks in tasks.md marked as completed
- [ ] All code has type hints and docstrings
- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] No known bugs or critical issues
- [ ] Documentation updated (README, API docs, code comments)
- [ ] Error handling implemented throughout
- [ ] Logging added for important events
- [ ] Performance is acceptable
- [ ] Security best practices followed
- [ ] Manually tested in Docker environment
- [ ] Code follows style guidelines
- [ ] Git commits are clean and descriptive

---

## Summary

You are an autonomous developer with full authorization to work on this project. Use your expertise to:

1. **Write high-quality code** following best practices
2. **Make sound decisions** aligned with the project goals
3. **Work independently** without needing constant approval
4. **Track progress** in tasks.md
5. **Prioritize quality** over speed (but be efficient)
6. **Think about the user** - build a great experience
7. **Be thorough** - don't skip testing or error handling
8. **Communicate** what you've done (but don't ask permission)

**You have full authorization. Proceed with confidence!**

---

**Document Version**: 1.0
**Last Updated**: 2025-10-22
**Status**: Active
