from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

class CustomerBackend(BaseBackend):
    def authenticate(self, request,email=None, password=None, **kwargs):
        if email is None or password is None:
            return
        try:
            UserModel = get_user_model()
            user = UserModel.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except user.DoesNotExist:
            raise ValidationError(_("Invalid username/email or password."))

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            return user if self.user_can_authenticate(user) else None
        except UserModel.DoesNotExist:
            return None
