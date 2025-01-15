from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       PasswordResetForm)
from users.models import User


class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('group_name',)


class UserLoginForm(AuthenticationForm):
    """Форма для входа в систему."""
    class Meta():
        model = User
        fields = ('username', 'password')


class UserPasswordResetForm(PasswordResetForm):
    """Форма для сброса пароля."""
    class Meta():
        model = User
        fields = ('email',)
