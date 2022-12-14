from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class EmailAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):    
        if username is None:
            email = kwargs.get(User.EMAIL_FIELD)
        if username is None or password is None:
            return
        try:
            email = username
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        