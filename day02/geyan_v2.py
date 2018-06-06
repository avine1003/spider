# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/5 10:56"

from bs4 import BeautifulSoup as BSP4
import requests
import os

URL_LIST = [
    ('https://www.geyanw.com/lizhimingyan/list_33_1.html', '励志名言', 'lizhimingyan'),
    ('https://www.geyanw.com/renshenggeyan/list_32_1.html', '人生格言', 'renshenggeyan'),
    ('https://www.geyanw.com/mingyanjingju/list_37_1.html', '名言警句', 'mingyanjingju'),
    ('https://www.geyanw.com/html/mingrenmingyan/list_1_1.html', '名人名言', 'mingrenmingyan'),
    ('https://www.geyanw.com/html/dushumingyan/list_5_1.html', '读书名言', 'dushumingyan'),
    ('https://www.geyanw.com/html/jingdianmingyan/list_2_1.html', '经典名言', 'jingdianmingyan'),
    ('https://www.geyanw.com/html/aiqingmingyan/list_3_1.html', '爱情名言', 'aiqingmingyan'),
    ('https://www.geyanw.com/html/jingdianduanju/list_9_1.html', '经典短句', 'jingdianduanju'),
    ('https://www.geyanw.com/html/renshenggeyan/list_4_1.html', '人生格言2', 'renshenggeyan2'),
]
g_set = set()

def store_file(file, filename, response):
    html_doc = response.text
    if not os.path.exists(file):
        os.mkdir(file)
    with open('%s/geyan_%s.html' % (file, filename), 'w', encoding='utf-8') as f:
        f.write(html_doc)


def download(url, file, filename='index', store_flag=True):
    '''
    :param url: 待爬取的url
    :param filename:  待存储html文件名称
    :param store_flag:  本地持久化标志
    :return:
    '''
    response = requests.get(url)
    if store_flag:
        store_file(file, filename, response)
    return response


def parse(response, type):
    url = response.url
    base_urls = url.split('/list_')
    domain = base_urls[0]
    init_html = base_urls[-1]
    ctype = init_html.split('_')[0]
    cindex = init_html.split('_')[1].split('.')[0]
    g_set.add(url)

    html_doc = response.content
    soup = BSP4(html_doc, 'lxml')
    page_list = soup.select('.pagelist li a')
    total_num = soup.select('.pagelist .pageinfo strong')[0].text
    page_max = int(total_num)
    [parse_page(type, page, ctype, '%s/list_%s_%s.html' %(domain, ctype, page)) for page in range(2, page_max+1)]


def parse_page(type, page, ctype, url):
    response = download(url, type, store_flag=False)
    html_doc = response.content
    soup = BSP4(html_doc, 'lxml')
    link_list = soup.select('#p_left h2 a')
    index = 1
    for link in link_list:
        url_link = 'https://www.geyanw.com' + link['href']
        print(url_link)
        if url_link not in g_set:
            index += 1
            response = download(url_link, type, filename='%s_%s.html'% (ctype, index), store_flag=True)


def process(entry_url, name, type):
    try:
        response = download(entry_url, type, store_flag=True)
        parse(response, type)
        return True
    except:
        return False

'''
采用多进程方式    RabbitMQ 
'''
def multprocess_run():
    from multiprocessing import Pool
    pool = Pool(processes=4)
    result = []
    for (entry_url, name, type) in URL_LIST:
        pc = pool.apply_async(process, args=(entry_url, name, type))
        result.append(pc)
    pool.close()
    pool.join()


'''
采用协程来处理并发量
'''
# import asyncio
#
# @asyncio.coroutine
# def async_io_loop(entry_url):
#     yield from process(entry_url)
#
#
# def async_run():
#     loop = asyncio.get_event_loop()
#     tasks = [async_io_loop(url) for (url, name, type) in URL_LIST]
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()


def main():
    # for (url, name, type) in URL_LIST:
    #     process(url, name, type)
    multprocess_run()
    # async_run()
    # [process(url, name, type) for (url, name, type) in URL_LIST]


if __name__ == '__main__':
    main()
