from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AccountTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium

        selenium.get('http://127.0.0.1:8000/accounts/signup/')

        username = selenium.find_element_by_id('id_username')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_xpath("//input[@value='Sign Up']")

        username.send_keys('testuser')
        email.send_keys('test@test.com')
        password1.send_keys('Lemur123')
        password2.send_keys('Lemur123')

        submit.click()

    def test_login(self):
        selenium = self.selenium

        selenium.get('http://127.0.0.1:8000/accounts/login/')

        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath("//input[@value='Login']")

        username.send_keys('kamila')
        password.send_keys('Lemur123')

        submit.click()

    def test_log_out(self):
        selenium = self.selenium
        self.test_login()

        selenium.get('http://127.0.0.1:8000/')

        logout = selenium.find_element_by_link_text('Log out')
        logout.click()

        self.assertTrue(selenium.find_elements_by_link_text('Log in'))
        self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')

    def test_profile_template(self):
        response = self.client.get('/accounts/profile/')
        self.assertTemplateUsed(response, 'profile.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'pagination.html')

    def test_login_template(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_signup_template(self):
        response = self.client.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertTemplateUsed(response, 'base.html')
