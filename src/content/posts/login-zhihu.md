---
title: "python模拟登陆知乎"
description: "第一次登陆的时候需要手动输入验证码,"
pubDatetime: 2016-08-11T11:22:12
draft: false
tags: ["python"]
---

第一次登陆的时候需要手动输入验证码,
之后用cookie登陆.

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-11-12 20:08:49
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import time
import json
import os
url = 'http://www.zhihu.com'
loginURL = 'http://www.zhihu.com/login/email'
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}
data = {
    'email': 'xxxxxx@gmail.com',
    'password': 'xxxxxxxxx',
    'rememberme': "true",
}
s = requests.session()
if os.path.exists('cookiefile'):
    with open('cookiefile') as f:
        cookie = json.load(f)
    s.cookies.update(cookie)
    req1 = s.get(url, headers=headers)
    # 建立一个zhihu.html文件,用于验证是否登陆成功
    with open('zhihu.html', 'w') as f:
        f.write(req1.content)
else:
    req = s.get(url, headers=headers)
    print req
    soup = BeautifulSoup(req.text, "html.parser")
    xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
    data['_xsrf'] = xsrf
    timestamp = int(time.time() * 1000)
    captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
    print captchaURL
    with open('zhihucaptcha.gif', 'wb') as f:
        captchaREQ = s.get(captchaURL)
        f.write(captchaREQ.content)
    loginCaptcha = raw_input('input captcha:\n').strip()
    data['captcha'] = loginCaptcha
    print data
    loginREQ = s.post(loginURL,  headers=headers, data=data)
    if not loginREQ.json()['r']:
        print s.cookies.get_dict()
        with open('cookiefile', 'wb') as f:
            json.dump(s.cookies.get_dict(), f)
    else:
        print 'login fail'

```