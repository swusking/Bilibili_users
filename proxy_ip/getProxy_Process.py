#!/usr/bin/env python
#coding:utf-8

import requests, re, time
from bs4 import BeautifulSoup as BS
from multiprocessing import Process, Pool, freeze_support
from Queue import Queue

baiduHeader = {
    'Host': 'www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'BIDUPSID=7B518EC75B729A6C7368A7E4968D1C19; PSTM=1494813509; BAIDUID=FF29F2870B37C78585A7D2E4F4C51B98:FG=1; BD_HOME=0; H_PS_PSSID=22675_1460_21110_17001_22919_22072; BD_UPN=12314753; __bsi=18221270840967475209_00_0_I_R_96_0303_C02F_N_I_I_0'
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
        'Cookie': 'UM_distinctid=15c142f5cb8329-014fa334b038d2-5393662-100200-15c142f5cb93d6; CNZZDATA5540483=cnzz_eid%3D439904357-1494982263-%26ntime%3D1494982263'
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

def test_ip(proxies_ip):
    global baiduHeader

    if proxies_ip.split(':')[1] == '80':
        proxies = {'http': proxies_ip}
    else:
        proxies = {'https': proxies_ip}

    try:
        response = requests.get(url='http://www.baidu.com', headers=baiduHeader, proxies=proxies)
        print response.status_code, proxies
        if response.status_code == 200:
            return proxies
        else:
            return 0
    except BaseException, e:
        print e
        return 0     #error

def getProxy(proxies_ip):
    p = Pool()

    result = []
    for i in xrange(len(proxies_ip)):
        result.append( p.apply_async(test_ip, args=(proxies_ip[i],)))

    p.close()  #不再添加进程
    p.join()

    x = [x.get() for x in result]    #使用get得到返回值
    proxies_ip_used = [ y for y in x if y != 0]

    return proxies_ip_used   #返回可用代理IP

def get_proxy_ip():

    proxies_ip = getProxyALL() #获取所有的代理IP
    #print proxies_ip
    proxies_ip_used = getProxy(proxies_ip) #获取代理IP中所有可用的代理IP
    return proxies_ip_used     #如果其他程序调用就返回

if __name__ == '__main__':
    freeze_support()    #Windows下必须有，不然会出问题
    proxies_ip = get_proxy_ip()
    print len(proxies_ip)
