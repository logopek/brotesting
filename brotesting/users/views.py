from django.shortcuts import redirect, render
from users.forms import UserRegistrationForm

# Create your views here.


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
