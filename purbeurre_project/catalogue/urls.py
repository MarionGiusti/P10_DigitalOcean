from django.urls import path

from . import views
from .views import SearchSubstituteListView
# from .views import SearchProductListView

urlpatterns = [
	# path('search/', views.search, name="search_product"),
	# path('search/', SearchProductListView.as_view(), name='search_product'),
	path('result/', SearchSubstituteListView.as_view(), name='results_substitute'),
	# path('detail/', SubstituteDetailView.as_view(), name='detail_substitute')



]