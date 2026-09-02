import { createContext, useContext, useMemo, useState } from 'react';
import apiClient from '../api/client.js';

/**authcontext creates empty context */
const AuthContext = createContext(null);

/** Take the JWT, grab its middle payload section, decode it, and turn it into a JavaScript object we can actually use.
 * token : HEADER.PAYLOAD.SIGNATURE
 * atob makes base64 token into json
 * parse json into javascript
 */

function decodeToken(token) {
    const payloadSegment = token.split('.')[1];
    return JSON.parse(atob(payloadSegment));
}

/** children means it is in between tags and authprovider is outside it (parent) */
export function AuthProvider({ children }) {

// On startup, check localStorage for a saved MedFlow token.
// token holds the current value, and setToken() is used to change it.
    const [token, setToken] = useState(() =>
        localStorage.getItem('medFlowToken')
    );

    // if token decode token else null
    //use memo updates if it senses a change in what it is put at seoncond comma [token]
    // () jsut says run this function and its the if else statement when senses change (null to begin with)
    const user = useMemo(
        () => (token ? decodeToken(token) : null),
        [token]
    );

    //create async funct login
    const login = async (username, password) => {
        // Create form data so the username and password are formatted for OAuth2PasswordRequestForm to parse 
        // it does not automatically know its url encoded but its is a fromat it can undestand
        const formData = new URLSearchParams();
        
        formData.append('username', username);
        formData.append('password', password);

        // POST sends the login form to FastAPI; await waits for the response.
        // Format: post(URL, DATA, CONFIG)
        const response = await apiClient.post('/auth/token', formData, {
        headers: {
            // URLSearchParams formats the data; this header tells FastAPI what format the request body uses.
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        });

        //set medflowtoken in local storage after response
        localStorage.setItem('medFlowToken', response.data.access_token);
        //set for usestate earlier
        setToken(response.data.access_token);
    };

    //logout function
    const logout = () => {
        localStorage.removeItem('medFlowToken');
        setToken(null);
    };

    // Bundle the auth data/functions that will be shared through AuthContext.
    const value = {
        token,
        user,
        isAuthenticated: Boolean(token),
        login,
        logout,
    };

    // Give AuthContext our auth data so all children can access it provider puts and value is what is put
    //children MAKE value accesible to all children
    return (
        <AuthContext.Provider value={value}>
        {children}
        </AuthContext.Provider>
    );
}

// GET the shared AuthContext value so child components can access the auth data and functions.

export function useAuth() {
    const context = useContext(AuthContext);

    if (context === null) {
        throw new Error('useAuth must be used within AuthProvider');
    }

    return context;
}