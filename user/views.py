"""
Define routes for the application "User" (login, logout, register, account)
and responses to HTTP request object
"""
import logging

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from user.forms import CreateUserForm

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

            return redirect('user:login') # redirect to login page

    logger.info('New user', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information
        # we can
       'request':request,
    })

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
    context = {}
    return render(request, 'user/account.html', context)
