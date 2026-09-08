import {
  Container,
  Typography,
  Box,
  Snackbar,
  Alert,
} from '@mui/material';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';
import { useState } from 'react';

import AppHeader from './components/layout/AppHeader.jsx';
import LoginForm from './components/auth/LoginForm.jsx';
import ReliabilityMetrics from './components/analytics/ReliabilityMetrics.jsx';
import MaintenanceFlags from './components/analytics/MaintenanceFlags.jsx';
import ReportingLines from './components/analytics/ReportingLines.jsx';


import EquipmentDataGrid from './components/equipment/EquipmentDataGrid.jsx';
import DiscrepancyDataGrid from './components/workOrders/DiscrepancyDataGrid.jsx';


function App() {
  return (
      <AuthProvider>
          <AppContent />
      </AuthProvider>
  );
}

//? means read if exists
// token is the encoded JWT string; user is the decoded token payload with fields like sub and role.
function Dashboard() {
  const { user, logout } = useAuth()
  const [notification, setNotification] = useState(null);

  return (
    <>
      <AppHeader
        username={user?.sub}
        role={user?.role}
        onLogout={logout}
      />

      <Box
        sx={{
          minHeight: '100vh',
          backgroundColor: '#f5f7fa',
          py: 4,
        }}
      >
        <Container maxWidth="lg">

          {/* Equipment */}
          <Box
            sx={{
              backgroundColor: 'white',
              p: 3,
              mb: 3,
              borderRadius: 2,
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography
              variant="h5"
              component="h2"
              sx={{
                mb: 2,
                color: '#1f2937',
                fontWeight: 600,
              }}
            >
              Equipment Overview
            </Typography>

            <EquipmentDataGrid onSuccess={setNotification} />
          </Box>


          {/* Co-Location */}
          <Box
            sx={{
              backgroundColor: 'white',
              p: 3,
              mb: 3,
              borderRadius: 2,
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography
              variant="h5"
              component="h2"
              sx={{
                mb: 2,
                color: '#1f2937',
                fontWeight: 600,
              }}
            >
              Co-Location Discrepancies
            </Typography>

            <DiscrepancyDataGrid />
          </Box>


          {/* Reliability */}
          <Box
            sx={{
              backgroundColor: 'white',
              p: 3,
              mb: 3,
              borderRadius: 2,
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography
              variant="h5"
              component="h2"
              sx={{
                mb: 2,
                color: '#1f2937',
                fontWeight: 600,
              }}
            >
              Reliability Metrics
            </Typography>

            <ReliabilityMetrics />
          </Box>


          {/* Maintenance */}
          <Box
            sx={{
              backgroundColor: 'white',
              p: 3,
              mb: 3,
              borderRadius: 2,
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography
              variant="h5"
              component="h2"
              sx={{
                mb: 2,
                color: '#1f2937',
                fontWeight: 600,
              }}
            >
              Maintenance Flags
            </Typography>

            <MaintenanceFlags />
          </Box>


          {/* Reporting Lines */}
          <Box
            sx={{
              backgroundColor: 'white',
              p: 3,
              mb: 3,
              borderRadius: 2,
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography
              variant="h5"
              component="h2"
              sx={{
                mb: 2,
                color: '#1f2937',
                fontWeight: 600,
              }}
            >
              Reporting Lines
            </Typography>

            <ReportingLines />
          </Box>

        </Container>
      </Box>


      <Snackbar
        open={Boolean(notification)}
        autoHideDuration={4000}
        onClose={() => setNotification(null)}
      >
        <Alert
          severity="success"
          onClose={() => setNotification(null)}
        >
          {notification}
        </Alert>
      </Snackbar>
    </>
  )
}

// Show the dashboard if logged in; otherwise show the login form.
function AppContent() {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? <Dashboard /> : <LoginForm />;
}




export default App;

