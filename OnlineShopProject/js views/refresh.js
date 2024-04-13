function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');

    fetch('/api/token/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'refresh': refreshToken
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem('accessToken', data.access);
        // Now you can retry fetching the dashboard with the new access token
        fetchDashboard();
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle token refresh errors, e.g., redirect to login
    });
}
