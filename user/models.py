"""
Define models to use in the database
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile.png", null=True)

    def __str__(self):
        """Method to change the object name in QuerySet """
        return f'Profil {self.user.username}'

    class Meta:
        """Change model name in french"""
        verbose_name = "Profil"
