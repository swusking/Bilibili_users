#!/usr/bin/env python
#coding:utf-8

import requests, re
from bs4 import BeautifulSoup as BS
from Queue import Queue
import threading, time


baiduHeader = {
    'Host': 'www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'BAIDUID=DBECB2238DC97D397D32A3F5925C7BE6:FG=1; BIDUPSID=DBECB2238DC97D397D32A3F5925C7BE6; PSTM=1493880881; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=0; H_PS_PSSID=1437_13549_21100_22159; BD_UPN=12314753'
}

def getProxyALL():
    headers = {
        'Host': 'cn-proxy.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://cn-proxy.com/archives/218',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'UM_distinctid=15be6dc106a49-00d07026689b75-396b4e08-100200-15be6dc106e1197; CNZZDATA5540483=cnzz_eid%3D1279388291-1494221474-null%26ntime%3D1494423679'
    }
    url = 'http://cn-proxy.com'
    response = requests.get(url=url, headers=headers)

    html_soup = BS(response.content, 'lxml')
    tbodies = html_soup.find_all(name='tbody')   #因为有两个tbody标签
    tr_list = []
    for i in range(0, len(tbodies)):
        tbody_soup = BS( str( tbodies[i] ), 'lxml')  #转换为string
        tr = tbody_soup.find_all(name='tr')

        for i in range(0, len(tr)):
            tr_soup = BS( str(tr[i]), 'lxml' )
            s = tr_soup.find_all(name='td')
            ip = s[0].string
            port = s[1].string
            tr_list.append(ip + ':' + port)   #存储
    return tr_list

class Proxies(threading.Thread):
    def __init__(self, queue, proxy_ip_list):
        threading.Thread.__init__(self)
        self.__queue = queue
        self.__proxy_ip_list = proxy_ip_list

    def run(self):
        global baiduHeader
        while not self.__queue.empty():
            proxy_ip = self.__queue.get()
            if proxy_ip.split(':')[1] == '80':
                proxies = {'http':proxy_ip}
            else:
                proxies = {'https':proxy_ip}
            #print proxies
            try:
                session = requests.session()
                response = session.get(url='http://www.baidu.com', headers=baiduHeader, proxies=proxies)
                #print response.status_code
                if response.status_code == 200:
                    self.__proxy_ip_list.append(proxies)
            except BaseException, e:
                print "ConnectionError", e

            #self.__queue.task_done()


def getProxy(proxied_ip):
    queue = Queue()
    proxy_ip_list = []    #存放最终可以用的Proxy IP
    threads = []
    for proxy in proxied_ip:
        queue.put(proxy)

    threads = [ Proxies(queue, proxy_ip_list) for i in range(0, 20) ]

    for i in range(len(threads)):
        threads[i].start()
        time.sleep(0.1)

    for i in range(len(threads)):
        threads[i].join()

    #queue.join()
    return proxy_ip_list  #结果返回

def getPorxyIP():
    proxies_ip = getProxyALL() #获取所有的代理IP
    #print proxies_ip
    proxies_ip_used = getProxy(proxies_ip) #获取代理IP中所有可用的代理IP
    return proxies_ip_used     #如果其他程序调用就返回

if __name__ == '__main__':
    proxies_ip = getPorxyIP()
    print len(proxies_ip)
