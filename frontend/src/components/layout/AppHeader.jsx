import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Button
} from '@mui/material';

import MedicalServicesIcon from '@mui/icons-material/MedicalServices';


function AppHeader({ username, role, onLogout }) {
    return (
        <AppBar
            position="static"
            sx={{
                backgroundColor: '#1f2937',
                color: 'white',
            }}
        >
            <Toolbar sx={{ px: 3 }}>

                <MedicalServicesIcon sx={{ mr: 2 }} />

                <Typography
                    variant="h6"
                    component="h1"
                    sx={{
                        flexGrow: 1,
                        fontWeight: 600,
                    }}
                >
                    MedFlow Clinical Equipment Command Center
                </Typography>

                {username && (
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 2,
                        }}
                    >
                        <Typography variant="body2">
                            {username} ({role})
                        </Typography>

                        <Button
                            color="inherit"
                            onClick={onLogout}
                            sx={{
                                border: '1px solid rgba(255,255,255,0.5)',
                            }}
                        >
                            Log Out
                        </Button>
                    </Box>
                )}

            </Toolbar>
        </AppBar>
    );
}


export default AppHeader;