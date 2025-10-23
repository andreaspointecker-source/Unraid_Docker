export interface Download {
  id: number;
  url: string;
  filename: string | null;
  status: DownloadStatus;
  progress: number;
  speed: number;
  size_total: number | null;
  size_downloaded: number;
  eta: number | null;
  aria2_gid: string | null;
  premium_account_id: number | null;
  file_path: string | null;
  error_message: string | null;
  retry_count: number;
  created_at: string;
  updated_at: string | null;
}

export type DownloadStatus =
  | 'pending'
  | 'queued'
  | 'downloading'
  | 'completed'
  | 'failed'
  | 'paused'
  | 'cancelled';

export interface DownloadStats {
  total_downloads: number;
  completed_downloads: number;
  failed_downloads: number;
  active_downloads: number;
  current_speed: number;
  num_active: number;
  num_waiting: number;
}

export interface CreateDownloadRequest {
  url: string;
  premium_account_id?: number;
}

export interface BulkDownloadRequest {
  urls: string[];
  premium_account_id?: number;
}

export interface DownloadActionResponse {
  success: boolean;
  message: string;
  download?: Download;
}
