  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_to_cookie_cart(request):
    if not request.user.is_authenticated:
        # Retrieve the current cart from the cookies or create a new one if it doesn't exist
        cookie_cart = request.COOKIES.get('cookie_cart', '[]')
        cookie_cart = json.loads(cookie_cart)

        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Check if the product is already in the cart and update the quantity
        product_exists = False
        for item in cookie_cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                product_exists = True
                break

        # If the product is not in the cart, add it
        if not product_exists:
            cookie_cart.append({'product_id': product_id, 'quantity': quantity})

        # Create a response and add the updated cart to the cookies
        response = JsonResponse({'success': 'Item added to cookie cart'})
        response.set_cookie('cookie_cart', json.dumps(cookie_cart), max_age=3600)  # Expires in 1 hour

        return response
    else:
        # If the user is authenticated, you might want to handle this differently
        return JsonResponse({'error': 'User is authenticated, use the database cart'}, status=400)

# Remember to replace 'product_id' and 'quantity' with the actual POST data keys you are using.


@csrf_exempt
def remove_from_cookie_cart(request):
    if not request.user.is_authenticated:
        # Retrieve the current cart from the cookies
        cookie_cart = request.COOKIES.get('cookie_cart', '[]')
        cookie_cart = json.loads(cookie_cart)

        product_id = request.POST.get('product_id')
        remove_entire_item = request.POST.get('remove_entire_item', 'false').lower() == 'true'

        # Find the product in the cart and adjust the quantity or remove it
        updated_cart = []
        for item in cookie_cart:
            if item['product_id'] == product_id:
                if remove_entire_item or item['quantity'] <= 1:
                    continue  # Remove the item by not adding it to the updated cart
                else:
                    item['quantity'] -= 1  # Decrease the quantity by one
            updated_cart.append(item)

        # Create a response and update the cart in the cookies
        response = JsonResponse({'success': 'Item updated in cookie cart'})
        response.set_cookie('cookie_cart', json.dumps(updated_cart), max_age=3600)  # Expires in 1 hour

        return response
    else:
        # If the user is authenticated, handle this differently
        return JsonResponse({'error': 'User is authenticated, use the database cart'}, status=400)

# Remember to replace 'product_id' and 'remove_entire_item' with the actual POST data keys you are using.