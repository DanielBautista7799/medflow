import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'serial_number', headerName: 'Serial Number', width: 150 },
    { field: 'model', headerName: 'Model', width: 160 },
    { field: 'charge_level', headerName: 'Charge %', width: 120, type: 'number' },
    { field: 'status', headerName: 'Status', width: 130 },
    { field: 'facility_id', headerName: 'Facility ID', width: 110, type: 'number' },
];

function EquipmentDataGrid() {
    const [equipment, setEquipment] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;

        async function fetchEquipment() {
            try {
                const response = await apiClient.get('/equipment');

                if (isMounted) {
                    setEquipment(response.data);
                }
            } catch {
                if (isMounted) {
                    setError('Could not load equipment data.');
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        }

        fetchEquipment();

        return () => {
            isMounted = false;
        };
    }, []);

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error}</Alert>;

    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <DataGrid
                rows={equipment}
                columns={columns}
                getRowId={(row) => row.id}
            />
        </Box>
    );
}

export default EquipmentDataGrid;