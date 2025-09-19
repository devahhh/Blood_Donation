from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Donor  # assuming models are in same app
from django.contrib.auth.hashers import make_password

# View for About Us page
def about_us(request):
    return render(request, 'about-us.html')

# View for Article page
def article_detail(request):
    context = {"title": "Sample Article", "content": "This is a sample article."}
    return render(request, 'article.html', context)

# Homepage
def index(request):
    return render(request, 'index.html')

# Dashboard page (login required)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')




# ---------------------------
# SIGNUP VIEW
# ---------------------------
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        blood_type = request.POST.get('type')
        phone = request.POST.get('phone')

        # Prevent duplicate accounts
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # Create User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Create Donor profile
        Donor.objects.create(
            user=user,
            dob=dob,
            blood_type=blood_type,
            phone=phone,
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')


# ---------------------------
# LOGOUT VIEW
# ---------------------------
def logout_user(request):
    logout(request)
    return redirect('login')
