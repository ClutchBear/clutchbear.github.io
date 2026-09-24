---
title: "python + requests抓取百度百科时候遇到的乱码问题"
description: "今天用python的requests抓住百度百科的老残游记条目时候出现乱码问题，"
pubDatetime: 2015-08-15T03:05:06
draft: false
tags: ["python"]
---

今天用python的requests抓住百度百科的老残游记条目时候出现乱码问题，
试了好多方法都没有解决。
最后通过谷歌搜索到大神的博客才懂，原来是requests库的问题。
大神博客[点这里](http://sh3ll.me/2014/06/18/python-requests-encoding/)

根据官方文档http://docs.python-requests.org/en/latest/api/#requests.Response.text，
requests 是通过 http header 猜测页面编码，如果 header 中不存在 charset 就认为编码为 ISO-8859-1。
我抓取的这个百度百度的headers的charset就没有设置编码。
要手动指定成'utf-8'才行。

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import codecs

url = 'http://baike.baidu.com/view/37202.htm'
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
              }
session = requests.session()
req = session.get(url, headers=my_headers)
req.encoding = 'utf-8'

soup = BeautifulSoup(req.text, "html.parser")
item = soup.find('div', {'class': 'para'})

print item.get_text().encode('utf-8')

```
![](http://ww2.sinaimg.cn/large/7293e3b7jw1ev3jups6s7j21970pzn35.jpg)


参考：
http://sh3ll.me/2014/06/18/python-requests-encoding/
http://liguangming.com/python-requests-ge-encoding-from-headers