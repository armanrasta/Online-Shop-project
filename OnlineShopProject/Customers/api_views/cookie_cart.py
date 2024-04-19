from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_cookie_cart(request):
    cookie_cart = request.COOKIES.get('cookie_cart', '[]')
    return json.loads(cookie_cart)

def set_cookie_cart(response, cookie_cart):
    response.set_cookie('cookie_cart', json.dumps(cookie_cart), max_age=86400)

@csrf_exempt
def add_to_cookie_cart(request):
    if request.user.is_authenticated:
        return JsonResponse({'error': 'User is authenticated, use the database cart'}, status=400)

    cookie_cart = get_cookie_cart(request)
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Product ID is missing'}, status=400)
    
    quantity = int(request.POST.get('quantity', 1))
    product_exists = any(item['product_id'] == product_id for item in cookie_cart)

    if product_exists:
        for item in cookie_cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                break
    else:
        cookie_cart.append({'product_id': product_id, 'quantity': quantity})

    response = JsonResponse({'success': 'Item added to cookie cart'})
    set_cookie_cart(response, cookie_cart)
    return response

@csrf_exempt
def remove_from_cookie_cart(request):
    if request.user.is_authenticated:
        return JsonResponse({'error': 'User is authenticated, use the database cart'}, status=400)

    cookie_cart = get_cookie_cart(request)
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Product ID is missing'}, status=400)
    
    remove_entire_item = request.POST.get('remove_entire_item', 'false').lower() == 'true'
    updated_cart = [item for item in cookie_cart if not (item['product_id'] == product_id and (remove_entire_item or item['quantity'] <= 1))]

    if len(updated_cart) < len(cookie_cart):
        for item in updated_cart:
            if item['product_id'] == product_id:
                item['quantity'] -= 1
                break

    response = JsonResponse({'success': 'Item updated in cookie cart'})
    set_cookie_cart(response, updated_cart)
    return response
