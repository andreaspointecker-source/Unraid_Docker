import { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  IconButton,
  Chip,
  Stack,
  Tooltip,
  Alert,
} from '@mui/material';
import {
  Pause as PauseIcon,
  PlayArrow as PlayIcon,
  Cancel as CancelIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
  GetApp as DownloadIcon,
} from '@mui/icons-material';
import { downloadApi } from '../../api/downloads';
import type { Download, DownloadStatus } from '../../types/download';

interface DownloadListProps {
  status?: DownloadStatus;
  refreshTrigger?: number;
}

export default function DownloadList({
  status,
  refreshTrigger = 0,
}: DownloadListProps) {
  const [downloads, setDownloads] = useState<Download[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDownloads = async () => {
    try {
      setError(null);
      const data = await downloadApi.getAll(status);
      setDownloads(data);
    } catch (err: any) {
      console.error('Failed to fetch downloads:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load downloads');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDownloads();
    // Auto-refresh every 2 seconds for active downloads
    const interval = setInterval(fetchDownloads, 2000);
    return () => clearInterval(interval);
  }, [status, refreshTrigger]);

  const handlePause = async (id: number) => {
    try {
      await downloadApi.pause(id);
      fetchDownloads();
    } catch (err: any) {
      console.error('Failed to pause download:', err);
    }
  };

  const handleResume = async (id: number) => {
    try {
      await downloadApi.resume(id);
      fetchDownloads();
    } catch (err: any) {
      console.error('Failed to resume download:', err);
    }
  };

  const handleCancel = async (id: number) => {
    try {
      await downloadApi.cancel(id);
      fetchDownloads();
    } catch (err: any) {
      console.error('Failed to cancel download:', err);
    }
  };

  const handleRetry = async (id: number) => {
    try {
      await downloadApi.retry(id);
      fetchDownloads();
    } catch (err: any) {
      console.error('Failed to retry download:', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await downloadApi.delete(id);
      fetchDownloads();
    } catch (err: any) {
      console.error('Failed to delete download:', err);
    }
  };

  const getStatusColor = (status: DownloadStatus) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'downloading':
        return 'primary';
      case 'failed':
        return 'error';
      case 'paused':
        return 'warning';
      case 'cancelled':
        return 'default';
      default:
        return 'info';
    }
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
  };

  const formatSpeed = (bytesPerSec: number): string => {
    return `${formatBytes(bytesPerSec)}/s`;
  };

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  if (loading) {
    return (
      <Box sx={{ mt: 2 }}>
        <LinearProgress />
      </Box>
    );
  }

  if (downloads.length === 0) {
    return (
      <Box sx={{ mt: 2, textAlign: 'center', py: 4 }}>
        <DownloadIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
        <Typography variant="h6" color="text.secondary">
          No downloads found
        </Typography>
      </Box>
    );
  }

  return (
    <Stack spacing={2} sx={{ mt: 2 }}>
      {downloads.map((download) => (
        <Card key={download.id}>
          <CardContent>
            <Box sx={{ mb: 2 }}>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  mb: 1,
                }}
              >
                <Box sx={{ flex: 1, mr: 2 }}>
                  <Typography variant="subtitle1" noWrap>
                    {download.filename || download.url}
                  </Typography>
                  {download.filename && (
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      noWrap
                      sx={{ display: 'block' }}
                    >
                      {download.url}
                    </Typography>
                  )}
                </Box>
                <Chip
                  label={download.status}
                  color={getStatusColor(download.status)}
                  size="small"
                />
              </Box>

              {download.status === 'downloading' && (
                <>
                  <LinearProgress
                    variant="determinate"
                    value={download.progress}
                    sx={{ mb: 1, height: 8, borderRadius: 1 }}
                  />
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      mb: 1,
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      {download.progress.toFixed(1)}% - {formatBytes(download.downloaded_bytes)} / {formatBytes(download.total_bytes)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {formatSpeed(download.speed)}
                    </Typography>
                  </Box>
                </>
              )}

              {download.status === 'completed' && (
                <Typography variant="body2" color="text.secondary">
                  Downloaded: {formatBytes(download.total_bytes)}
                </Typography>
              )}

              {download.error_message && (
                <Alert severity="error" sx={{ mt: 1 }}>
                  {download.error_message}
                </Alert>
              )}
            </Box>

            <Box sx={{ display: 'flex', gap: 1 }}>
              {download.status === 'downloading' && (
                <Tooltip title="Pause">
                  <IconButton
                    size="small"
                    onClick={() => handlePause(download.id)}
                  >
                    <PauseIcon />
                  </IconButton>
                </Tooltip>
              )}

              {download.status === 'paused' && (
                <Tooltip title="Resume">
                  <IconButton
                    size="small"
                    onClick={() => handleResume(download.id)}
                  >
                    <PlayIcon />
                  </IconButton>
                </Tooltip>
              )}

              {(download.status === 'downloading' ||
                download.status === 'paused') && (
                <Tooltip title="Cancel">
                  <IconButton
                    size="small"
                    onClick={() => handleCancel(download.id)}
                  >
                    <CancelIcon />
                  </IconButton>
                </Tooltip>
              )}

              {download.status === 'failed' && (
                <Tooltip title="Retry">
                  <IconButton
                    size="small"
                    onClick={() => handleRetry(download.id)}
                  >
                    <RefreshIcon />
                  </IconButton>
                </Tooltip>
              )}

              {(download.status === 'completed' ||
                download.status === 'failed' ||
                download.status === 'cancelled') && (
                <Tooltip title="Delete">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => handleDelete(download.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              )}
            </Box>
          </CardContent>
        </Card>
      ))}
    </Stack>
  );
}
