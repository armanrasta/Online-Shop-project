from rest_framework.permissions import BasePermission
from .models import Operators

class IsOperator(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Operators)