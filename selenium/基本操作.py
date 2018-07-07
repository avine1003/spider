# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys 
# from selenium.webdriver.support import expected_conditions as EC 
# from selenium.webdriver.support.wait import WebDriverWait


# browser = webdriver.Chrome()
# try:
#     browser.get('http://www.baidu.com')
#     input = browser.find_element_by_id('kw')
#     input.send_keys('python')
#     input.send_keys(Keys.ENTER)
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
#     print(browser.current_url)
#     print(browser.get_cookies())
#     print(browser.page_source)

# except Exception as e:
#     raise
# else:
#     pass
# finally:
#     pass
#     
#     


# from selenium import webdriver
# import time

# browser = webdriver.Chrome()
# browser.get('http://www.taobao.com')
# input = browser.find_element_by_id('q')
# print(input.id)
# print(input.location)
# print(input.tag_name)
# print(input.size)

# input.send_keys('iphone')
# time.sleep(1)
# input.clear()
# input.send_keys('ipad')
# button = browser.find_element_by_class_name('btn-search')
# button.click()
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom")')
# 
# 


import time
from selenium import webdriver

browser = webdriver.Chrome()
# browser.get('http://www.taobao.com')
browser.get('http://www.baidu.com')
# browser.get('http://www.python.org')

# browser.back()
# time.sleep(1)
# browser.forward()
# browser.close()

# browser.get("http://www.zhihu.com/explore")
# print(browser.get_cookies())
# browser.add_cookie({'name':'hehe', 'value':'123'})
# print(browser.get_cookies())
# browser.delete_all_cookies()
# print(browser.get_cookies())
# 
# 
browser.execute_script('window.open()')
print(browser.window_handles)
browser.switch_to_window(browser.window_handles[1])
browser.get('http://www.taobao.com')
time.sleep(1)
browser.switch_to_window(browser.window_handles[0])
