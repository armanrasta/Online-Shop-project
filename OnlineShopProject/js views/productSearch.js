document.getElementById('product-search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var nameContains = document.getElementById('name-contains').value;
    var brandContains = document.getElementById('brand-contains').value;
    var minPrice = document.getElementById('min-price').value;
    var maxPrice = document.getElementById('max-price').value;
    
    var queryParams = new URLSearchParams({
        name_contains: nameContains,
        brand_contains: brandContains,
        min_price: minPrice,
        max_price: maxPrice
    }).toString();
  
    fetch('api/search-products?' + queryParams, {
        method: 'POST',
        // Additional options like headers, body, etc.
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});