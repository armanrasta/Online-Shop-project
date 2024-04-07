function loginOtp() {
    let emailOrUsername = document.getElementById('emailOrUsername').value;
    let password = document.getElementById('password').value;

    fetch('/api/login-otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'username or email': emailOrUsername,
            'password': password
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert(data.success);
            sessionStorage.setItem('user_id', data.user_id);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
document.getElementById('loginButton').addEventListener('click', loginOtp);

//login
function login() {
    let OTP = document.getElementById('OTP').value;
    let uuid = sessionStorage.getItem('user_id');
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            otp: OTP,
            user_id: uuid
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                // Store the JWT in localStorage
                localStorage.setItem('jwt', data.access);
                alert('Welcome to Online Shop :)');
            } else {
                // Handle any errors, such as invalid OTP
                console.error('Error:', data.error);
                alert(data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
document.getElementById('loginButton').addEventListener('click', login);;