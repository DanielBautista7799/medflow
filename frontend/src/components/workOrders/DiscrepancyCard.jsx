import { Alert, Card, CardContent, Typography, Stack} from '@mui/material';

function DiscrepancyCard({discrepancy}){
    return(
        <Card variant = "outlined" sx={{minWidth:240}}>
            <CardContent>
                <Typography variant="h6" component="div">
                    {discrepancy.title}
                </Typography>

                <Typography color="text.secondary" gutterBottom>
                    Work Order #{discrepancy.workOrderId}
                </Typography>

                <Stack spacing ={0.5} sx={{mb:1.5}}>
                    <Typography variant="body2">
                        Equipment Facility: {discrepancy.equipmentFacilityId}
                    </Typography>

                    <Typography variant="body2">
                        Technician Facility: {discrepancy.technicicanFacilityId}
                    </Typography>
                </Stack>

                <Alert severity="warning">
                    Facility Mismatch Detected
                </Alert>
            </CardContent>

        </Card>
    );
}
export default DiscrepancyCard;