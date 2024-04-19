document.addEventListener("DOMContentLoaded", function () {
    // Function to fetch and display addresses
    function fetchAddresses() {
        fetch('/api/addresses/', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            // Display addresses in a list or table format
            // Include options to edit or delete each address
            const addressesContainer = document.getElementById('addresses-container');
            addressesContainer.innerHTML = ''; // Clear previous addresses
            data.forEach(address => {
                const addressElement = document.createElement('div');
                addressElement.innerHTML = `
                    <p>${address.full_address}</p>
                    <button onclick="editAddress(${address.id})">Edit</button>
                    <button onclick="deleteAddress(${address.id})">Delete</button>
                `;
                addressesContainer.appendChild(addressElement);
            });
        })
        .catch(error => {
            console.error('Error fetching addresses:', error);
        });
    }

    // Fetch and display addresses on page load
    fetchAddresses();

    // Function to edit an existing address
    function editAddress(addressId) {
        fetch(`/api/addresses/${addressId}/`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
            },
        })
        .then(response => response.json())
        .then(address => {
            // Populate a form with the address details for editing
            // Provide options to save changes or delete the address
            // Handle form submission to send a PUT request to update the address
        })
        .catch(error => {
            console.error('Error fetching address:', error);
        });
    }

    // Function to delete an address
    function deleteAddress(addressId) {
        if (confirm('Are you sure you want to delete this address?')) {
            fetch(`/api/addresses/${addressId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
                },
            })
            .then(response => {
                if (response.ok) {
                    // Address deleted successfully, fetch and display updated list of addresses
                    fetchAddresses();
                } else {
                    throw new Error('Failed to delete address');
                }
            })
            .catch(error => {
                console.error('Error deleting address:', error);
            });
        }
    }

    // Function to add a new address
    function addAddress(formData) {
        fetch('/api/addresses/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            if (response.ok) {
                // Address added successfully, fetch and display updated list of addresses
                fetchAddresses();
            } else {
                throw new Error('Failed to add address');
            }
        })
        .catch(error => {
            console.error('Error adding address:', error);
        });
    }

    // Handle form submission for adding a new address
    const addAddressForm = document.getElementById('add-address-form'); // Assuming your form has the ID 'add-address-form'
    addAddressForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Collect form data
        const formData = {
            postal_code: document.getElementById('postal-code').value,
            country: document.getElementById('country').value,
            state: document.getElementById('state').value,
            city: document.getElementById('city').value,
            full_address: document.getElementById('full-address').value,
            extra_description: document.getElementById('extra-description').value,
            // Add more fields as needed
        };
        addAddress(formData);
    });
});
