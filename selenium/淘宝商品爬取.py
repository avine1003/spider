from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait

from pyquery import PyQuery as pd
import pymongo

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KEYWORD = 'iPhone'

def index_page(page):
    '''
    爬取索引页
    '''
    print('正在爬取第{}页'.format(page))
    try:
        url = 'https://s.taobao.com/search?q=' + KEYWORD
        browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager  li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    '''
    提取商品数据
    '''
    html = browser.page_source
    doc = pd(html)
    items = doc('#mainsrp-itemlist .items .item').items()

    for item in items:
        product = {
        'imgae': item.find('.pic .img').attr('data-src'),
        'price': item.find('.price').text(),
        'deal': item.find('.deal-cnt').text(),
        'title': item.find('.shop').text(),
        'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


MONGO_URI = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]


def save_to_mongo(result):
    '''
    保存到数据库
    '''
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储成功')
    except:
        print('存储失败')


MAX_PAGE = 100

def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == '__main__':
    main()