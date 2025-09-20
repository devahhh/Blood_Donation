from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *  # assuming models are in same app
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings

# View for About Us page
def about_us(request):
    return render(request, 'about-us.html')

# View for Article page
def article_detail(request):
    context = {"title": "Sample Article", "content": "This is a sample article."}
    return render(request, 'article.html', context)

# Homepage
def index(request):
    donors = BloodRequest.objects.all().order_by('-request_date')
    return render(request, 'index.html',{'donors': donors})

# Dashboard page (login required)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def hospital_dashboard(request):
    hospital_id = request.session.get('hospital_id')
    if not hospital_id:
        return redirect('login')
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        blood_type = request.POST.get('blood_type')
        quantity = request.POST.get('units_needed')
        hospital = Hospital.objects.get(id=hospital_id)
        BloodRequest.objects.create(
            hospital=hospital,
            patient_name=patient_name,
            blood_type=blood_type,
            quantity=quantity
        )
        messages.success(request, "Blood request created successfully!")
        donors=Donor.objects.filter(blood_type=blood_type)
        for donor in donors:
            send_mail(
                'Blood Donation Request',
                f'Dear {donor.user.first_name},\n\nA hospital has requested {quantity} units of blood type {blood_type} for patient {patient_name}. If you are willing to donate, please contact the hospital at {hospital.phone} or {hospital.email}.\n\nThank you for your support!\n\nBest regards,\nBlood Donation Team',
                settings.EMAIL_HOST_USER,
                [donor.user.email],
                fail_silently=False,
            )
            if donor.requests == "":
                donor.requests = f"{hospital.name} ({patient_name})"
            else:
                donor.requests += f", {hospital.name} ({patient_name})"
            
        return redirect('hospital_dashboard')
    hospital = Hospital.objects.get(id=hospital_id)
    requests = BloodRequest.objects.filter(hospital=hospital).order_by('-request_date')
    return render(request, 'hospitaldash.html', {'requests': requests, 'hospital': hospital, 'blood_types': blood_types()})




# ---------------------------
# SIGNUP VIEW
# ---------------------------
def signup(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email = request.POST.get('email').lower()
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
            first_name=name,
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
   
    return render(request, 'signup.html', {'emails': emails(), 'phones': phone_numbers(), 'blood_types': blood_types()})

def signup_hospital(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        Hospital.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            address=address,
            phone=phone,
        )
        

        messages.success(request, "Hospital account created successfully! Please log in.")
        return redirect('login')
   
    return render(request, 'signuphos.html', {'emails': emails(), 'phones': phone_numbers()})
# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            hospital = Hospital.objects.get(email=email)
            if hospital and check_password(password, hospital.password):
                print("Hospital logged in")
                request.session['hospital_id'] = hospital.id
                return redirect('hospital_dashboard')
            
            else:
                messages.warning(request,"Invalid email or password")

    return render(request, 'login.html')

def emails():
    hospitals = Hospital.objects.all()
    donors=User.objects.all()
    email_list = [hospital.email for hospital in hospitals] + [donor.email for donor in donors]
    return email_list
def phone_numbers():
    hospitals = Hospital.objects.all()
    donors=Donor.objects.all()
    phone_list = [hospital.phone for hospital in hospitals] + [donor.phone for donor in donors]
    return phone_list
def blood_types():
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return blood_types
# ---------------------------
# LOGOUT VIEW
# ---------------------------
def logout_user(request):
    logout(request)
    return redirect('login')

