"""Unit test for the pages application"""
from django.test import SimpleTestCase
from django.urls import reverse

class PagesTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_home_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_home_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_mentions_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_mentions_url_by_name(self):
        response = self.client.get(reverse('mentions'))
        self.assertEqual(response.status_code, 200)

    def test_view_mentions_uses_correct_template(self):
        response = self.client.get(reverse('mentions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentions.html')
