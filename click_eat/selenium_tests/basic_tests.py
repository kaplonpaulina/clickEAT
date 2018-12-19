from django.test import TestCase
from selenium import webdriver

class BasicTestCase(TestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(BasicTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BasicTestCase, self).tearDown()

    def log_in(self):
        selenium = self.selenium

        selenium.get('http://127.0.0.1:8000/accounts/login/')

        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath("//input[@value='Login']")

        username.send_keys('testuser')
        password.send_keys('Lemur123')

        submit.click()

    def test_page_name(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        self.assertIn('ClickEat', selenium.title)


    def test_go_to_log_in(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        login = selenium.find_element_by_link_text('Log in')
        login.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/accounts/login/')

    def test_go_to_sign_up(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')

        signup = selenium.find_element_by_link_text('Sign up')
        signup.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/accounts/signup/')

    def test_go_to_log_out(self):
        selenium = self.selenium
        self.log_in()

        selenium.get('http://127.0.0.1:8000/')

        signup = selenium.find_element_by_link_text('Log out')
        signup.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')

    def test_go_to_profile(self):
        selenium = self.selenium
        self.log_in()

        selenium.get('http://127.0.0.1:8000/')

        signup = selenium.find_element_by_link_text('Profile')
        signup.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/accounts/profile/')

    def test_go_to_new_restaurant(self):
        selenium = self.selenium
        self.log_in()

        selenium.get('http://127.0.0.1:8000/')

        signup = selenium.find_element_by_link_text('Add new Restaurant')
        signup.click()

        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/restaurants/new_restaurant/')
