# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/7/6 19:22"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
assert '百度' in driver.title

elem = driver.find_element_by_name('wd')
elem.clear()
elem.send_keys('python')
elem.send_keys(Keys.RETURN)
# RETURN 和 enter 类似 匹配语义使用
assert 'No results found' not in driver.page_source
driver.close()