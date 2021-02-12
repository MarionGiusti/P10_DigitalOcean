import os
import codecs
import json
from unittest.mock import patch

from django.test import TestCase

from catalogue.management.commands.database_import_off import Command
from catalogue.models import Category, Product

class ImportAPIDataTests(TestCase):
    @patch('requests.get')
    def test_request_ok_get_biggest_categories(self, mock_request):
        # set a `status_code` attribute on the mock object with value 200
        mock_request.return_value.status_code = 200
        # set fake content json
        mock_request.return_value.json.return_value = {
            "count": 18752,
            "tags": [
                {
                    "name": "Aliments et boissons à base de végétaux",
                    "products": 99241,
                    "known": 1,
                    "url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux",
                    "id": "en:plant-based-foods-and-beverages"
                },
                {
                    "products": 85214,
                    "known": 1,
                    "name": "Aliments d'origine végétale",
                    "id": "en:plant-based-foods",
                    "url": "https://fr.openfoodfacts.org/categorie/aliments-d-origine-vegetale"
                }
            ]
        }

        command = Command()
        selected_cat = command.get_biggest_categories()
        mock_request.assert_called_with(
            "https://fr.openfoodfacts.org/categories.json",
            headers={"User-Agent": "P8_PurBeurre - Version 1.0"}
        )
        self.assertEqual(
            selected_cat,
            ['Aliments et boissons à base de végétaux',
            "Aliments d'origine végétale"]
        )
        self.assertEqual(Category.objects.count(), 2)

    @patch('requests.get')
    def test_request_ok_get_product_from_category(self, mock_request):
        # set a `status_code` attribute on the mock object with value 200
        mock_request.return_value.status_code = 200
        # set fake content json
        with codecs.open(os.path.join(os.path.dirname(__file__),
        "dataSet_json_cat_prod_mock.json"),"r", encoding='utf-8') as read_file:
            data = json.loads(read_file.read())
        mock_request.return_value.json.return_value = data

        command = Command()
        selected_prod_from_cat = command.get_product_from_category("Produits à tartiner")
        self.assertEqual(data["products"], selected_prod_from_cat)

    def test_insert_product(self):
        Category.objects.create(name="Pâte à tartiner")
        with codecs.open(os.path.join(os.path.dirname(__file__),
            "dataSet_json_cat_prod_mock.json"),"r", encoding='utf-8') as read_file:
            data = json.loads(read_file.read())
        products = data["products"]
        command = Command()
        command.insert_product(products, "Pâte à tartiner")
        self.assertEqual(Product.objects.count(),10)

    @patch('catalogue.management.commands.database_import_off.Command.get_biggest_categories')
    @patch('catalogue.management.commands.database_import_off.Command.get_product_from_category')
    @patch('catalogue.management.commands.database_import_off.Command.insert_product')
    def test_handle(self, mock_insert, mock_get_products, mock_get_categories):
        mock_get_categories.return_value = ['Produits à tartiner']
        command = Command()
        handle = command.handle()
        mock_get_categories.assert_called_once()
        mock_get_products.assert_called_with('Produits à tartiner')
        mock_insert.assert_called_once()
