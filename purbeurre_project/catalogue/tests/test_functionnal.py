"""Functionnal test with Selenium for the catalogue application"""
import os
import time

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from catalogue.models import Product, Category, FavoriteProduct
from config import ROOT_DIR

class ResultsSubstituteSeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'AugusteGusteau',
            email = 'auguste.gusteau@bocuse.com',
            password = 'EcSofFRie!',
        )

        self.category1 = Category.objects.create(name='Produits à tartiner')
        self.category2 = Category.objects.create(name='Petit-déjeuners')
        self.category3 = Category.objects.create(name='Produits à tartiner sucrés')
        self.product1 = Product.objects.create(
            product_name='Nutella',
            generic_name='NUTELLA',
            code_prod='3017620422003',
            brand_name='Ferrero, Nutella',
            url='https://fr.openfoodfacts.org/produit/3017620422003/nutella-ferrero',
            nova_gps='4',
            nutri_grades='e',
            pnns_gps1='Sugary snacks',
            pnns_gps2='Sweets',
            store_name='Bi1, Magasins U',
            picture='https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.205.400.jpg',
            fat_100g='30.9',
            saturated_fat_100g='10.6',
            salt_100g='0.107',
            sugars_100g='56.4'
        )

        self.product2 = Product.objects.create(
            product_name='Nocciolata',
            generic_name='Pâte à tartiner au cacao et noisettes biologique',
            code_prod='8001505005707',
            brand_name='Rigoni di Asiago',
            url='https://fr.openfoodfacts.org/produit/8001505005707/nocciolata-rigoni-di-asiago',
            nova_gps='4',
            nutri_grades='d',
            pnns_gps1='Sugary snacks',
            pnns_gps2='Sweets',
            store_name="L'Ethique Verte,Magasins U,Monoprix,carrefour,Cora,Delhaize,Auchan",
            picture='https://static.openfoodfacts.org/images/products/800/150/500/5707/front_fr.128.400.jpg',
            fat_100g='32.0',
            saturated_fat_100g='5.7',
            salt_100g='0.12',
            sugars_100g='51.0'
        )

        self.category1.products.add(self.product1)
        self.category1.products.add(self.product2)
        self.category2.products.add(self.product1)
        self.category2.products.add(self.product2)
        self.category3.products.add(self.product1)
        self.category3.products.add(self.product2)
        self.driver = webdriver.Firefox(executable_path=os.path.join(ROOT_DIR, 'geckodriver.exe'))
        # Open the navigator with the server adress
        self.driver.get(self.live_server_url)

    def tearDown(self):
        self.driver.quit()

    def test_user_research_product_good_url(self):
        query='nutella'
        search = self.driver.find_element_by_id('searchForm')
        submit_search = self.driver.find_element_by_id('submit')
        search.send_keys(query)
        time.sleep(5)
        self.driver.implicitly_wait(5)
        submit_search.click()
        time.sleep(10)
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('catalogue:results_substitute') + '?query=' + query)

    def test_user_research_product_find_substitute(self):
        query='nutella'
        search = self.driver.find_element_by_id('searchForm')
        submit_search = self.driver.find_element_by_id('submit')
        search.send_keys(query)
        # time.sleep(5)
        self.driver.implicitly_wait(5)
        submit_search.click()
        section = self.driver.find_element_by_class_name('page-section')
        div = section.find_element_by_class_name('row')
        self.assertEqual(
            div.find_element_by_tag_name('h1').text,
            'Vous pouvez remplacer cet aliment par:'
        )

    def test_user_research_product_find_no_substitute(self):
        query='chips'
        search = self.driver.find_element_by_id('searchForm')
        submit_search = self.driver.find_element_by_id('submit')
        search.send_keys(query)
        time.sleep(5)
        self.driver.implicitly_wait(5)
        submit_search.click()
        section = self.driver.find_element_by_class_name('box_wrap')
        div = section.find_element_by_class_name('row')
        self.assertEqual(
            div.find_element_by_tag_name('h2').text,
            "Désolé, nous n'avons trouvé aucun produit !"
        )

    def test_user_research_product_and_look_detail_of_substitute(self):
        query='nutella'
        search = self.driver.find_element_by_id('searchForm')
        submit_search = self.driver.find_element_by_id('submit')
        search.send_keys(query)
        time.sleep(5)
        self.driver.implicitly_wait(5)
        submit_search.click()
        time.sleep(5)
        self.driver.implicitly_wait(5)
        substitute = self.driver.find_element_by_css_selector("a.btn-info")
        substitute.click()
        time.sleep(5)
        header = self.driver.find_element_by_class_name('masthead_substitute')
        header.find_element_by_class_name('container')
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('catalogue:details_substitute',args=[self.product2.id]))

    def test_user_no_logged_in_add_substitute_to_favorite(self):
        query='nutella'
        search = self.driver.find_element_by_id('searchForm')
        submit_search = self.driver.find_element_by_id('submit')
        search.send_keys(query)
        time.sleep(5)
        self.driver.implicitly_wait(5)
        submit_search.click()
        time.sleep(5)
        self.driver.implicitly_wait(5)
        substitute = self.driver.find_element_by_css_selector("button.btn-outline-info")
        substitute.click()
        time.sleep(5)
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + reverse('user:login') + '?next=' + reverse('catalogue:save_substitute')
        )


    def test_user_logged_in_add_substitute_to_favorite(self):
        search_login = self.driver.find_element_by_class_name('navbar-nav')
        icon = search_login.find_element_by_id('login_link')
        icon.click()
        self.driver.find_element_by_name('username').send_keys(self.user.username)
        self.driver.find_element_by_name('password').send_keys('EcSofFRie!')
        time.sleep(5)
        self.driver.find_element_by_class_name('btn-auth').click()
        time.sleep(5)
        query='nutella'
        search = self.driver.find_element_by_id('searchForm')
        submit_search = self.driver.find_element_by_id('submit')
        search.send_keys(query)
        submit_search.click()
        time.sleep(5)
        self.driver.implicitly_wait(5)
        substitute = self.driver.find_element_by_css_selector("button.btn-outline-info")
        substitute.click()
        alert = self.driver.find_element_by_class_name('alert')
        self.assertEqual(alert.text, "Le substitut a bien été enregistré dans vos favoris !")
        self.assertEqual(FavoriteProduct.objects.count(), 1)
        favorite_product = FavoriteProduct.objects.first().substitute.product_name
        self.assertEqual(favorite_product, self.product2.product_name)
