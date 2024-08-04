from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate ,logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import HostRegistrationForm, ParticipantRegistrationForm

def home(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['Host', 'Participant']:
            return redirect('login', role=role)
    
    # Fetch events for participants
    user_events = []
    if request.user.is_authenticated and request.user.role == 'PARTICIPANT':
        user_events = request.user.participating_events.all()

    return render(request, 'user/home.html', {'user_events': user_events})

def login(request, role):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == role.upper():
                auth_login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'user/login.html', {'form': form, 'role': role})

def register(request, role):
    if role == 'Host':
        form = HostRegistrationForm(request.POST or None)
    elif role == 'Participant':
        form = ParticipantRegistrationForm(request.POST or None)
    else:
        return redirect('home')
    
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        if role == 'Host':
            user.role = User.Role.HOST
        elif role == 'Participant':
            user.role = User.Role.PARTICIPANT
        user.save()
        auth_login(request, user)
        return redirect('home')

    return render(request, 'user/register.html', {'form': form, 'role': role})

def logout(request):
    auth_logout(request)
    return redirect('home')
