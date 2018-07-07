# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/7/6 20:00"

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BaiduSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search(self):
        driver = self.driver
        driver.get('http://www.baidu.com')
        self.assertIn('百度', driver.title)
        elem = driver.find_element_by_name('wd')
        elem.send_keys('python')
        elem.send_keys(Keys.RETURN)
        assert 'No results found' not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
