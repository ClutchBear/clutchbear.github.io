---
title: "python爬取贴吧楼中楼"
description: "贴吧把每个帖子每页的楼主楼回复都放到一个json数据里面."
pubDatetime: 2015-09-19T20:21:06
draft: false
tags: ["python"]
---

贴吧把每个帖子每页的楼主楼回复都放到一个json数据里面.
首先是找出这个json连接,
用charles抓包发现
![](http://ww2.sinaimg.cn/large/7293e3b7jw1ew81ayffluj20tx09940u.jpg)
链接是这个样子的,

```
http://tieba.baidu.com/p/totalComment?t=1442661243&tid=3924896002&fid=1627732&pn=1&see_lz=0
```
分析后发现,t = 1442661243这个数字是时间,可以用python得time.time()函数得到, tid=3924896002是帖子的数字没啥好说的,
fid=1627732是论坛id我想应该是每个贴吧的数字id,比如dota2贴吧是:1627732.

用bs4分析每个帖子的数据,拼凑出这个链接来就ok.

这是代码,不过不完美.还需要用re把表情 语音什么的过滤掉.根据每个回帖的id遍历字典找到相应的楼中楼回复.

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import time

url = 'http://tieba.baidu.com/p/4044110950'


req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
forum_ids = soup.find('div', class_='p_postlist').find('div', class_='l_post l_post_bright j_l_post clearfix  ').get('data-field')
forum_id = json.loads(forum_ids)['content']['forum_id']
localTime = int(time.time())
commentURL = 'http://tieba.baidu.com/p/totalComment?t=' + str(localTime) + '&tid=' + str(url.split('/')[-1]) + '&fid='+str(forum_id)+'&pn=1&see_lz=0'

print commentURL
commentreq = requests.get(commentURL)

for k, v in commentreq.json()['data']['comment_list'].items():
    for j in v['comment_info']:
        print j['username'].encode('utf-8'),
        print j['content'].encode('utf-8')
    print
    print
```

