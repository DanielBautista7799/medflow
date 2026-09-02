import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {
    Alert,
    Box,
    CircularProgress,
    FormControl,
    InputLabel,
    MenuItem,
    Select
} from '@mui/material';

import apiClient from '../../api/client.js';

const PRIORITY_OPTIONS = ['', 'Low', 'Medium', 'Critical'];

//top of columns id , title, id , id and can be filled in by row gotten from schemas(api)

const columns = [
    { field: 'work_order_id', headerName: 'Work Order ID', width: 130 },
    { field: 'title', headerName: 'Title', width: 220 },
    { field: 'equipment_facility_id', headerName: 'Equipment Facility', width: 170, type: 'number' },
    { field: 'technician_facility_id', headerName: 'Technician Facility', width: 180, type: 'number' },
];

function DiscrepancyDataGrid(){
    //default vals
    const [priority, setPriority] = useState('');
    const [discrepancies, setDiscrepancies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        let isMounted = true;
        setLoading(true);

        async function fetchDiscrepancies(){
            try{
                    const response = await apiClient.get("/work-orders/discrepancies", {
                        params: {
                            priority: priority || undefined,
                        },
                    });
                    if(isMounted){
                        setDiscrepancies(response.data);
                    }
                } catch {
                    if(isMounted){
                        setError('Could not load discrepancy report');
                    }
                } finally {
                    if(isMounted){
                        setLoading(false);
                    }
                }
                
        }

        fetchDiscrepancies();
        return () =>{
            isMounted = false;
        }

    }, [priority]);

    return(
        <Box>
            <FormControl size="small" sx={{mb:2, minWidth:180}}>
                <InputLabel id ="priority-filter-label"> Priority </InputLabel>
        {/* Build each priority option: React tracks it with key all low medium critical, value is what gets selected, and "" is shown as "All". */}
                <Select
                    labelId="priority-filter-label"
                    label="Priority"
                    value={priority}
                    onChange = {(event) => setPriority(event.target.value)}>
                         {/* map separtes by option and key sets the id to each optioin */}
                        {PRIORITY_OPTIONS.map((option)=>(
                            <MenuItem key={option || 'All'} value={option}>
                                {option === '' ? 'All' : option}
                            </MenuItem>
                        ))}

                    </Select>
            </FormControl>

            {loading && <CircularProgress />}
            {error && (
                    <Alert severity="error">
                        {error}
                    </Alert>
            )}  
            {!loading && !error && (
            <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid
                    rows={discrepancies}
                    columns={columns}
                    getRowId={(row) => row.work_order_id}
                />
            </Box>
            )}    
        </Box>
    );


}

export default DiscrepancyDataGrid