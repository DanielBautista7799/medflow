import { Container, Typography, Box } from '@mui/material';

import AppHeader from './components/layout/AppHeader.jsx';
import EquipmentList from './components/equipment/EquipmentList.jsx';
import DiscrepancyList from './components/workOrders/DiscrepancyList.jsx';

import { mockEquipment } from './mockData/equipment.js';
import { mockDiscrepancies } from './mockData/discrepancies.js';

function App(){
  return(
    <>
      <AppHeader />
      <Container sx={{mb:4}}>
        <Box sx={{mb:4}}>
          <Typography variant="h4" gutterBottom>
            Equipment Overview
          </Typography>
          <EquipmentList equipment={mockEquipment} />

        </Box>
        <Box sx={{mb:4}}>
          <Typography variant="h4" gutterBottom>
            Co-Location Discrepancies
          </Typography>
          <DiscrepancyList discrepancies={mockDiscrepancies} />
          
        </Box>
      </Container>
    
    
    </>
  );
}

export default App;