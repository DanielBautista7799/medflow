import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {
    Alert,
    Box,
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    MenuItem,
    Stack,
    TextField,
} from '@mui/material';

import apiClient from '../../api/client.js';


const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'serial_number', headerName: 'Serial Number', width: 150 },
    { field: 'model', headerName: 'Model', width: 150 },
    { field: 'status', headerName: 'Status', width: 140 },
    { field: 'charge_level', headerName: 'Charge Level', width: 130 },
    { field: 'facility_id', headerName: 'Facility ID', width: 110 },
];


const STATUS_OPTIONS = [
  'Available',
  'In-Use',
  'Maintenance',
  'Offline',
];


function EquipmentDataGrid({ onSuccess }) {
    const [equipment, setEquipment] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [dialogOpen, setDialogOpen] = useState(false);

    const [formValues, setFormValues] = useState({
    serial_number: '',
    model: '',
    charge_level: '',
    facility_id: '',
    status: 'Available',
});


async function fetchEquipment() {
    setLoading(true);

    try {
        const response = await apiClient.get('/equipment');

        setEquipment(response.data);
        setError(null);
    } catch {
        setError('Could not load equipment data.');
    } finally {
        setLoading(false);
    }
}


  // Load equipment when the component first appears.
    useEffect(() => {
    fetchEquipment();
    }, []);


  // Updates whichever form field the user is typing in.
    const handleFieldChange = (field) => (event) => {
    setFormValues((prev) => ({
        ...prev,
        [field]: event.target.value,
    }));
};


  // Creates a new equipment record through the backend.
    const handleCreate = async () => {
    try {
        await apiClient.post('/equipment', {
        ...formValues,
        charge_level: Number(formValues.charge_level),
        facility_id: Number(formValues.facility_id),
        });

        setDialogOpen(false);

        setFormValues({
        serial_number: '',
        model: '',
        charge_level: '',
        facility_id: '',
        status: 'Available',
        });

        onSuccess(`Equipment ${formValues.serial_number} created.`);

        await fetchEquipment();
    } catch {
      // Leaving creation error handling simple for now.
    }
    };


    if (loading) {
        return <CircularProgress />;
    }


    if (error) {
        return <Alert severity="error">{error}</Alert>;
    }


return (
    <Box>

    <Button
        variant="outlined"
        sx={{ mb: 2 }}
        onClick={() => setDialogOpen(true)}
    >
        Add Equipment
    </Button>


    <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid
        rows={equipment}
        columns={columns}
        getRowId={(row) => row.id}
        />
    </Box>


    <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
    >
        <DialogTitle>Add New Equipment</DialogTitle>

        <DialogContent>
        <Stack spacing={2} sx={{ mt: 1, minWidth: 300 }}>

            <TextField
            label="Serial Number"
            value={formValues.serial_number}
            onChange={handleFieldChange('serial_number')}
            />

            <TextField
            label="Model"
            value={formValues.model}
            onChange={handleFieldChange('model')}
            />

            <TextField
            label="Charge Level"
            type="number"
            value={formValues.charge_level}
            onChange={handleFieldChange('charge_level')}
            />

            <TextField
            label="Facility ID"
            type="number"
            value={formValues.facility_id}
            onChange={handleFieldChange('facility_id')}
            />

            <TextField
            select
            label="Status"
            value={formValues.status}
            onChange={handleFieldChange('status')}
            >
            {STATUS_OPTIONS.map((option) => (
                <MenuItem
                key={option}
                value={option}
                >
                {option}
                </MenuItem>
            ))}
            </TextField>

        </Stack>
        </DialogContent>


        <DialogActions>
        <Button onClick={() => setDialogOpen(false)}>
            Cancel
        </Button>

        <Button
            variant="contained"
            onClick={handleCreate}
        >
            Create
        </Button>
        </DialogActions>

    </Dialog>

    </Box>
);
}


export default EquipmentDataGrid;