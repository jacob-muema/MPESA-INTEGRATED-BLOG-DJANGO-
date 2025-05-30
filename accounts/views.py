from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse('admin_dashboard:dashboard')  # Redirect admin users here
        return reverse('blog:home')  # Redirect regular users here

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # DO NOT auto-login the user here
            messages.success(request, 'Registration successful! Please log in with your new account.')
            return redirect('accounts:login')  # Always redirect to login
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
