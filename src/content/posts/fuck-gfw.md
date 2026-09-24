---
title: "MAC下面修改hosts和获得最新hosts的方法"
description: "因为某些原因google搜索经常被屏蔽,但是工作需要经常使用.修改hosts是访问google最方便的方法之一."
pubDatetime: 2015-08-07T16:44:25
draft: false
tags: ["科学上网"]
---

因为某些原因google搜索经常被屏蔽,但是工作需要经常使用.修改hosts是访问google最方便的方法之一.

1: 10.9.5的MAC下修改hosts的方法,搜索得来的,
   在终端输入:
```                  
    sudo /Applications/TextEdit.app/Contents/MacOS/TextEdit /etc/hosts
```
   10.10 Yosemite
   打开finder,选择前往文件夹,填入
```   
    /etc/hosts,
```
   将hosts拖到桌面,修改.然后再覆盖进去.
   
2: 获取hosts的几种方法,
   github大神制作好的的hosts文件,直接拷贝就行了.
   
   获取最新hosts的网站,
   
   ```
    https://github.com/vokins/simpleu
    https://github.com/racaljk/hosts
   ```
   
   一个hosts不好用时候,及时更换成另外一个.

3: 用chrome浏览器的话,在设置里把默认搜索改成:
   
     https://www.google.com/search?q=%s
   
   并且在浏览器中运行一次:
   
     https://www.google.com/ncr
   
  防止自动跳转到google.com.hk

4: 日常科学上网用shadowsocks,
[官网点这里](https://github.com/clowwindy/shadowsocks),
安装运行后,免费得ss网站上获取服务器和密码

### 大神总结的翻墙小结.各种系统的都有, 
[这里是连接](
http://wsgzao.github.io/post/gfw-break/)


