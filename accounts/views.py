from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from donors.models import DonorProfile


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto login after registration
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Blood Management System.')
            
            # Redirect based on user type
            if user.user_type == 'donor':
                # Check if donor profile exists, if not redirect to create profile
                if not hasattr(user, 'donor_profile'):
                    messages.info(request, 'Please complete your donor profile.')
                    return redirect('donor_profile_create')
                return redirect('donor_dashboard')
            else:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on user type
                if user.user_type == 'donor':
                    return redirect('donor_dashboard')
                else:
                    return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def home_view(request):
    """Home page view"""
    return render(request, 'home.html')
