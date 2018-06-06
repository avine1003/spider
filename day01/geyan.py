# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/4 15:59"

import requests
from bs4 import BeautifulSoup as BS4


def download(url, filename='index'):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    # r.encoding = 'utf-8'
    write_file(filename, r)
    return r


def write_file(filename, r):
    html_doc = r.text
    with open('geyan_%s.html' % filename, 'w', encoding='gb18030') as f:
        f.write(html_doc)


def parse_tbox(tbox, base_domain):
    tbox_tag = tbox.select('dt a')[0].text
    index = 0
    li_list = tbox.find_all('li')
    for li in li_list:
        link = base_domain[:-1] + li.a['href']
        print("index: %s, link: %s" % (index, link))
        index += 1
        if link not in g_set:
            g_set.add(link)
            filename = '%s_%s' % (tbox_tag, index)
            sub_html = download(link, filename)


def parse(response):
    global g_set
    g_set = set()
    base_domain = response.url
    g_set.add(base_domain)
    html_doc = response.content
    soup = BS4(html_doc, 'lxml')
    tbox_list = soup.select("#p_left dl.tbox")
    [parse_tbox(tbox, base_domain) for tbox in tbox_list]


def main():
    base_url = 'https://www.geyanw.com/'
    response = download(base_url)
    parse(response)


if __name__ == '__main__':
    main()
