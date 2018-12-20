from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AccountTestCase(LiveServerTestCase):
    def setUp(self):
        #self.selenium = webdriver.Firefox()
        self.selenium = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        self.selenium.set_window_size(1920, 1080)
        size = self.selenium.get_window_size()
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

        username.send_keys('testuser')
        password.send_keys('Lemur123')

        submit.click()
