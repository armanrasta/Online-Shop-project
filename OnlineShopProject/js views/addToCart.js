async function addToCart(productId, quantity) {
    const url = 'api/add-to-cart/';

    const accessToken = localStorage.getItem('accessToken');

    if (!jwtToken) {
        console.error('JWT token not found in session storage');
        return;
    }

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    };

    try {
        const response = await fetch(url, requestOptions);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to add item to cart');
        }
        const responseData = await response.json();
        return responseData;
    } catch (error) {
        console.error('Error:', error.message);
        throw error;
    }
}

// Usage example
const productId = 'your-product-id';  // Replace 'your-product-id' with the actual product ID
const quantity = 1;  // Set the desired quantity
addToCart(productId, quantity)
    .then(data => console.log('Success:', data))
    .catch(error => console.error('Error:', error));
