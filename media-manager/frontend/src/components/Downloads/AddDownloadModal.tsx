import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { downloadApi } from '../../api/downloads';

interface AddDownloadModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AddDownloadModal({
  open,
  onClose,
  onSuccess,
}: AddDownloadModalProps) {
  const [urls, setUrls] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!urls.trim()) {
      setError('Please enter at least one URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const urlList = urls
        .split('\n')
        .map((url) => url.trim())
        .filter((url) => url.length > 0);

      if (urlList.length === 0) {
        setError('No valid URLs found');
        return;
      }

      if (urlList.length === 1) {
        // Single download
        await downloadApi.add({ url: urlList[0] });
      } else {
        // Bulk download
        await downloadApi.addBulk({ urls: urlList });
      }

      // Success
      setUrls('');
      onSuccess();
      onClose();
    } catch (err: any) {
      console.error('Failed to add download:', err);
      setError(
        err.response?.data?.detail || err.message || 'Failed to add download'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      setUrls('');
      setError(null);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Add Downloads</DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <TextField
            autoFocus
            multiline
            rows={8}
            fullWidth
            label="URLs"
            placeholder="Enter URLs (one per line)"
            value={urls}
            onChange={(e) => setUrls(e.target.value)}
            disabled={loading}
            helperText="Add one or multiple URLs, each on a separate line"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !urls.trim()}
          startIcon={loading ? <CircularProgress size={20} /> : <AddIcon />}
        >
          {loading ? 'Adding...' : 'Add'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
