# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/6 15:31"

import requests
from bs4 import BeautifulSoup as BSp
import json
from queue import Queue
import pymysql
from threading import Thread


def insert_data(my_dict):
    # 连接数据库
    db_conn = pymysql.connect(host='localhost',
                              port=3306,
                              user='root',
                              passwd='123456',
                              db='books',
                              charset='utf8', )
    # 创建游标
    cursor = db_conn.cursor()
    cols = ', '.join(list(my_dict.keys()))
    values = '"," '.join(list(my_dict.values()))
    sql = "INSERT INTO book_list (%s) VALUES (%s)" % (cols, '"' + values + '"')
    try:
        result = cursor.execute(sql)
        db_conn.commit()
        if result:
            print('插入成功')
    except:
        db_conn.rollback()
    # cursor.close()
    db_conn.close()


class BookSpider(Thread):
    def __init__(self, url, q):
        super().__init__()
        self.url = url
        self.q = q

    def run(self):
        soup = self.get_soup(self.url)
        data = self.get_art_info(soup)
        self.write_data(data)

    def get_soup(self, url):
        try:
            response = requests.get(url)
            html_doc = response.text
            soup = BSp(html_doc, 'lxml')
            return soup
        except:
            pass

    def get_art_info(self, soup):
        art_list = soup.select('.product_pod')
        art_li = []
        for art in art_list:
            art_dict = {}
            img = art.select('.image_container img')[0]['src']
            # 书籍图片地址
            img_link = 'http://books.toscrape.com' + img[2:]
            # 书籍星级
            star = art.select('p')[0]['class'][1]
            # 书籍名称
            title = art.select('h3 a')[0]['title']
            # 价格
            price = art.select('.price_color')[0].text
            art_dict['img_link'] = img_link
            art_dict['star'] = star
            art_dict['title'] = title
            art_dict['price'] = price
            art_li.append(art_dict)
            insert_data(art_dict)
            self.q.put('图片地址:%s, 星级:%s, 书名:%s, 价格:%s' % (img_link, star, title, price))
        data = json.dumps(art_li)
        return data

    def write_data(self, data):
        # 爬取数据保存到文件
        with open('books.txt', 'a', encoding='utf-8') as f:
            f.write(data)


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


def main():
    # 创建一个队列来保存获取的数据
    q = Queue()
    # 获取所有url
    url_list = get_url_list()
    # 保存线程
    thread_list = []

    # 创建并启动线程
    for url in url_list:
        thread = BookSpider(url, q)
        thread.start()
        thread_list.append(thread)

    # 让主进程等待子进程执行完毕
    for i in thread_list:
        i.join()

    while not q.empty():
        print(q.get())


if __name__ == '__main__':
    main()
