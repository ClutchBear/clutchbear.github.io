---
title: "Mac10.10系统下用python抓取淘宝时出现sslv3 alert handshake failure (_ssl.c:590)的解决办法"
description: "用python的requests库模拟抓取淘宝页面时会出现如下错误,"
pubDatetime: 2015-09-25T18:44:31
draft: false
tags: ["python"]
---

用python的requests库模拟抓取淘宝页面时会出现如下错误,

```
requests.exceptions.SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:590)
```
![](http://ww3.sinaimg.cn/large/7293e3b7jw1ewew5jglasj20ut061djd.jpg)

换成自带的urllib也是一样报错,
但是在windows系统下同样的代码正常,没有任何错误.

开始以为是openssl的问题, 把系统自带的openssl删除,然后用brew安装最新版本的openssl也不行.

根据stackoverflow大神的帖子,我试了很多方式,最终找到一个解决这个错误的方法.

在python中加入以下语句即可.

```
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
```

![](http://ww2.sinaimg.cn/large/7293e3b7jw1ewewd68bx3j20wv0lf16w.jpg)


参考链接 :  [Stack Overflow](http://stackoverflow.com/questions/31730819/python-sslerror-using-requests-for-surveymonkey-com)