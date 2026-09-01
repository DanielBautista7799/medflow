import DiscrepancyCard from "./DiscrepancyCard";
import { Grid } from "@mui/material";

function DiscrepancyList({discrepancies}){
    return(
        <Grid container spacing={2}>
            {discrepancies.map((discrepancy) => (
                <Grid item key={discrepancy.workOrderId}>
                    <DiscrepancyCard discrepancy={discrepancy} />
                </Grid>
            ))}
        </Grid>

    );
}
export default DiscrepancyList