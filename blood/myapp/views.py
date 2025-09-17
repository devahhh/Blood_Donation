from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
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

# Login page
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')

# Signup page
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password =make_password(request.POST.get('password'))  # Use a secure method to hash passwords
        dob = request.POST.get('dob')
        blood_type = request.POST.get('type')
        phone = request.POST.get('phone')

        # Save to DB
        Donor.objects.create(
            email=email,
            password=password,  # NOTE: This is insecure, see below!
            dob=dob,
            blood_type=blood_type,
            phone=phone,
        )
        return redirect('login')
    return render(request, 'signup.html')
