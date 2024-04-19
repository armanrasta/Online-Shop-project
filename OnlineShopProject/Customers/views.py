from django.shortcuts import render

# Create your views here.

def address_page(request):
    return render(request, 'Customers/address.html', {'user': request.user})

def login(request):
    return render(request, 'Customers/login.html')

def login_otp(request):
    return render(request, 'Customers/login_otp.html')

def signup(request):
    return render(request, 'Customers/signup.html')

def sigup_otp(request):
    return render(request, 'Customers/signup_otp.html')