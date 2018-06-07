# -*- coding: utf-8 -*-

__author__ = "wuyou"
__date__ = "2018/6/7 10:02"

import threading
from queue import Queue
import requests
from lxml import etree
from bs4 import BeautifulSoup as BSp
from mysql_helper import Book, create_session, add_records

DOMAIN = "http://books.toscrape.com"

'''
# 抓取数据
def fetch_books(session, url):
    r = requests.get(url)
    html_doc = r.text
    html_etree = etree.HTML(html_doc)
    book_articles = html_etree.xpath("//article[@class='product_pod']")
    for book in book_articles:
        book_title = book.xpath("./h3/a/@title")[0]
        image_url = book.xpath("./div[@class='image_container']/a/img/@src")[0]
        image_url = DOMAIN + image_url[2:]
        book_url = book.xpath("./div[@class='image_container']/a/@href")[0]
        book_url = DOMAIN + "/catalogue/" + book_url
        book_rate = book.xpath("./p/@class")[0]
        book_price = book.xpath("./div[@class='product_price']/p/text()")[0]
        # print(book_title, image_url, book_url, book_rate, book_price)
        book = Book(book_title=book_title, image_url=image_url,
                    book_url=book_url, book_rate=book_rate, book_price=book_price)
        add_records(session, book)
        print(f"save ok with {book_title}")
'''


'''
存储和爬取分离
'''
g_mutex = threading.Lock()  # 创建线程锁
g_queue_urls = Queue()  # 待爬取页面url队列
g_data_list = Queue()  # 待存储的队列
g_success_list = []  # 爬取成功的url列表
g_fail_list = []  # 爬取失败的url列表
session = create_session()


import os
spider_data_dir = "./data"   # 保存book详情页的文件夹
if not os.path.exists(spider_data_dir):
    os.mkdir(spider_data_dir)

imgs = "./imgs"   # 保存book图片的文件夹
if not os.path.exists(imgs):
    os.mkdir(imgs)

'''
负责下载的线程
'''
class CrawlerThread(threading.Thread):
    def __init__(self, url, store_flag=False):
        # 在init中要先初始化Thread，然后在给参数赋值, 否则 RuntimeError: thread.__init__() not called
        threading.Thread.__init__(self)
        self.__url = url
        self.__store_flag = store_flag
        self.start()

    def run(self):
        try:
            r = requests.get(self.__url)
            html = r.text
            import time
            filename = '%s/scrape_%s.html' % (spider_data_dir, int(time.time() * 1000))
            if not self.__store_flag:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(html)
            g_mutex.acquire()
            g_success_list.append(self.__url)
            g_mutex.release()
            return True
        except Exception as e:
            g_fail_list.append(self.__url)
            print(f"页面 {self.__url} 下载失败")
            return False


# 爬取
class Crawler:
    def __init__(self, name, thread_number):
        self.name = name
        self.thread_number = thread_number
        self.logfile = open("log.txt", 'a+', encoding='utf-8')
        self.thread_pool = []  # 线程池

    def __del__(self):
        for thread in self.thread_pool:
            thread.join()

    def logging(self, inp):
        self.logfile.write(inp + '\n')

    def __fetch_books(self, url):
        # r = requests.get(url)
        self.logging("fetch_url: " + url)
        r = self.downloader(url, mult_thread=False)
        html_doc = r.text
        html_etree = etree.HTML(html_doc)
        book_articles = html_etree.xpath("//article[@class='product_pod']")
        scrapy_book_urls = []  # 书籍详情页url
        for book in book_articles:
            book_title = book.xpath("./h3/a/@title")[0]
            image_url = book.xpath("./div[@class='image_container']/a/img/@src")[0]
            image_url = DOMAIN + image_url[2:]
            book_url = book.xpath("./div[@class='image_container']/a/@href")[0]
            book_url = DOMAIN + "/catalogue/" + book_url
            book_rate = book.xpath("./p/@class")[0]
            book_price = book.xpath("./div[@class='product_price']/p/text()")[0]
            book = Book(book_title=book_title, image_url=image_url,
                        book_url=book_url, book_rate=book_rate, book_price=book_price)
            g_mutex.acquire()
            g_data_list.put(book)
            scrapy_book_urls.append(book_url)
            # 保存图片到本地
            filename = book_title[:20] if len(book_title) > 20 else book_title
            with open("%s/%s.jpg" % (imgs, filename), 'wb+') as f:
                f.write(requests.get(image_url).content)
            g_mutex.release()
            self.logging("book_url: %s store ok" % book_url)
        return scrapy_book_urls

    def start(self, urls):
        global g_queue_urls
        [g_queue_urls.put(url) for url in urls]
        depth = 0  # 爬取深度
        print(f"爬虫 {self.name} 开始启动...")
        while g_queue_urls.qsize() > 0:
            depth += 1
            self.logging("获取队列url数据,进行爬取")
            url = g_queue_urls.get()
            print(f'当前爬取的深度是{depth}, url: {url}')
            scrapy_book_urls = self.__fetch_books(url)
            [self.downloader(book_url) for book_url in scrapy_book_urls]

    def downloader(self, url, mult_thread=True):
        '''
        :param url:  输入的待爬取的url
        :return:
        '''
        if mult_thread:
            crawler_thread = CrawlerThread(url)  # 创建下载线程
            self.thread_pool.append(crawler_thread)
        else:
            return requests.get(url)


# 获取所有页码链接
def get_url_list():
    base_url = 'http://books.toscrape.com/catalogue/page-1.html'
    r = requests.get(base_url)
    soup = BSp(r.text, 'lxml')
    content = soup.select('.current')[0].text
    pages = int(content.split()[-1])
    url_list = []
    for page in range(1, pages + 1):
        url = 'http://books.toscrape.com/catalogue/page-' + str(page) + '.html'
        url_list.append(url)
    return url_list


def store_data():
    while True:
        print("g_data_list queue size is" + str(g_data_list.qsize()))
        data_size = g_data_list.qsize()
        if data_size == 0:
            break
        book = g_data_list.get()
        add_records(session, book)


def spider(url_list):
    thread_number = 4  # 线程数
    scrape_name = "scrape"
    crawler = Crawler(scrape_name, thread_number)
    crawler.start(url_list)
    # index = 0
    # 还可将每个url开一个进程,单独处理
    # for url in URL_ENTRY_LIST:
    #     scrape_name = "scrape_%s" % index
    #     crawler = Crawler(scrape_name, thread_number)
    #     index += 1
    #     crawler.start(URL_ENTRY_LIST)

    # start new thread to pipeline
    pipeline = threading.Thread(target=store_data)
    pipeline.start()
    pipeline.join()


if __name__ == '__main__':
    url_list = get_url_list()
    # url_list = ["http://books.toscrape.com/catalogue/page-1.html",
    #             "http://books.toscrape.com/catalogue/page-2.html",]
    from multiprocessing import Process

    spider_ps = Process(target=spider, args=(url_list,))
    # pipeline_ps = Process(target=pipeline)

    spider_ps.start()
    # pipeline_ps.start()

    spider_ps.join()
    # pipeline_ps.join()

    spider_ps.terminate()

