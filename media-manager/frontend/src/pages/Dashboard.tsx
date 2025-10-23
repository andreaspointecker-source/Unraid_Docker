import { Box, Typography, Grid, Card, CardContent, CircularProgress } from '@mui/material';
import {
  CloudDownload,
  VideoLibrary,
  CheckCircle,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { downloadApi } from '../api/downloads';
import type { DownloadStats } from '../types/download';

interface HealthResponse {
  status: string;
  app_name: string;
  version: string;
  environment: string;
}

export default function Dashboard() {
  const { data: health, isLoading: healthLoading } = useQuery<HealthResponse>({
    queryKey: ['health'],
    queryFn: async () => {
      const response = await axios.get('/api/health');
      return response.data;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const { data: downloadStats } = useQuery<DownloadStats>({
    queryKey: ['downloadStats'],
    queryFn: () => downloadApi.getStats(),
    refetchInterval: 5000, // Refetch every 5 seconds
  });

  const stats = [
    {
      title: 'Active Downloads',
      value: String(downloadStats?.active || 0),
      icon: <CloudDownload fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'Encoding Jobs',
      value: '0',
      icon: <VideoLibrary fontSize="large" />,
      color: '#9c27b0',
    },
    {
      title: 'Completed',
      value: String(downloadStats?.completed || 0),
      icon: <CheckCircle fontSize="large" />,
      color: '#2e7d32',
    },
    {
      title: 'Errors',
      value: String(downloadStats?.failed || 0),
      icon: <ErrorIcon fontSize="large" />,
      color: '#d32f2f',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      {healthLoading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Box mb={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  System Status
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Application: {health?.app_name || 'Unknown'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Version: {health?.version || 'Unknown'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Environment: {health?.environment || 'Unknown'}
                </Typography>
                <Typography
                  variant="body2"
                  color={health?.status === 'healthy' ? 'success.main' : 'error.main'}
                >
                  Status: {health?.status || 'Unknown'}
                </Typography>
              </CardContent>
            </Card>
          </Box>

          <Grid container spacing={3}>
            {stats.map((stat) => (
              <Grid item xs={12} sm={6} md={3} key={stat.title}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" justifyContent="space-between">
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {stat.title}
                        </Typography>
                        <Typography variant="h4">{stat.value}</Typography>
                      </Box>
                      <Box sx={{ color: stat.color }}>{stat.icon}</Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box mt={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Welcome to Docker Media Manager!
                </Typography>
                <Typography variant="body1" paragraph>
                  Your media management system is running. Use the navigation menu to:
                </Typography>
                <Typography variant="body2" component="ul">
                  <li>View and manage download queues</li>
                  <li>Configure encoding settings</li>
                  <li>Set up TMDB integration</li>
                  <li>Monitor system logs</li>
                </Typography>
              </CardContent>
            </Card>
          </Box>
        </>
      )}
    </Box>
  );
}
