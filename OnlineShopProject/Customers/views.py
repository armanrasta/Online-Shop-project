from django.shortcuts import render

# Create your views here.

def address_page(request):
    return render(request, 'Customers/address.html', {'user': request.user})