"""
Custom management command used to request API OpenFoodFacts and
import data in the database.
"""
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
        """ Method to:
        Request the API to get categories with more than 7000.
        Import the categories in the database """
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
        """ Method to:
        Request the API to import products from each category.
        Returns a json file with the products of the category"""
        search_url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        headers = {"User-Agent": "P8_PurBeurre - Version 1.0"}
        
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
            "page_size": 300,
            "json": True
            }

        req = requests.get(search_url, params=payload, headers=headers)
        if req.status_code == 200:
            results_json = req.json()
            products_json = results_json["products"]           
            return products_json

    def insert_product(self, products, category):
        """Method to insert products from a category in the database """
        products_resu = []
        for prod in products:
            product_resu = {
                k : v for k, v in prod.items()
                if k in CHOSEN_FIELDS and v != ""
                }
            if len(product_resu) == len(CHOSEN_FIELDS):
                try:
                    with transaction.atomic():
                        product, _ = Product.objects.update_or_create(
                            code_prod=product_resu.get("code"),
                            defaults={
                                'product_name' : product_resu.get("product_name_fr"),
                                'generic_name' : product_resu.get("generic_name_fr"),
                                'brand_name' : product_resu.get("brands"),
                                'url' : product_resu.get("url"),
                                'nova_gps' : product_resu.get("nova_groups"),
                                'nutri_grades' : product_resu.get("nutrition_grades"),
                                'pnns_gps1' : product_resu.get("pnns_groups_1"),
                                'pnns_gps2' : product_resu.get("pnns_groups_2"),
                                'store_name' : product_resu.get("stores"),
                                'picture' : product_resu.get("image_url"),
                                'fat_100g' : product_resu["nutriments"].get("fat_100g"),
                                'saturated_fat_100g' : product_resu["nutriments"].get("saturated-fat_100g"),
                                'salt_100g' : product_resu["nutriments"].get("salt_100g"),
                                'sugars_100g' : product_resu["nutriments"].get("sugars_100g")
                            },
                        )

                        cat = Category.objects.get(name=category)
                        product.categories.add(cat.id)

                except IntegrityError as err:
                    print("Une erreur est intervenue dans l'insertion ou la mise à jour d'un produit: ", err)

    def handle(self, *args, **options):
        """Main method to import the data in the database """
        selected_categories = self.get_biggest_categories()
        print(selected_categories)
        
        for category in selected_categories:
            try:
                products = self.get_product_from_category(category)
                self.insert_product(products, category)
                self.stdout.write(self.style.SUCCESS('Importation des données OpenFoodFacts réussie ! '))

            except Exception as err:
                raise CommandError("Echec dans l'importation des données de l'OpenFoodFacts: ", err)