---
title: "腾讯视频评论动态网页评论的抓取"
description: "!/usr/bin/env python"
pubDatetime: 2015-08-27T20:16:52
draft: false
tags: ["python"]
---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-23 20:03:51
# @Author  : Xin(skywater@gmail.com)
# @Link    : playbear.github.io

import requests
from bs4 import BeautifulSoup
import json

url = 'http://v.qq.com/cover/q/qviv9yyjn83eyfu/c0017ivdw3z.html'
my_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

req = requests.get(url)

soup = BeautifulSoup(req.text, "lxml")


ji_shu = soup.find_all('a', class_='album_link')
for ji in ji_shu:
    num = ji.get_text().encode('utf-8').strip()
    ji_url = 'http://sns.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&vid=' + ji.get('id')
    ji_req = requests.get(ji_url)
    ji_id = json.loads(ji_req.content.split('=')[1][:-1])['comment_id']
    comment_url = 'http://coral.qq.com/article/' + ji_id.encode('utf-8') + '/comment?commentid=0&reqnum=10'
    comment_req = requests.get(comment_url, headers=my_headers)
    for i in comment_req.json()['data']['commentid']:
        print '第%s集' % num, i['userinfo']['nick'], i['timeDifference']
        print i['content']
        print
    raw_input()
```