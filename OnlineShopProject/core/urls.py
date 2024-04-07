"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import send_welcome_email

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("shop/", include('Product.urls')  ),
    path('send-welcome-email/', send_welcome_email, name='send_welcome_email'),
    path('api/', include('Customers.api_urls')),
    path('api/', include('Product.api_urls')),
    # path('api/', include('Orders.api_urls')),
]
