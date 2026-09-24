---
title: "用python找出知乎某个答案点赞的所有名单"
description: "!/usr/bin/env python"
pubDatetime: 2016-08-16T10:01:25
draft: false
tags: ["python"]
---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import json
import os
import sys

url = 'http://www.zhihu.com'
loginURL = 'http://www.zhihu.com/login/email'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

data = {
    'email': 'xxxxx@gmail.com',
    'password': 'xxxxxxx',
    'rememberme': "true",
}

s = requests.session()
# 如果成功登陆过,用保存的cookies登录
if os.path.exists('cookiefile'):
    with open('cookiefile') as f:
        cookie = json.load(f)
    s.cookies.update(cookie)
    req1 = s.get(url, headers=headers)
    with open('zhihu.html', 'w') as f:
        f.write(req1.content)
# 第一次需要手动输入验证码登录
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
    # print data
    loginREQ = s.post(loginURL,  headers=headers, data=data)
    # print loginREQ.url
    # print s.cookies.get_dict()
    if not loginREQ.json()['r']:
        # print loginREQ.json()
        with open('cookiefile', 'wb') as f:
            json.dump(s.cookies.get_dict(), f)
    else:
        print 'login failed, try again!'
        sys.exit(1)

# 以http://www.zhihu.com/question/27621722/answer/48820436这个大神的399各赞为例子.
zanBaseURL = 'http://www.zhihu.com/answer/22229844/voters_profile?&offset={0}'
page = 0
count = 0
while 1:
    zanURL = zanBaseURL.format(str(page))
    page += 10
    zanREQ = s.get(zanURL, headers=headers)
    zanData = zanREQ.json()['payload']
    if not zanData:
        break
    for item in zanData:
        # print item
        zanSoup = BeautifulSoup(item, "html.parser")
        zanInfo = zanSoup.find('a', {'target': "_blank", 'class': 'zg-link'})
        if zanInfo:
            print 'nickname:', zanInfo.get('title'),  '    ',
            print 'person_url:', zanInfo.get('href')
        else:
            anonymous = zanSoup.find(
                'img', {'title': True, 'class': "zm-item-img-avatar"})
            print 'nickname:', anonymous.get('title')

        count += 1
    print count
```

![](http://ww1.sinaimg.cn/large/7293e3b7jw1exjcxedihvj20p40l0dl1.jpg)