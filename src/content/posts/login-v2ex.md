---
title: "用request和beautisoup登录、签到v2ex"
description: "代码如下，"
pubDatetime: 2015-08-07T02:36:59
draft: false
tags: ["python"]
---

### 代码如下，

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time


url = 'http://www.v2ex.com'

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
              'Referer': 'http://www.v2ex.com/signin',
              'Host': 'www.v2ex.com',
              }

login_data = {'u': 'roc100year@gmail.com',
              'p': '',
              'next': '/'
              }
time.sleep(3)

session = requests.session()
url_login = url + '/signin'
response = session.get(url_login, headers=my_headers)
soup = BeautifulSoup(response.content, "html.parser")

once = soup.find('input', attrs={'name': 'once'}).get('value').encode('utf-8')


login_data['once'] = once

session.post(url_login, login_data, headers=my_headers)

daily = url + '/mission/daily'

r = session.get(daily, headers=my_headers)
soupDaily = BeautifulSoup(r.text, "html.parser")

item = soupDaily.find('input', class_='super normal button').get('onclick')
mission_url = url + item.split("'")[1]

mission_r = session.get(mission_url, headers=my_headers)
```

### 对我而言，难点是

* ### name是beautifulsoup.find()的关键字，不能用soup.find(name = 'once')查找需要的tag，要用soup.find（attrs={'name': 'once'}）才行

* ### 通过chrome的f12--NetWork，找signin，再在下面找到Form Data的post数据
![](http://ww3.sinaimg.cn/large/7293e3b7jw1eusznybzgnj20ix0iqtbo.jpg)


参考来源 ：
[模拟登录V2EX及进行签到](http://blog.leanote.com/post/maijver/Untitled-54c144e238f411103700147a-17)