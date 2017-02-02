# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException

from helpers import *


class OauthVerifier(unittest.TestCase):

    def test_oauth(self):
        xml_vars = parse("vars.xml")
        tw_login_url = 'https://twitter.com/login'
        tw_token_url = 'https://api.twitter.com/oauth/authenticate?oauth_token='
        tw_otoken = create_tw_token()

        self.driver = webdriver.Firefox()
        driver = self.driver
        driver.get(tw_login_url)

        fields = driver.find_element_by_class_name('signin-wrapper').find_element_by_class_name('t1-form').\
            find_elements_by_class_name('clearfix')

        print 'entering login'
        fields[0].find_element_by_class_name('email-input').send_keys('lobanov_autotest@rambler.ru')
        print 'entering password'
        fields[1].find_element_by_class_name('js-password-field').send_keys('qweasd123')
        print 'pressing login button'
        fields[2].find_element_by_class_name('primary-btn').click()
        print 'TWITTER LOGIN SUCCESSFUL'

        print 'trying that url'

        driver.get(tw_token_url + tw_otoken)

        # ДОБАВИТЬ ПРОВЕРКУ НА НАЛИЧИЕ КНОПКИ, ЕСЛИ НЕТ, СРАЗУ ДЕРБАНИТЬ УРЛ
        # ТЕПЕРЬ 

        try:
            driver.find_element_by_id('allow')
            auth_btn.click()
        except NoSuchElementException:
            pass

        # auth_btn = driver.find_element_by_id('allow')
        # auth_btn.click()

        # print 'catching js alert'
        try:
            driver.switch_to_alert().accept()
        except NoAlertPresentException:
            print("no alert, but whatever")

        cur_url = driver.current_url.encode('utf-8')
        cur_url = cur_url.rsplit('=')
        
        oauth_token = cur_url[2].rsplit('&')[0]
        oauth_verifier = cur_url[-1]
        # print 'verifier token = ', oauth_verifier

        # write token to xml
        print 'writing oauth token'
        write_to_xml('tw_oauth_token', oauth_token)
        print 'successful\n'
        print 'writing oauth verifier'
        write_to_xml('tw_oauth_verifier', oauth_verifier)
        print 'successful'

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
