
import psycopg2
import json
import requests

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from catalogue.models import Product, Category
from .constants import CHOSEN_FIELDS


class Command(BaseCommand):
    help = 'Create and Update my database with the OpenFoodFacts API'


    def get_biggest_categories(self):
        """ request to get categories with more than 7000 """
        selected_categories = []
        category_url = "https://fr.openfoodfacts.org/categories.json"
        headers = {"User-Agent": "P8_PurBeurre - Version 1.0"}
        req = requests.get(category_url, headers=headers)
        if req.status_code == 200:
            results_json = req.json()
            category = results_json["tags"]
            i = 0
            for cat in category:
                if cat["products"] >= 7000:
                    try:
                        selected_categories.append(cat["name"])
                        db_categories = Category(name=cat["name"])
                        if Category.objects.filter(name=cat.get("name")).exists():
                            print(f"La catégorie {selected_categories[i]}, existe déjà")
                        else:
                            db_categories.save()
                            print(f"La catégorie {selected_categories[i]}, a été enregistrée")
                    except Exception as err:
                        print(f"La catégorie {selected_categories[i]}, n'a pu être importée. Erreur: {err}")
                i += 1
            return selected_categories

        else:
            self.stdout.write(self.style.ERROR("Désolé, impossible d'accéder à la liste des catégories de l'API OpenFoodFacts..."))

    def get_product_from_category(self, category):
        """ request to import products from each category """
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        headers = {"User-Agent": "P8_PurBeurre - Version 1.0"}
        # Record products by category in the dictionnary json_cat_prod
        # self.json_category_product = {}
        # print(f"Requêtes importation des produits de la catégorie {category}")
        
        # i = 1
        # products_resu = []
        # for i in range(1, 7):
        # Search criteria for API
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "tagtype_1": "countries",
            "tag_contains_1": "contains",
            "tag_1": "france",
            "tagtype_2": "categories_lc",
            "tag_contains_2": "contains",
            "tag_2": "fr",
            # Sort by popularity
            "sort_by": "unique_scans_n",
            # "page": i,
            "page_size": 300,
            "json": True
            }

        req = requests.get(search_url, params=payload, headers=headers)
        if req.status_code == 200:
            results_json = req.json()
            products_json = results_json["products"]

            return products_json
                # for product in products_json:
                #     product_resu = {
                #         k : v for k, v in product.items()
                #         if k in CHOSEN_FIELDS and v != ""
                #     }
                #     if len(product_resu) == len(CHOSEN_FIELDS):
                #         products_resu.append(product_resu)
            # print(" Catégorie '{}': {} produits importés de l'API Open Food Facts \n" \
            #     .format(category, len(products_resu)))
            # self.json_category_product[category] = products_resu 
            # # Can save the data in a json file
            # with open('json_cat_prod.json','w') as f:
            #     f.write(json.dumps(self.json_cat_prod, indent=4))
            # else:
            #     self.stdout.write(self.style.ERROR("Désolé, impossible d'importer les produits de l'API OpenFoodFacts..."))

    def update_product(self, product, detail):
        try:
            with transaction.atomic():
                product.product_name = detail.get("product_name_fr")
                product.generic_name = detail.get("generic_name_fr")
                product.code_prod = detail.get("code")
                product.brand_name = detail.get("brands")
                product.url = detail.get("url")
                product.nova_gps = detail.get("nova_groups")
                product.nutri_grades = detail.get("nutrition_grades")
                product.pnns_gps1 = detail.get("pnns_groups_1")
                product.pnns_gps2 = detail.get("pnns_groups_2")
                product.store_name = detail.get("stores")
                product.picture = detail.get("image_url")

                product.save()
        except IntegrityError as err:
            print("Une erreur est intervenue dans la mise à jour d'un produit: ", err)


    def insert_product(self, products):
        products_resu = []
        for prod in products:
            product_resu = {
                k : v for k, v in prod.items()
                if k in CHOSEN_FIELDS and v != ""
                }
            if len(product_resu) == len(CHOSEN_FIELDS):
                # products_resu.append(product_resu)
        # print(type(products_resu))                
        # print(products_resu)

                if Product.objects.filter(product_name=product_resu.get("product_name_fr")).exists():
                    product = Product.objects.get(product_name=product_resu.get("product_name_fr"))
                    # Update product
                    self.update_product(product, product_resu)
                else:
                    # Create product
                    try:
                        with transaction.atomic():
                            product = Product.objects.create(
                                product_name = product_resu.get("product_name_fr"),
                                generic_name = product_resu.get("generic_name_fr"),
                                code_prod = product_resu.get("code"),
                                brand_name = product_resu.get("brands"),
                                url = product_resu.get("url"),
                                nova_gps = product_resu.get("nova_groups"),
                                nutri_grades = product_resu.get("nutrition_grades"),
                                pnns_gps1 = product_resu.get("pnns_groups_1"),
                                pnns_gps2 = product_resu.get("pnns_groups_2"),
                                store_name = product_resu.get("stores"),
                                picture = product_resu.get("image_url"))

                            categories = product_resu.get("categories")
                            for category in categories.split(","):
                            #     # if category in selected_categories:
                                cat, _ = Category.objects.get_or_create(name=category)
                                
                                # print("YOP:", cat_id.id)
                                product.categories.add(cat_id.id)
                            product.save()

                    except IntegrityError as err:
                        print("Une erreur est intervenue dans l'insertion d'un produit: ", err)

    def handle(self, *args, **options):
        selected_categories = self.get_biggest_categories()
        
        for category in selected_categories:
            try:
                products = self.get_product_from_category(category)
                self.insert_product(products)

                # self.stdout.write(self.style.SUCCESS('Importation des données OpenFoodFacts réussie ! '))
                # raise Exception

            except Exception as err:
                raise CommandError("Echec dans l'importation des données de l'OpenFoodFacts: ", err)