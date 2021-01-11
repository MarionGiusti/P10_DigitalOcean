from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category, Product

# class SearchProductListView(ListView):
#     model = Product
#     paginate_by = 9
#     template_name = 'catalogue/search_product.html'
#     def get_queryset(self):
#         query = self.request.GET.get('query')
#         product_list = Product.objects.filter(
#             Q(product_name__icontains=query) |
#             Q(generic_name__icontains=query)
#         ).order_by('product_name')
#         return product_list

#     def get_context_data(self, **kwargs):
#         query = self.request.GET.get('query')
#         context = super().get_context_data(**kwargs)
#         context['query'] = query
#         return context

class SearchSubstituteListView(ListView):
    model = Product
    paginate_by = 9
    template_name = 'catalogue/results_substitute.html'
    def get_queryset(self):
        query = self.request.GET.get('query')
        product_list = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(generic_name__icontains=query) 
        ).order_by('product_name')

        prod_to_change = product_list[0]
        print('BOUUUUUUUUUh',product_list[0].nutri_grades, product_list[0].nova_gps)

        substitute_list = Product.objects.filter(
            (Q(product_name__icontains=query) |
            Q(generic_name__icontains=query)) & 
            (Q(pnns_gps1=prod_to_change.pnns_gps1) | Q(pnns_gps1=prod_to_change.pnns_gps2)) &
            (Q(pnns_gps2=prod_to_change.pnns_gps1) | Q(pnns_gps2=prod_to_change.pnns_gps2))
        ).order_by('product_name')

        for substitute in substitute_list:
            if (substitute.nutri_grades <= prod_to_change.nutri_grades and \
             substitute.nova_gps < prod_to_change.nova_gps) | \
            (substitute.nutri_grades < prod_to_change.nutri_grades and \
                substitute.nova_gps <= prod_to_change.nova_gps) :
                print('LAAAAAAAAAA',substitute.product_name, substitute.nutri_grades, substitute.nova_gps, substitute.code_prod)

        return substitute_list

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        context = super().get_context_data(**kwargs)
        context['query'] = query
        return context

# class SubstituteDetailView(DetailView):
#     model = Product
#     template_name = 'catalogue/details_substitute.html'
#     def get_queryset(self):


# def search(request):
#     # query = request.GET.get('query', None)
#     # products = Product.objects.all()
#     # if query is not None:
#     #     products_list = products.filter(product_name__icontains=query)
#     query = request.GET.get('query')
#     products_list = Product.objects.filter(
#         Q(product_name__icontains=query) | 
#         Q(generic_name__icontains=query)
#     ).order_by('product_name')
#     context = {
#         'products_list': products_list
#     }
#     return render(request, 'catalogue/search_product.html', context)
    
# >>> prod
# <QuerySet [<Product: Gazpacho>, <Product: Gazpacho original sin gluten envase 1 l>, <Product: Gazpacho>, <Product: Gazpacho vert>]>
# >>> prod[1]
# <Product: Gazpacho original sin gluten envase 1 l>
# >>> prod[1].code_prod
# '8422174010029'
# >>> prod[1].fat_100g
# 2.6