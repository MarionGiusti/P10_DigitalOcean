from django.forms import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models

# Create your models here.
class CreateUserForm(UserCreationForm):
 # password2 = forms.CharField(
 #        label="Password confirmation",
 #        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder':'Pseudo'}),
 #        strip=False,
 #        help_text="Enter the same password as before, for verification.",
    
    # )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

