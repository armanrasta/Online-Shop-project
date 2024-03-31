
const url = 'http://yourdomain.com/send_otp';
const data = {};

const options = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
};

fetch(url, options)
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('user_id', data.user_id);
    })
    .catch(error => {
        console.error('Error:', error);
    });