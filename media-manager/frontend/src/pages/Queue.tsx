import {
  Box,
  Typography,
  Card,
  CardContent,
  Tabs,
  Tab,
  Button,
  Paper,
} from '@mui/material';
import { useState } from 'react';
import { Add as AddIcon } from '@mui/icons-material';
import AddDownloadModal from '../components/Downloads/AddDownloadModal';
import DownloadList from '../components/Downloads/DownloadList';
import type { DownloadStatus } from '../types/download';

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
  const [downloadTab, setDownloadTab] = useState(0);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const downloadStatusMap: (DownloadStatus | undefined)[] = [
    undefined, // All
    'downloading',
    'paused',
    'completed',
    'failed',
  ];

  const handleAddSuccess = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <Box>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Typography variant="h4">Queue Management</Typography>
        {tabValue === 0 && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setAddModalOpen(true)}
          >
            Add Download
          </Button>
        )}
      </Box>

      <Card>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="queue tabs">
          <Tab label="Downloads" />
          <Tab label="Extraction" />
          <Tab label="Encoding" />
          <Tab label="TMDB Matching" />
          <Tab label="Organization" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Paper sx={{ mb: 2 }}>
            <Tabs
              value={downloadTab}
              onChange={(_, newValue) => setDownloadTab(newValue)}
              variant="fullWidth"
            >
              <Tab label="All" />
              <Tab label="Downloading" />
              <Tab label="Paused" />
              <Tab label="Completed" />
              <Tab label="Failed" />
            </Tabs>
          </Paper>
          <DownloadList
            status={downloadStatusMap[downloadTab]}
            refreshTrigger={refreshTrigger}
          />
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

      <AddDownloadModal
        open={addModalOpen}
        onClose={() => setAddModalOpen(false)}
        onSuccess={handleAddSuccess}
      />
    </Box>
  );
}
