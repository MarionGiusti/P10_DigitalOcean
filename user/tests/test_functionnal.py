# """Functionnal test with Selenium for the catalogue application"""
import os
import time

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

from user.models import Profile

from purbeurre_project.settings.defaults import BASE_DIR

class ProfileSeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'AugusteGusteau',
            email = 'auguste.gusteau@bocuse.com',
            password = 'EcSofFRie!',
        )
        self.profile = Profile.objects.create(user=self.user, profile_pic='auguste.png')

        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=fireFoxOptions)
        self.driver.get(self.live_server_url)
    
    def tearDown(self):
        self.driver.quit()

    def test_user_logged_in(self):
        self.driver.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('AugusteGusteau')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('EcSofFRie!')
        self.driver.find_element_by_class_name("btn-auth").click()
        time.sleep(2)

        self.assertEqual(
            self.driver.find_element_by_id("account-link").text,
            'Mon compte'
        )

    def test_user_account_access_profile_info_correct(self):
        self.driver.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('AugusteGusteau')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('EcSofFRie!')
        self.driver.find_element_by_class_name("btn-auth").click()
        time.sleep(2)
        account_link = self.driver.find_element_by_id("account-link")
        account_link.click()
        username_profile = self.driver.find_element_by_id('id_username').get_attribute('value')
        email_profile = self.driver.find_element_by_id('id_email').get_attribute('value')
        div_pic = self.driver.find_element_by_id('div_id_profile_pic')
        pic_profile = div_pic.find_element_by_tag_name('a').text
        time.sleep(3)
        self.assertEqual(username_profile , 'AugusteGusteau')
        self.assertEqual(email_profile , 'auguste.gusteau@bocuse.com')
        self.assertEqual(pic_profile ,'auguste.png')

    def test_div_profile_picture_correct(self):
        self.driver.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('AugusteGusteau')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('EcSofFRie!')
        self.driver.find_element_by_class_name("btn-auth").click()
        time.sleep(2)
        account_link = self.driver.find_element_by_id("account-link")
        nav_src_profile_pic = account_link.find_element_by_tag_name('img').get_attribute('src')
        account_link.click()
        time.sleep(3)
        src_profile_pic = self.driver.find_element_by_class_name("profile_pic_circle").get_attribute('src')
        self.assertEqual(src_profile_pic , self.live_server_url + '/media/auguste.png')
        self.assertEqual(nav_src_profile_pic , self.live_server_url + '/media/auguste.png')

    def test_user_account_change_profile(self):
        self.driver.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('AugusteGusteau')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('EcSofFRie!')
        self.driver.find_element_by_class_name("btn-auth").click()
        time.sleep(2)
        account_link = lambda : self.driver.find_element_by_id("account-link")

        account_link().click()
        username_profile = self.driver.find_element_by_id('id_username')
        username_profile.clear()
        username_profile.send_keys('Auguste_Gusteau')
        email_profile = self.driver.find_element_by_id('id_email')
        email_profile.clear()
        email_profile.send_keys('auguste_gusteau@bocuse.com')
        div_pic = self.driver.find_element_by_id('id_profile_pic')
        div_pic.send_keys(str(BASE_DIR / 'mediafiles/profile.png'))
        self.driver.find_element_by_class_name("btn-primary").click()
        time.sleep(10)

        new_username_profile = self.driver.find_element_by_tag_name('header h2').text
        new_email_profile = self.driver.find_element_by_tag_name('section div h3 span').text
        new_src_profile_pic = self.driver.find_element_by_class_name('profile_pic_circle').get_attribute('src')
        new_profile_pic = Profile.objects.filter(user__username='Auguste_Gusteau').get()
        nav_src_profile_pic = account_link().find_element_by_tag_name('img')
        new_nav_src_profile_pic = nav_src_profile_pic.get_attribute('src')
        self.assertEqual(new_username_profile , 'Auguste_Gusteau !')
        self.assertEqual(new_email_profile , 'auguste_gusteau@bocuse.com')
        self.assertEqual(new_src_profile_pic , self.live_server_url + '/media/' + str(new_profile_pic.profile_pic))
        self.assertEqual(new_nav_src_profile_pic , self.live_server_url + '/media/' + str(new_profile_pic.profile_pic))
