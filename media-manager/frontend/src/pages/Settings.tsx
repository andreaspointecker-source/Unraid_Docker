import { Box, Typography, Card, CardContent } from '@mui/material';

export default function Settings() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Configuration
          </Typography>
          <Typography variant="body1">
            Settings interface will be implemented in the next phase.
            This will include configuration for:
          </Typography>
          <Typography variant="body2" component="ul" sx={{ mt: 2 }}>
            <li>Download settings (aria2c configuration, premium accounts)</li>
            <li>Extraction settings (passwords, archive handling)</li>
            <li>Encoding settings (presets, workers, quality)</li>
            <li>TMDB integration (API key, language preferences)</li>
            <li>File organization (naming schemes, paths)</li>
            <li>System settings (logging, cleanup intervals)</li>
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
