from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Product, FavoriteProduct

class SearchSubstituteListView(ListView):
    model = Product
    paginate_by = 9
    template_name = 'catalogue/results_substitute.html'
    def get_queryset(self):
        query = self.request.GET.get('query')
        prod_to_change= Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(generic_name__icontains=query) 
        ).order_by('product_name').first()
        # prod_to_change = product_list[0]
        if prod_to_change is not None:
        # if prod_to_change.exists():
            print('BOUUUUUUUUUh',prod_to_change.nutri_grades, prod_to_change.nova_gps, prod_to_change.id)

            substitute_list = Product.objects.filter(
                (Q(product_name__icontains=query) | Q(generic_name__icontains=query)) & 
                (
                (Q(pnns_gps1=prod_to_change.pnns_gps1) | Q(pnns_gps1=prod_to_change.pnns_gps2)) &
                (Q(pnns_gps2=prod_to_change.pnns_gps1) | Q(pnns_gps2=prod_to_change.pnns_gps2))
                ) &
                (
                (Q(nutri_grades__lte=prod_to_change.nutri_grades) & Q(nova_gps__lt=prod_to_change.nova_gps)) |
                (Q(nutri_grades__lt=prod_to_change.nutri_grades) & Q(nova_gps__lte=prod_to_change.nova_gps))
                )
            ).order_by('product_name')

            for substitute in substitute_list:
               print('LAAAAAAAAAA',substitute.product_name, substitute.nutri_grades, substitute.nova_gps, substitute.code_prod, substitute.id)

        else:
            print("choubibibi")
            substitute_list = []
        
        return substitute_list

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        prod_to_change= Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(generic_name__icontains=query) 
        ).order_by('product_name').first()



        context = super().get_context_data(**kwargs)
        context['query'] = query
        if prod_to_change is not None:
            context['product'] = prod_to_change
        return context



class SubstituteDetailView(DetailView):
    model = Product
    template_name = 'catalogue/details_substitute.html'

    # def get_object(self):
    #     id_ = self.kwargs.get("id")
    #     return get_object_or_404(Product, id=id_)

@login_required(login_url='/user/login/')
def save_substitute(request):
    if request.method == 'POST':
        substitute_id = request.POST["substitute_id"]
        product_id = request.POST["product_id"]
        user_id = request.user.id
        page = request.POST["next"]

        print("CHOUUUUBIDOU",substitute_id, product_id, page)
        if substitute_id and product_id and user_id:
            with transaction.atomic():
                fav, created = FavoriteProduct.objects.get_or_create(
                    user_id = user_id,
                    product_id = product_id,
                    substitute_id = substitute_id,)

                if created:
                    messages.add_message(request, messages.SUCCESS, "Le substitut a bien été enregistré dans vos favoris !")
                else:
                    messages.add_message(request, messages.INFO, "Le substitut est déjà enregistré dans vos favoris !")
    return redirect(page)


class FavoritesListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 9
    template_name = 'catalogue/favorites_substitute.html'
    def get_queryset(self):
        favorites_list = FavoriteProduct.objects.filter(user_id=self.request.user.id).order_by("product")
        return favorites_list

