from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('blog:home')

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
