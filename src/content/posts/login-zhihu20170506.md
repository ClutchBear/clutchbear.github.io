---
title: "20170506 可用的登录知乎的python代码"
description: "python"
pubDatetime: 2017-05-06T14:03:47
draft: false
tags: ["python"]
---

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import json
import os


url = 'https://www.zhihu.com'
loginURL = 'https://www.zhihu.com/login/email'
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    "Referer": "https://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}
data = {
    'email': 'xxxxx',
    'password': 'xxxxx',
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
    captchaURL = 'https://www.zhihu.com/captcha.gif?=' + \
        str(timestamp) + "&type=login"
    print captchaURL
    with open('zhihucaptcha.gif', 'wb') as f:
        captchaREQ = s.get(captchaURL, headers=headers)
        f.write(captchaREQ.content)
    loginCaptcha = raw_input('input captcha:\n').strip()
    data['captcha'] = loginCaptcha
    print data
    loginREQ = s.post(loginURL, headers=headers, data=data)
    if not loginREQ.json()['r']:
        print s.cookies.get_dict()
        with open('cookiefile', 'wb') as f:
            json.dump(s.cookies.get_dict(), f)
    else:
        print 'login fail'

```