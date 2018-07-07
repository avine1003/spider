import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# browser = webdriver.Chrome('./chromedriver.exe')
from selenium.webdriver.common.keys import Keys
browser = webdriver.Ie()

open_url = 'https://www.baidu.com'
# 打开百度
browser.get(open_url)
time.sleep(2)
# 鼠标悬停 设置
browser.maximize_window()
a1 = browser.find_element_by_xpath('//*[@id="u1"]/a[8]')
ActionChains(browser).move_to_element(a1).perform()
time.sleep(2)
# 点击搜索设置
browser.find_element_by_xpath('//*[@id="wrapper"]/div[6]/a[1]').click()
time.sleep(1)
# 进行设置
browser.find_element_by_xpath('//*[@id="nr"]').click()
time.sleep(1)

browser.find_element_by_xpath('//*[@id="nr"]/option[2]').click()
time.sleep(1)
# 保存设置
browser.find_element_by_xpath('//*[@id="gxszButton"]/a[1]').click()
time.sleep(1)
# 点击弹框
box = browser.switch_to.alert.accept()
time.sleep(1)
# 输入关键词
a1 = browser.find_element_by_xpath('//*[@id="kw"]')
a1.send_keys('我的英雄学院')
a1.send_keys(Keys.RETURN)
time.sleep(2)
# 点击搜索
browser.find_element_by_xpath('//*[@id="su"]').click()
time.sleep(1)
# 跳转百度图片
browser.find_element_by_xpath('//*[@id="s_tab"]/a[5]').click()
time.sleep(2)
# 关闭网页
browser.close()