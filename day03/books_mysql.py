# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/6 15:31"

import requests
from bs4 import BeautifulSoup as BSp
import pymysql


# 用来操作数据库的类
class MysqlCommand:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'
        self.db = 'books'  # 库

    # 连接数据库
    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        passwd=self.password,
                                        db=self.db,
                                        charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql fail.')

    # 插入数据，插入之前先查询是否存在，如果存在就不再插入
    def insert_data(self, my_dict):
        cols = ', '.join(list(my_dict.keys()))
        values = '"," '.join(list(my_dict.values()))
        sql = "INSERT INTO book_list (%s) VALUES (%s)" % (cols, '"' + values + '"')
        try:
            result = self.cursor.execute(sql)
            self.conn.commit()
            if result:
                print('插入成功')
        except:
            self.conn.rollback()

    def close_mysql(self):
        self.cursor.close()
        self.conn.close()


def get_soup(url):
    try:
        response = requests.get(url)
        html_doc = response.text
        soup = BSp(html_doc, 'lxml')
        return soup
    except:
        pass


def get_art_info(soup):
    art_list = soup.select('.product_pod')
    mysql_command = MysqlCommand()
    mysql_command.connect()
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
        # print(list(art_dict.keys()))
        mysql_command.insert_data(art_dict)
    mysql_command.close_mysql()


# 获取所有页码链接
def get_url_list(pages):
    url_list = []
    for page in range(1, pages + 1):
        url = 'http://books.toscrape.com/catalogue/page-' + str(page) + '.html'
        url_list.append(url)
    return url_list


def main():
    for url in get_url_list(50):
        soup = get_soup(url)
        get_art_info(soup)
        print('写入url: %s' % url)
    print('保存完毕')


if __name__ == '__main__':
    main()
