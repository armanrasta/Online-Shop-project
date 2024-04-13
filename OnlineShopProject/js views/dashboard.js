import {refreshAccessToken} from './refresh';

function fetchDashboard() {
    const accessToken = localStorage.getItem('accessToken');

    fetch('/api/dashboard', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 401) {
            // If the response is 401 (Unauthorized), try refreshing the access token
            refreshAccessToken();
            throw new Error('Access token expired');
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        console.log('Success:', data);
        // Handle the response data
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


fetchDashboard();
