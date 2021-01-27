"""
URL configuration to process result, detail, save and favorite pages.
"""
from django.urls import path

from . import views
from .views import SearchSubstituteListView, SubstituteDetailView, FavoritesListView

urlpatterns = [
	path('result/', SearchSubstituteListView.as_view(), name='results_substitute'),
	path('detail/<int:id>', SubstituteDetailView.as_view(), name='details_substitute'),
	path('save/', views.save_substitute, name='save_substitute'),
	path('favorites', FavoritesListView.as_view(), name='favorites_substitute')
]