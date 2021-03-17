"""
User forms for registration
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from user.models import Profile

class CreateUserForm(UserCreationForm):
    """ Form to create a user"""
    class Meta:
        """ Indicate which model to use, here User and the required fields"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(ModelForm):
    # email = forms.EmailField()
    class Meta:
        """ Indicate which model to use, here User and the required fields"""
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']
        