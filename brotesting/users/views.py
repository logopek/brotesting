from django.shortcuts import redirect, render
from django.contrib.auth import logout
from users.forms import UserRegistrationForm, UserLoginForm, UserPasswordResetForm

# Create your views here.


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('core:index')


def login_view(request):
    """Handle user login."""
    form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def registration_view(request):
    """Handle user registration."""
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    return render(
        request,
        'registration/registration_form.html',
        {'form': form}
    )


def password_reset_view(request):
    """Handle password reset."""
    form = UserPasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


def password_reset_done_view(request):
    """Handle password reset done."""
    return render(request, 'registration/password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    """Handle password reset confirm."""
    return render(request, 'registration/password_reset_confirm.html')


def password_reset_complete_view(request):
    """Handle password reset complete."""
    return render(request, 'registration/password_reset_complete.html')
