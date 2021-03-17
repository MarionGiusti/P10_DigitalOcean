"""
Define routes for the application "User" (login, logout, register, account)
and responses to HTTP request object
"""
import logging

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from user.forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

def register_page(request):
    """ Process the user's registration
    Returns:
    redirects to user login page if user created
    """ 
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Un compte a bien été créé pour ' + user)

            return redirect('user:login')
    logger.info('New user', exc_info=True)
    context = {'form':form}
    return render(request, 'user/register.html', context)

def login_page(request):
    """ Process the login of the user
    Returns: redirects to home page if user is authentificated
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, "Nom d'utilisateur OU Mot de passe incorrect")
    logger.info('New connexion', exc_info=True)
    context = {}
    return render(request, 'user/login.html', context)

def logout_user(request):
    """ Process the logout of the user
    Returns: redirects to home page
    """
    logout(request)
    return redirect('home')

def account(request):
    """ Process the account of the user
    Returns: the account page
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre compte a bien été modifié !')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
        }

    return render(request, 'user/account.html', context)
    