from django.shortcuts import render

# Create your views here.

def checkoutpage(request):
    return render(request, 'Orders/checkout.html', {'user': request.user})