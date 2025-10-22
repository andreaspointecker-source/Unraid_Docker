import { Box, Typography, Card, CardContent, Tabs, Tab } from '@mui/material';
import { useState } from 'react';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`queue-tabpanel-${index}`}
      aria-labelledby={`queue-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function Queue() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Queue Management
      </Typography>

      <Card>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="queue tabs">
          <Tab label="Downloads" />
          <Tab label="Extraction" />
          <Tab label="Encoding" />
          <Tab label="TMDB Matching" />
          <Tab label="Organization" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <CardContent>
            <Typography variant="body1">
              No active downloads. Downloads will appear here when added.
            </Typography>
          </CardContent>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <CardContent>
            <Typography variant="body1">
              No files being extracted. Extraction tasks will appear here.
            </Typography>
          </CardContent>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <CardContent>
            <Typography variant="body1">
              No encoding jobs. Encoding tasks will appear here.
            </Typography>
          </CardContent>
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <CardContent>
            <Typography variant="body1">
              No metadata matching in progress. TMDB tasks will appear here.
            </Typography>
          </CardContent>
        </TabPanel>

        <TabPanel value={tabValue} index={4}>
          <CardContent>
            <Typography variant="body1">
              No files being organized. Organization tasks will appear here.
            </Typography>
          </CardContent>
        </TabPanel>
      </Card>
    </Box>
  );
}
