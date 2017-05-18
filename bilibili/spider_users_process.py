#!/usr/bin/env python
#coding:utf-8


import requests
import time, json, sys, copy, random
from multiprocessing import Process, Pool, freeze_support
from Queue import Queue
import MySQLdb
from DBUtils.PooledDB import PooledDB
sys.path.append('..')
from proxy_ip.getProxy_Process import *


userAgent = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'UCWEB7.0.2.37/28/999',
    'NOKIA5700/ UCWEB7.0.2.37/28/999',
    'Openwave/ UCWEB7.0.2.37/28/999',
    'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999'
    ]

headers = {
    'Host': 'space.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/1/',
    'Content-Length': '11',
    'Cookie': 'finger=7360d3c2; UM_distinctid=15c1134c6aad8-0d27d672160cad-5393662-100200-15c1134c6abed; pgv_pvi=3224074240; fts=1494937291; buvid3=CD8D2E8B-2CAE-47CB-B50F-0647CEE2A03D31463infoc; rpdid=omqpoqpqpidoplplkmixw',
    'Connection': 'close',
    'Cache-Control': 'max-age=0'
}

payloads = {
    'mid': '1',
    'csrf': ''
}


pool = PooledDB(MySQLdb, mincached=5, host='127.0.0.1', user='root', passwd='yangjinxin', db='bilibili_user',
                port=3306, charset='utf8')


def put_user(user_info):
    global pool
    id = int( user_info['data']['mid'] )
    name = user_info['data']['name'].encode('utf-8')
    sex = user_info['data']['sex'].encode('utf-8')
    level = int( user_info['data']['level_info']['current_level'] )

    print id,
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_info(`mid`, `name`, `sex`, `level`) VALUE(%s, %s, %s, %s);" , (id, name, sex, level))
    cursor.close()
    conn.commit()
    conn.close()


def spider(args):        # url_referer = http://space.bilibili.com/1
        #重构报头和载荷，不能对全局变量进行复制，会影响到其他进程
        global  headers, payloads, userAgent
        url_referer = args[0]
        proxies_ip = args[1]

        headers = copy.deepcopy(headers)
        payloads = copy.deepcopy(payloads)
        proxies = proxies_ip[random.randint(0, len(proxies_ip)-1)]

        headers['Referer'] = url_referer
        headers['User-Agent'] = userAgent[random.randint(0, len(userAgent)-1)]
        payloads['mid'] = url_referer.split('/')[-1]
        url = 'http://space.bilibili.com/ajax/member/GetInfo'

        try:
            session = requests.session()
            response = session.post(url, headers=headers, data=payloads, proxies=proxies)
            print
            print response.status_code,

            if response.status_code == 200:
                user_info = json.loads(response.text)  # 反序列化返回的JSON数据
                if user_info['status']:
                    put_user(user_info)   #调用函数
                return 0
            else:  #如果status_code不是200，说明服务器拒绝，则重新把URL放回队列
                return int(url_referer.split('/')[-1])

        #讲道理把异常抛出后，就继续执行
        except BaseException, e:
            print e
            return 0

def run(number_list, proxies_ip):
    p = Pool()
    url_referer = 'http://space.bilibili.com/'
    result = []
    for i in number_list:
        args = [url_referer+str(i), proxies_ip]
        result.append( p.apply_async(spider, args=(args,)) )

    p.close()
    p.join()
    result_data = [x.get() for x in result]
    return [ x for x in result_data if x!=0 ]    #把403的重新放回队列

def main():
    print "Getting Proxy IP..."
    proxies_ip = get_proxy_ip()  #从getProxy_Process.py中获取代理IP
    print 'Staring Spider...', time.ctime()
    number_list = range(1, 1001)
    while len(number_list):
        number_list = run(number_list, proxies_ip)
        time.sleep(60)

if __name__ == '__main__':
    freeze_support()
    main()


