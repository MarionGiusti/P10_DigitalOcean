"""Filter the results from Product database model
"""
"""
Define routes for the application "Catalogue" (result, detail, save and favorite)
and responses to HTTP request object
"""
import logging

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404

from .models import Product, FavoriteProduct

# Get an instance of a logger
logger = logging.getLogger(__name__)

class SearchSubstituteListView(ListView):
    """Class-based generic ListView.
    Returns: results page with the substitutes."""
    model = Product
    paginate_by = 9
    template_name = 'catalogue/results_substitute.html'

    def get_queryset(self):
        """Override the get_queryset() and change the list of records returned.
        Returns: list of substitutes. Filter the Product database model
        depending of the first product corresponding to the query."""
        query = self.request.GET.get('query')
        prod_to_change= Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(generic_name__icontains=query)
        ).order_by('product_name').first()
        if prod_to_change is not None:
            substitute_list = []
            prod_to_change_cat = prod_to_change.categories.all()
            substitute_list = Product.objects.filter(
                (Q(categories__in=prod_to_change_cat)) &
                (
                (Q(pnns_gps1=prod_to_change.pnns_gps1) | Q(pnns_gps1=prod_to_change.pnns_gps2)) &
                (Q(pnns_gps2=prod_to_change.pnns_gps1) | Q(pnns_gps2=prod_to_change.pnns_gps2))
                ) &
                (
                (Q(nutri_grades__lt=prod_to_change.nutri_grades)) |
                (Q(nutri_grades__lte=prod_to_change.nutri_grades) & Q(nova_gps__lt=prod_to_change.nova_gps)) 
                )
            ).order_by('product_name')
        else:
            substitute_list = []

        return substitute_list

    def get_context_data(self, **kwargs):
        """Override the get_context_data() to pass additional context variables
        to the template.
        Returns: the query or the first product corresponding to the query
        and used to search substitutes."""
        query = self.request.GET.get('query')
        prod_to_change= Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(generic_name__icontains=query)
        ).order_by('product_name').first()

        context = super().get_context_data(**kwargs)
        context['query'] = query
        if prod_to_change is not None:
            context['product'] = prod_to_change
        logger.info('Search substitute', exc_info=True, extra={
            'request': context,
        })
        return context


class SubstituteDetailView(DetailView):
    """Class-based generic DetailView.
    Returns: results page with the detail of a substitute."""
    model = Product
    template_name = 'catalogue/details_substitute.html'

    def get_object(self):
        """Method to return the single object that this
        view will display, here the id of the product"""
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)

@login_required(login_url='/user/login/')
def save_substitute(request):
    """Function to save a substitute which will be displayed in favorite page.
    User needs to be login.
    Returns: redirects to the actual page """
    if request.method == 'POST':
        substitute_id = request.POST["substitute_id"]
        product_id = request.POST["product_id"]
        user_id = request.user.id
        page = request.POST["next"]

        if substitute_id and product_id and user_id:
            with transaction.atomic():
                fav, created = FavoriteProduct.objects.get_or_create(
                    user_id = user_id,
                    product_id = product_id,
                    substitute_id = substitute_id,)

                if created:
                    messages.add_message(
                        request, messages.SUCCESS,
                        "Le substitut a bien été enregistré dans vos favoris !"
                    )
                else:
                    messages.add_message(
                        request, messages.INFO,
                        "Le substitut est déjà enregistré dans vos favoris !"
                    )
    return redirect(page)


class FavoritesListView(LoginRequiredMixin, ListView):
    """Class-based generic ListView and LoginRequiredMixin.
    Requests by non-authenticated users will be redirected to the login page.
    Returns: favorite page with the saved substitutes of the login user."""
    model = Product
    paginate_by = 9
    template_name = 'catalogue/favorites_substitute.html'

    def get_queryset(self):
        """Override the get_queryset() and change the list of records returned.
        Returns: list of favorite substitutes for the login user."""
        favorites_list = FavoriteProduct.objects.filter(
            user_id=self.request.user.id
        ).order_by("product")
        return favorites_list
