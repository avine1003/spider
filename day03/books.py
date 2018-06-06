# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/6 15:31"

import requests
from bs4 import BeautifulSoup as BSp
import json


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
        art_dict['img'] = img_link
        art_dict['star'] = star
        art_dict['title'] = title
        art_dict['price'] = price
        art_li.append(art_dict)
    data = json.dumps(art_li)
    return data


def write_data(data):
    # 爬取数据保存到文件
    with open('books.txt', 'a', encoding='utf-8') as f:
        f.write(data)


# 获取所有页码链接
def get_url_list(pages):
    url_list = []
    for page in range(1, pages + 1):
        url = 'http://books.toscrape.com/catalogue/page-' + str(page) + '.html'
        url_list.append(url)
    return url_list


def main():
    for url in get_url_list(2):
        soup = get_soup(url)
        data = get_art_info(soup)
        write_data(data)
        print('写入url: %s' % url)
    print('保存完毕')


if __name__ == '__main__':
    main()
