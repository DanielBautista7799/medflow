import { useState } from 'react';
import { Alert, Box, Button, Paper, TextField, Typography } from '@mui/material';
import { useAuth } from '../../context/AuthContext.jsx';

function LoginForm(){
    //call login function from use get auth value
    const { login } = useAuth();
    //use state means set var to inside () set with second var
    const [username,setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] =useState(null);

    // Submit the login form without refreshing; show an error if login fails.
    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);    
        try {
            await login(username, password);
        } catch (err) {
            if (err.response?.status === 401) {
                setError('Incorrect Username or password');
            } else {
                setError('Something went wrong logging in, please try again shortly');
            }
        }
    }

    //paper styled box form tells it to be a form psprt is just a visual container
    //if error then alert error and set error and display
    //update username as it is typed
return (
    <Box sx={{display: 'flex', justifyContent: 'center', mt: 8}}>
        <Paper
            component="form"
            onSubmit={handleSubmit}
            variant="outlined"
            sx={{p:4, width: 320}}>
                <Typography variant="h6" gutterBottom>
                    MedFlow Login
                </Typography>
                {error && (
                    <Alert severity="error" sx={{mb:2}}>
                        {error}
                    </Alert>
                )}
                <TextField
                    label = "Username"
                    fullWidth
                    margin="normal"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)} />
                <TextField 
                    label = "Password"
                    type = "password"
                    fullWidth
                    margin = "normal"
                    value = {password}
                    onChange={(event) => setPassword(event.target.value)} />
                    <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
                            Log In
                    </Button>
            </Paper>

    </Box>
);

}
export default LoginForm;