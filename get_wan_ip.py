# encoding=UTF-8
import re
import urllib.request
import string
from urllib.parse import quote
import time

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_wan_ip_inner():
    word = "我的ip"
    pattern = "((?:(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d)))\\.){3}(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d))))"
    url = 'http://www.baidu.com.cn/s?wd=' + urllib.parse.quote(word) + '&pn=0'
    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf8')
        res = re.search(pattern, html)
        return res.groups()[0]

def get_wan_ip(check_times=3):
    old_ip = ''
    for i in range(check_times):
        ip = get_wan_ip_inner()
        if i != 0 and ip != old_ip:
            return None
        old_ip = ip
        time.sleep(1)
    return old_ip


if __name__ == '__main__':
    print(get_wan_ip())
