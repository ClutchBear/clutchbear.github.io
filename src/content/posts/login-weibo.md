---
title: "模拟登陆sina微博"
description: "!/usr/bin/env python"
pubDatetime: 2015-08-25T19:47:44
draft: false
tags: ["python"]
---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'http://login.weibo.cn/login/'
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'}
post_data = {'mobile': 'roc100year@gmail.com',
             'backURL': 'http://weibo.cn/',
             'backTitle': u'微博',
             'submit': u'登录',
             'remember': 'on',
             'tryCount': ''
             }
html = requests.get(url, headers=my_headers).content
soup = BeautifulSoup(html, "html.parser")
password = soup.find('input', {'type': 'password'}).get('name')
vk = soup.find('input', {'name': 'vk'}).get('value')
print password, vk
post_data[password] = 'xxxxx'
post_data['vk'] = vk
new_html = requests.post(url, data=post_data).content
print new_html
```