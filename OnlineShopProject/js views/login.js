function loginOtp() {
    let emailOrUsername = document.getElementById('emailOrUsername').value;
    let password = document.getElementById('password').value;

    fetch('/api/login-otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'username-or-email': emailOrUsername,
            'password': password
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert(data.success);
            sessionStorage.setItem('user-id', data.user_id);
        } else {
            console.error('Error:', data.error);
            alert(data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
document.getElementById('otpRequestButton').addEventListener('click', loginOtp);

//login
function login() {
    let OTP = document.getElementById('OTP').value;
    let uuid = sessionStorage.getItem('user-id');
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "otp": OTP,
            "user-id": uuid
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                alert('Welcome to Online Shop :)');
                sessionStorage.removeItem('user-id');
            } else {
                console.error('Error:', data.error);
                alert(data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
document.getElementById('loginButton').addEventListener('click', login);