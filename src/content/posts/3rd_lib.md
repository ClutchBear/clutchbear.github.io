---
title: "Python2.7 常用第三方库的安装方法"
description: "1: 安装PIL或者PILLOW的方法:"
pubDatetime: 2015-08-23T15:18:39
draft: false
tags: ["python"]
---

## 1: 安装PIL或者PILLOW的方法:
PIL是Python Imaging Library的简写,是Python中最常用的图像处理库.

如果是MAC 10.9.4系统的话, 用sudo easy_install PIL安装pil可能会出现错误,谷歌搜索的话,很多人都会出现这样那样的问题.

pillow是pil的替代品,更容易安装.pillow的最新信息可以参考[这里](http://pillow.readthedocs.org/en/latest/)或者[中文文档](http://pillow-cn.readthedocs.org/zh_CN/latest/index.html)

- 安装方法:

```
       brew install libtiff libjpeg webp little-cms2
       sudo pip install pillow
```

- 使用方法:在需要import Image,ImageDraw的地方用下面的语句代替

```
from PIL import Image,ImageDraw
```
     
## 2: 安装和使用virtualenv
virtualenv 用来创建隔离的Python环境。它会创建一个拥有独立安装目录的python环境，该隔离环境不会与其他virtualenv环境共享模块（可选择是否访问全局库目录）。

- 安装:

```
pip install virtualenv
```

- 简单使用:

```      
      mkdir testdir
      cd testdir
      virtualenv venv --distribute #初始化
      . venv/bin/activate 激活
      deactivate 退出
```
###3: MySQL安装
MySQL是目前最流行的开源数据库之一.
- 安装:

```  
      brew intall MySQL #系统的Mysql
      sudo ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install mysql-python #python的MySQL
```

- 使用:

``` 
      mysql.server start
```      

### 4: Pygame安装
需要去官方(http://www.pygame.org/download.shtml)下载
pygame-1.9.2pre-py2.7-macosx10.7.mpkg.zip,解压缩后安装在mac10.10上才行.

### 5: Scrapy安装

```
pip install Scrapy
```

很快安装成功,
但是新建项目时候出错了

```
scrapy startproject tutorial
``` 

![](http://ww3.sinaimg.cn/large/7293e3b7jw1evclegfxc9j20st086ju2.jpg)

解决方法也很简单,根据错误提示谷歌搜索,打开第一个结果的stackoverflow网站,按照答案一步一步来就行.

```
sudo rm -rf /Library/Python/2.7/site-packages/six*
sudo rm -rf /System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six*
sudo pip install six
```

参考: [stackoverflow真是好地方](http://stackoverflow.com/questions/30964836/scrapy-throws-importerror-cannot-import-name-xmlrpc-client)