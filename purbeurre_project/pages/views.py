"""
Define routes for the application "Pages" (homepage and mentions)
and responses to HTTP request object
"""
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    """ Class-based generic view which uses the built-in TemplateView
    Returns: display the home page template
    """
    template_name = 'home.html'

class MentionsView(TemplateView):
    """ Class-based generic view which uses the built-in TemplateView
    Returns: display the terms of service (mentions) template
    """
    template_name = 'mentions.html'
    