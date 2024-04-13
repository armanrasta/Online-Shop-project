function signUpOTP() {
    let username = document.getElementById('username').value;
    let phoneNumber = document.getElementById('phone_number').value;
    let firstName = document.getElementById('first_name').value;
    let lastName = document.getElementById('last_name').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    
    fetch('/api/signup_otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            phone_number :phoneNumber,
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.user_id) {
            sessionStorage.setItem('user_id', data.user_id);
            alert(data.success);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
document.getElementById('signUpButton').addEventListener('click', signUpOTP);

function createAccount() {
    let otp = document.getElementById('otp').value;
    let userId = sessionStorage.getItem('user-id');
    
    fetch('/api/create_account/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            otp: otp,
            user_id: userId,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.success);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
document.getElementById('createAccountButton').addEventListener('click', createAccount);