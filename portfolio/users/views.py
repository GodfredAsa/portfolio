
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Profile

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist ')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('profiles')
        else:
            messages.error(request, 'username OR password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out ')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account successfully created")
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "An error occurred")
            
    context = {'page': page, 'form':form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # topSkills = profile.skill_set.exclude(description__exact = "") # profile skill with description 
    skills = profile.skill_set.filter() # profile skill without description 
    context = {'profile': profile, 'skills': skills}
    return render(request, 'users/user-profile.html', context)


