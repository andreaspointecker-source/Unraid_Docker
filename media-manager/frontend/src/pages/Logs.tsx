import { Box, Typography, Card, CardContent } from '@mui/material';

export default function Logs() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Logs
      </Typography>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Log Viewer
          </Typography>
          <Typography variant="body1">
            Log viewer will be implemented in a future phase.
            This will provide real-time access to:
          </Typography>
          <Typography variant="body2" component="ul" sx={{ mt: 2 }}>
            <li>Application logs</li>
            <li>Download logs</li>
            <li>Encoding logs</li>
            <li>TMDB API logs</li>
            <li>Error logs</li>
          </Typography>
          <Typography variant="body2" sx={{ mt: 2 }}>
            Features: filtering, search, export, and real-time updates.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
