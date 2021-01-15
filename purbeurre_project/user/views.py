from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.
from .forms import CreateUserForm

def index(request):
    context = {}
    return render(request, 'user/home.html', context)

def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Un compte a bien été créé pour ' + user)

            return redirect('login') # redirect to login page

    context = {'form':form}
    return render(request, 'user/register.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Nom d'utilisateur OU Mot de passe incorrect")

    context = {}
    return render(request, 'user/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')

def account(request):
    context = {}
    return render(request, 'user/account.html', context)


