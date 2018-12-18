from django.urls import resolve
from django.test import LiveServerTestCase
from selenium import webdriver
from restaurants.views import list_restaurants
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


class RestaurantsTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(RestaurantsTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(RestaurantsTestCase, self).tearDown()


    def test_root_url_resolves_to_restaurants_page_view(self):
        found = resolve('/restaurants/')
        self.assertEqual(found.func, list_restaurants)

    def test_uses_search_template(self):
        response = self.client.get('/restaurants/')
        self.assertTemplateUsed(response, 'search.html')

    def test_add_new_restaurant(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants/new_restaurant')

        restaurants= selenium.find_element_by_id('id_name')
        category_dropdown_list = Select(selenium.find_element_by_id('id_category'))
        save = selenium.find_element_by_name('button')

        restaurants.send_keys('lumo')
        category_dropdown_list.select_by_visible_text('@ciasta')

        save.click()

    def test_choose_restaurant_from_list(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        restaurant = selenium.find_element_by_link_text('Szwagra')
        restaurant.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/Szwagra/')

    def test_choose_category_from_list(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        restaurant = selenium.find_element_by_link_text('@kebab')
        restaurant.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/category_detail/kebab/')

    def test_search_restaurant(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        restaurants= selenium.find_element_by_name('q')
        search = selenium.find_element_by_xpath("//button[@type='submit']")

        restaurants.send_keys('szwagra')

        search.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/results/?q=szwagra')

    def test_go_to_home(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        logo = selenium.find_element_by_css_selector('img.d-inline-block.align-top')
        logo.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')

    def test_go_to_next_page(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        logo = selenium.find_element_by_link_text('Next')
        logo.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/?page=2')

    def test_go_to_page_by_number(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        logo = selenium.find_element_by_link_text('2')
        logo.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/?page=2')

    def test_go_to_previous_page(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants/?page=2')

        logo = selenium.find_element_by_link_text('Previous')
        logo.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/?page=1')
