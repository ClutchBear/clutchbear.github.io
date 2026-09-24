---
title: "win10下面python的codecs模块写入txt文件，用记事本打开显示不换行bug"
description: "今天用beautifulsoup爬取网页，把解析出的unicode格式的内容写到txt文本文件里面。"
pubDatetime: 2015-08-04T20:28:41
draft: false
tags: ["Windows"]
---

今天用beautifulsoup爬取网页，把解析出的unicode格式的内容写到txt文本文件里面。
发现用codecs模块写入的txt文件，用记事本打开后，死活不换行。
f.write('\n')不行，f.write('\n'.decode('utf-8')也不行。
谷歌了好久，也没有找出解决办法。
![](http://ww2.sinaimg.cn/large/7293e3b7jw1euph3aw2gij20sq05xq3p.jpg)

跟上海知乎群里的python大神 光大证券的唐老师咨询，他说他用f.write('\n')可以换行。

这时候我怀疑是不是win10系统记事本的问题，把保存好的txt文件拖到sublime text3上打开，果然各种正常换行了。
![](http://ww2.sinaimg.cn/large/7293e3b7jw1euph3xhwwwj20p308ygo7.jpg)

看来，新出的win10系统还是有各种小bug啊。