"""
URL configuration to display homepage and mentions page.
"""
from django.urls import path

from pages.views import HomePageView, MentionsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('mentions/', MentionsView.as_view(), name='mentions'),
]
