from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('root_home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('root_home')

def register_view(request):
    if request.method == 'POST':
        # Simple registration for demo purposes
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_page')
            
        is_host = request.POST.get('is_host') == 'on'
        user = User.objects.create_user(username=username, password=password, email=email, is_provider=is_host)
        login(request, user)
        messages.success(request, "Registration successful. Welcome!")
        return redirect('root_home')
        
    return render(request, 'users/register.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/login/')
def become_host(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_provider:
            user.is_provider = True
            user.save()
            messages.success(request, "You are now a host!")
        return redirect('host_dashboard')
    return render(request, 'users/become_host.html')

@login_required(login_url='/users/login/')
def review_host(request, host_id):
    host = get_object_or_404(User, id=host_id, is_provider=True)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    from .models import UserReview
                    UserReview.objects.create(
                        reviewer=request.user,
                        reviewee=host,
                        rating=rating,
                        comment=comment
                    )
                    messages.success(request, f"Review for host {host.username} added successfully!")
                    return redirect('trips')
                else:
                    messages.error(request, "Rating must be between 1 and 5.")
            except ValueError:
                messages.error(request, "Invalid rating.")
        else:
            messages.error(request, "Please provide both rating and comment.")
            
    return render(request, 'users/review_host.html', {'host': host})

def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    reviews_received = profile_user.reviews_received.all()
    context = {
        'profile_user': profile_user,
        'reviews_received': reviews_received,
    }
    return render(request, 'users/profile.html', context)
