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
  const {user, logout} = useAuth()
  const [notification, setNotification] = useState(null);
  return(
    <>
      <AppHeader 
        username={user?.sub}
        role={user?.role}
        onLogout={logout} />

              <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom>
              Equipment Overview
          </Typography>

          <Box sx={{ mb: 4 }}>
              <EquipmentDataGrid onSuccess={setNotification}/>
          </Box>

                <Typography variant="h5" component="h2" gutterBottom>
              Co-Location Discrepancies
          </Typography>

          <Box sx={{ mb: 4 }}>
              <DiscrepancyDataGrid />
          </Box>
      </Container>
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

