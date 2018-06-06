# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/4 15:59"

import requests
from bs4 import BeautifulSoup as BS4


def download(url, filename=''):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    write_file(filename, r)
    return r


def write_file(filename, r):
    html_doc = r.text
    with open('lizhi/_%s.html' % filename, 'w', encoding='gb18030') as f:
        f.write(html_doc)


link_set = set()
def parse(response):
    base_domain = response.url
    r = response.content
    soup = BS4(r, 'lxml')
    li_list = soup.select('#p_left ul')[0].find_all('li')
    for li in li_list:
        li_tag = li.a.text
        content = li.p.text
    a_list = soup.select('#p_left ul')[1].find_all('a')
    page_format = a_list[-1]['href'][:-5].split('_')
    page_last, page_sec = page_format[-1], page_format[1]
    for i in range(1, int(page_last) + 1):
        link = base_domain + 'list_' + page_sec + '_' + str(i) + '.html'
        link_set.add(link)
    [parse_set(link) for link in link_set]


def parse_set(link):
    index = 0
    for link in link_set:
        r = requests.get(link)
        r.encoding = r.apparent_encoding
        index += 1
        print('开始下载%s' % link)
        write_file(index, r)
        print("index: %s, link: %s 下载完毕" % (index, link))


def main():
    base_url = 'https://www.geyanw.com/lizhimingyan/'
    response = download(base_url)
    parse(response)


if __name__ == '__main__':
    main()
