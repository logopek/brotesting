
from django.contrib.auth.forms import (UserCreationForm)
from users.models import User
from core.models import StudentGroup


class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = tuple(["username","email", "password1", "password2"])
