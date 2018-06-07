# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/7 10:02"


import requests
from lxml import etree
from mysql_helper import Book, create_session, add_records

DOMAIN = "http://books.toscrape.com"

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


if __name__ == '__main__':
    session = create_session()
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    fetch_books(session, url)



