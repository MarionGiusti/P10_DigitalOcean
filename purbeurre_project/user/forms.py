"""
User forms for registration
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    """ Form to create a user"""
    class Meta:
        """ Indicate which model to use, here User and the required fields"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']
