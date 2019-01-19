from django.urls import resolve
from django.test import LiveServerTestCase
from selenium import webdriver
from restaurants.views import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class RestaurantsTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(RestaurantsTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(RestaurantsTestCase, self).tearDown()

    def log_in(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/accounts/login/')

        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath("//input[@value='Login']")

        username.send_keys('kamila')
        password.send_keys('Lemur123')

        submit.click()

    def test_add_new_restaurant(self):
        self.log_in()
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants/new_restaurant')

        restaurants= selenium.find_element_by_id('id_name')
        category = selenium.find_element_by_xpath("//label[@for='ramen']")
        opening_hours= selenium.find_element_by_id('id_opening_hours')
        closing_hours= selenium.find_element_by_id('id_closing_hours')
        price_dropdown_list = Select(selenium.find_element_by_id('id_price'))
        address= selenium.find_element_by_id('id_address')
        save = selenium.find_element_by_name('button')

        restaurants.send_keys('Ramen People')
        opening_hours.send_keys('12:00')
        closing_hours.send_keys('21:00')
        price_dropdown_list.select_by_visible_text('przystępnie')
        address.send_keys('Czysta 8')
        category.click()

        save.click()
        self.assertTrue('new restaurant was added' in selenium.page_source)

    def test_choose_restaurant_from_list(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        restaurant = selenium.find_element_by_link_text('Farina')
        restaurant.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/farina/')

    def test_choose_category_from_list(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        category = selenium.find_element_by_link_text('| polska |')
        category.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/category_detail/polska/')

    def test_search_restaurant(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        restaurants= selenium.find_element_by_name('q')
        search = selenium.find_element_by_xpath("//button[@type='submit']")

        restaurants.send_keys('Restauracja Boscaiola')
        search.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/results/?q=Restauracja+Boscaiola')

        restaurant=selenium.find_element_by_link_text('Restauracja Boscaiola')
        restaurant.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/restauracja-boscaiola/')

    def test_go_to_home(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        home = selenium.find_element_by_css_selector('img.d-inline-block.align-top')
        home.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')

    def test_go_to_next_page(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        page = selenium.find_element_by_link_text('Next')
        page.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/?page=2')

    def test_go_to_page_by_number(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants')

        page = selenium.find_element_by_link_text('2')
        page.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/?page=2')

    def test_go_to_previous_page(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/restaurants/?page=2')

        page = selenium.find_element_by_link_text('Previous')
        page.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/?page=1')

    def test_add_rating(self):
        selenium = self.selenium
        self.log_in()
        selenium.get('http://127.0.0.1:8000/restaurants/farina/')

        rate_dropdown_list = Select(selenium.find_element_by_name('rating'))
        addrating = selenium.find_element_by_name('addRating')

        rate_dropdown_list.select_by_visible_text('1')
        addrating.click()

        self.assertTrue('rating: 1' in selenium.page_source)

    def test_add_to_favourite(self):
        selenium = self.selenium
        self.log_in()
        selenium.get('http://127.0.0.1:8000/restaurants/farina/')

        fav = selenium.find_element_by_name('add_fav')
        fav.click()

        selenium.get('http://127.0.0.1:8000/accounts/profile/')
        self.assertTrue('Farina' in selenium.page_source)

    def test_delete_from_favourite(self):
        selenium = self.selenium
        self.log_in()
        selenium.get('http://127.0.0.1:8000/restaurants/farina/')

        fav = selenium.find_element_by_name('del_fav')
        fav.click()

        selenium.get('http://127.0.0.1:8000/accounts/profile/')
        self.assertFalse('Farina' in selenium.page_source)

    def test_add_comment(self):
        selenium = self.selenium
        self.log_in()
        selenium.get('http://127.0.0.1:8000/restaurants/farina/')

        title = selenium.find_element_by_name('title')
        comment = selenium.find_element_by_name('body')
        add = selenium.find_element_by_name('addComm')

        title.clear()
        comment.clear()
        title.send_keys('Super')
        comment.send_keys('Bardzo nam się podobało.')
        add.click()

        self.assertTrue('kamila' in selenium.page_source)
        self.assertTrue('Super' in selenium.page_source)
        self.assertTrue('Bardzo nam się podobało.' in selenium.page_source)

    def test_add_positive_info_rating(self):
        selenium = self.selenium
        self.log_in()
        selenium.get('http://127.0.0.1:8000/restaurants/farina/')

        rate=selenium.find_element_by_name('positiveRating')
        rate.click()

        self.assertTrue("info rating : 1" in selenium.page_source)

    def test_add_negative_info_rating(self):
        selenium = self.selenium
        self.log_in()
        selenium.get('http://127.0.0.1:8000/restaurants/farina/')

        rate=selenium.find_element_by_name('negativeRating')
        rate.click()

        self.assertTrue('info rating : -1' in selenium.page_source)

    def test_get_Category_Names_From_Restaurnt_Category(self):
        restaurant1 = Restaurant.objects.create(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        category1 = Category.objects.create(name="testkategoria", slug="kategoriaslug")
        restcategory = RestauratsCategory.objects.create(restaurant=restaurant1, category=category1)
        self.assertEqual(str(getCategoryNamesFromRestaurntCategory()),'[<Category: @testkategoria>]')

    def test_get_Category_Names(self):
        category1 = Category.objects.create(name="testkategoria", slug="kategoriaslug")
        category2 = Category.objects.create(name="testkategoria2", slug="kategoriaslug2")
        self.assertEqual(str(getCategoryNames()),"['testkategoria', 'testkategoria2']")

    def test_get_Category_Initials(self):
        restaurant1 = Restaurant.objects.create(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        category1 = Category.objects.create(name="testkategoria", slug="kategoriaslug")
        category2 = Category.objects.create(name="testkategoria2", slug="kategoriaslug2")
        category3 = Category.objects.create(name="testkategoria3", slug="kategoriaslug3")
        RestauratsCategory.objects.create(restaurant=restaurant1, category=category1)
        RestauratsCategory.objects.create(restaurant=restaurant1, category=category2)
        self.assertEqual(str(getCategoriesInitials(restaurant1)),"['testkategoria', 'testkategoria2']")
