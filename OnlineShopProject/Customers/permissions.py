from rest_framework.permissions import BasePermission
from .models import Customer

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Customer)