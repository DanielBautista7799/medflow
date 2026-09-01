import {Grid} from '@mui/material'
import EquipmentCard from './EquipmentCard'

function EquipmentList({equipment}){
    return(
        <Grid container spacing={2}>
            {equipment.map((item) => (
                <Grid item key={item.id}>
                    <EquipmentCard equipment={item} />
                </Grid>
            ))}
        </Grid>
    );
}

export default EquipmentList;