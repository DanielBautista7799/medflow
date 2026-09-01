import { AppBar, Toolbar, Typography } from "@mui/material";
import MedicalServicesIcon from '@mui/icons-material/MedicalServices'

function AppHeader(){
return (
        <AppBar position="static">
            <Toolbar>
                <MedicalServicesIcon sx = {{mr:2}} />
                <Typography variant="h6" component="h1">
                </Typography>
            </Toolbar>
        </AppBar>
    );
}

export default AppHeader;