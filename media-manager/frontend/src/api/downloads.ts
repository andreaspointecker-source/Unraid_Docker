import axios from 'axios';
import type {
  Download,
  DownloadStats,
  CreateDownloadRequest,
  BulkDownloadRequest,
  DownloadActionResponse,
} from '../types/download';

const API_BASE = '/api/downloads/';

export const downloadApi = {
  // Get all downloads
  getAll: async (status?: string): Promise<Download[]> => {
    const params = status ? { status } : {};
    const response = await axios.get<Download[]>(API_BASE, { params });
    return response.data;
  },

  // Get download by ID
  getById: async (id: number): Promise<Download> => {
    const response = await axios.get<Download>(`${API_BASE}/${id}`);
    return response.data;
  },

  // Get download statistics
  getStats: async (): Promise<DownloadStats> => {
    const response = await axios.get<DownloadStats>(`${API_BASE}/stats`);
    return response.data;
  },

  // Add single download
  add: async (data: CreateDownloadRequest): Promise<Download> => {
    const response = await axios.post<Download>(API_BASE, data);
    return response.data;
  },

  // Add multiple downloads
  addBulk: async (data: BulkDownloadRequest): Promise<Download[]> => {
    const response = await axios.post<Download[]>(`${API_BASE}/bulk`, data);
    return response.data;
  },

  // Pause download
  pause: async (id: number): Promise<DownloadActionResponse> => {
    const response = await axios.post<DownloadActionResponse>(
      `${API_BASE}/${id}/pause`
    );
    return response.data;
  },

  // Resume download
  resume: async (id: number): Promise<DownloadActionResponse> => {
    const response = await axios.post<DownloadActionResponse>(
      `${API_BASE}/${id}/resume`
    );
    return response.data;
  },

  // Cancel download
  cancel: async (id: number): Promise<DownloadActionResponse> => {
    const response = await axios.post<DownloadActionResponse>(
      `${API_BASE}/${id}/cancel`
    );
    return response.data;
  },

  // Retry download
  retry: async (id: number): Promise<DownloadActionResponse> => {
    const response = await axios.post<DownloadActionResponse>(
      `${API_BASE}/${id}/retry`
    );
    return response.data;
  },

  // Delete download
  delete: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE}/${id}`);
  },
};
