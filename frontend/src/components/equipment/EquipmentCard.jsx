import { Card, CardContent, Typography, Chip, Stack} from '@mui/material';

const LOW_CHARGE_THRESHOLD = 20;

function EquipmentCard({equipment}) {
    const isLowCharge = equipment.chargeLevel < LOW_CHARGE_THRESHOLD
    return(
        <Card variant="outlined" sx={{minWidth: 240}}>
            <CardContent>
                <Typography variant="h6" component="div">
                    {equipment.serialNumber}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                    {equipment.model}
                </Typography>

                <Stack direction="row" spacing={1} alignItems="center">
                    <Chip
                        label={`${equipment.chargeLevel}% charge`}
                        color= {isLowCharge ? 'error' : 'success'}
                        size="small"
                            />
                    <Chip
                        label={equipment.status}
                        variant="outlined"
                        size="small"
                        />
                </Stack>
            </CardContent>
        </Card>
    );
}

export default EquipmentCard;