from django.contrib.auth.backends import ModelBackend
from Apis.models import AllUsers

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Try to fetch the user (could be Admin, User, or Company) by email
            user = AllUsers.objects.get(email=email)
            if user.check_password(password):  # Use the built-in password check
                return user
        except AllUsers.DoesNotExist:
            return None
        return None
