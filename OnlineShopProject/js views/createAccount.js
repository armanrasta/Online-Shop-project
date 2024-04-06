const userId = 'the_user_id_received_from_send_otp';
const otpCode = sessionStorage.getItem('user_id') ;

const url = 'http://yourdomain.com/create_account';

const data = {
    user_id: userId,
    otp: otpCode
};

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
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });


