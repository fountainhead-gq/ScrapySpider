# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
import random
import os


class Proxies(object):
    def __init__(self, page=3):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies_nt()
        self.get_proxies_nn()
        self.get_proxies_wn()
        self.get_proxies_wt()

    # 免费国内普通代理IP
    def get_proxies_nt(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                self.proxies.append(':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    # 免费国内高匿代理IP
    def get_proxies_nn(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                self.proxies.append(':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    # 免费国外高匿代理IP
    def get_proxies_wn(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/wn/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                self.proxies.append(':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    # 免费国外普通代理IP
    def get_proxies_wt(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/wt/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                self.proxies.append(':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def verify_proxies(self):
        old_queue = Queue()   # 没验证的代理
        new_queue = Queue()  # 验证后的代理
        print('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0:
                break
            proxies = {'http': proxy}
            headers = {
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8'
            }
            try:
                requests.get('http://www.baidu.com', headers=headers,proxies=proxies, timeout=5)

                # 代理IP写入文本
                proxy_dir = os.getcwd()
                proxy_dir = os.path.join(proxy_dir, 'proxy.txt')
                with open(proxy_dir, 'a') as f:
                    if proxy !=0:
                        f.write(proxy + '\n')

                print('success %s' % proxy)
                new_queue.put(proxy)
            except:
                print('fail %s' % proxy)


if __name__ == '__main__':
    a = Proxies(10)  # 设置爬去代理的页数
    a.verify_proxies()
    proxies = a.proxies
