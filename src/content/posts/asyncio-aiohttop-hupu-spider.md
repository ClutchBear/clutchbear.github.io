---
title: "用asyncio协程和aiohttp爬取虎扑步行街前100页的主贴"
description: "!/usr/bin/env python"
pubDatetime: 2017-08-17T20:11:01
draft: false
tags: ["python"]
---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import time
from pyquery import PyQuery as pq
import sys
import codecs
import json


async def get_post_url(url):
    '''
    得到每一页的所有链接
    '''
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            body = await response.text(encoding="utf-8")
            # print(body)
            post_list = parser(body)
            for post_url in post_list:
                post = {}
                post["url"] = post_url
                post_urls.append(post_url)


async def get_post_info(url):
    '''
    根据链接得到标题 作者 发帖时间等内容
    '''
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            body = await response.text(encoding="utf-8")
            post_info = paser_post(body)
            if post_info is not None:
                post_info["url"] = url
                post_lists.append(post_info)


def paser_post(html):
    '''
    解析列表页
    '''
    post_info = {}
    doc = pq(html)
    main_post = doc('div#tpc')
    post_author = main_post.find('div.author a.u').text()
    post_time = main_post.find('div.author span.stime').text()
    post_title = doc('h1#j_data').text()
    post_info["title"] = post_title
    post_info['time'] = post_time
    post_info['author'] = post_author
    if not post_title and not post_time and not post_author:
        return None
    return post_info


def parser(html):
    '''
    解析帖子页
    '''
    post_list = []
    doc = pq(html)
    links_item = doc('table[id="pl"]').find('tbody').find('tr[mid]')
    for link_item in links_item.items():
        post_link = link_item.find('td.p_title').find('a').attr('href')
        post_link = "https://bbs.hupu.com" + post_link
        post_list.append(post_link)
    return post_list


# 得到开始时间
start_time = time.time()
# 存储数据的列表
post_lists = []
# 每一个帖子链接的列表
post_urls = []
# 创建时间循环
loop = asyncio.get_event_loop()

# 将步行街前一百的链接加入事件循环, 同时访问这100页, 得到所有的帖子链接
urls = [
    "https://bbs.hupu.com/bxj-postdate-{}".format(i) for i in range(1, 101)]
tasks = [get_post_url(url) for url in urls]
loop.run_until_complete(asyncio.wait(tasks))
# 输出帖子总数
print(len(post_urls))
# 将所有帖子链接加入事件循环, 得要内容
for i in range(0, len(post_urls), 1000):
    lenth = len(post_urls) - i
    if lenth >= 1000:
        lenth = 1000
    print(i)
    end_time = time.time()
    print("cast time", end_time - start_time)
    tasks = [get_post_info(post_urls[num + i]) for num in range(lenth)]
    loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# 存储所有数据.
post_dicts = {"posts": post_lists, "lenth": len(post_lists)}
with codecs.open("post.json", "w", "utf-8") as f:
    f.write(json.dumps(post_dicts, indent=True))
end_time = time.time()

print("cast time", end_time - start_time)
```

因为虎扑没有登录只能看到前100页的帖子.
总共11594个主贴, 总共耗费了358秒.
大概每秒爬32个帖子.
开了500个协程和1000个协程,速度差不多.
应该是单ip的极限了.



