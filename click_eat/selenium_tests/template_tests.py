from django.test import TestCase
from restaurants.views import *

class TemplateTest(TestCase):
    def test_restaurants_template(self):
        response = self.client.get('/restaurants/')
        self.assertTemplateUsed(response, 'search.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'pagination.html')

    def test_categories_template(self):
        response = self.client.get('/restaurants/categories/')
        self.assertTemplateUsed(response, 'categories.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'pagination.html')

    def test_results_template(self):
        response = self.client.get('/restaurants/results/')
        self.assertTemplateUsed(response, 'search.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'pagination.html')

    def test_new_restaurant_template(self):
        response = self.client.get('/restaurants/new_restaurant/')
        self.assertTemplateUsed(response, 'new_restaurant.html')
        self.assertTemplateUsed(response, 'base.html')
