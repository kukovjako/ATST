# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException

from helpers import *


class GetVKCode(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_get_oauth(self):
        vk_login = from_xml('vk_login')
        vk_pass = from_xml('vk_pass')
        vk_login_url = 'https://oauth.vk.com/authorize?client_id=3210582&display=page&redirect_uri=https%3A%2F%2Fid.rambler.ru%2Foauth-20%2F%3Fprovider%3Dvkontakte&response_type=code&v=5.62&state=123456'

        driver = self.driver
        driver.get(vk_login_url)
        #time.sleep(10)
        login_field = driver.find_element_by_xpath('//input[@name="email"]')
        login_field.send_keys(vk_login)

        password_field = driver.find_element_by_xpath('//input[@name="pass"]')
        password_field.send_keys(vk_pass)
        # time.sleep(1000)

        button = driver.find_element_by_xpath('//button[@type="submit"]')
        button.click()

        try:
            driver.find_element_by_xpath('//button[@class="flat_button fl_r button_indent"]').click()
        except NoSuchElementException:
            pass

        try:
            driver.switch_to_alert().accept()
        except NoAlertPresentException:
            pass
            # print("no alert, but whatever")
        cur_url = driver.current_url.encode('utf-8')
        cur_url = cur_url.rsplit('&')
        for a in cur_url:
            if 'code=' in a:
                code = a[5:]
                print code

        try:
            assert code, 'No code received from VK'
        except UnboundLocalError:
            raise AssertionError, 'No code received from VK'

        write_to_xml('vk_code', code)


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
