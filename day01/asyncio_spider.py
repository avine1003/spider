# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/4 15:59"

import requests
from bs4 import BeautifulSoup as BS4
import asyncio
import os


link_set = set()


def download(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # write_file(file, filename, r)
    return r


def write_file(file, filename, r):
    html_doc = r.text
    if not os.path.exists(file):
        os.mkdir(file)
    with open('%s/_%s.html' % (file, filename), 'w', encoding='gb18030') as f:
        f.write(html_doc)


def parse(response):
    base_domain = response.url
    r = response.content
    soup = BS4(r, 'lxml')
    li_list = soup.select('#p_left ul')[0].find_all('li')
    # for li in li_list:
    #     li_tag = li.a.text
    #     content = li.p.text
    a_list = soup.select('#p_left ul')[1].find_all('a')
    page_format = a_list[-1]['href'][:-5].split('_')
    page_last, page_sec = page_format[-1], page_format[1]
    for i in range(1, int(page_last) + 1):
        link = base_domain + 'list_' + page_sec + '_' + str(i) + '.html'
        link_set.add(link)
        parse_set(link_set)


def parse_set(link_set):
    index = 0
    for link in link_set:
        r = requests.get(link)
        r.encoding = r.apparent_encoding
        index += 1
        file = link.split('/')[-2]
        print('开始下载%s' % link)
        write_file(file, index, r)
        print("index: %s, link: %s 下载完毕" % (index, link))


async def main1():
    base_url = url_list[0]
    response = download(base_url)
    parse(response)


async def main2():
    base_url = url_list[1]
    response = download(base_url)
    parse(response)


async def main3():
    base_url = url_list[2]
    response = download(base_url)
    parse(response)


async def main4():
    base_url = url_list[3]
    response = download(base_url)
    parse(response)


async def main5():
    base_url = url_list[4]
    response = download(base_url)
    parse(response)


async def main6():
    base_url = url_list[5]
    response = download(base_url)
    parse(response)


async def main7():
    base_url = url_list[6]
    response = download(base_url)
    parse(response)


if __name__ == '__main__':
    url_list = ['https://www.geyanw.com/mingyanjingju/',
                'https://www.geyanw.com/renshenggeyan/',
                'https://www.geyanw.com/html/dushumingyan/',
                'https://www.geyanw.com/html/jingdianduanju/',
                'https://www.geyanw.com/html/aiqingmingyan/',
                'https://www.geyanw.com/html/jingdianmingyan/',
                'https://www.geyanw.com/html/mingrenmingyan/',
                ]
    loop = asyncio.get_event_loop()
    tasks = [main1(), main2(), main3(), main4(), main5(), main6(), main7()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
