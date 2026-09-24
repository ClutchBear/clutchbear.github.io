---
title: "个人爬虫常用的几个知识点"
description: "1 最常用beautifulsoup4的几个语法"
pubDatetime: 2015-09-29T02:41:54
draft: false
tags: ["python"]
---

### 1 最常用beautifulsoup4的几个语法

```
from bs4 import BeautifulSoup

soup  = BeautifulSoup(r.text)
```

如果搜索很多标签用

```
soup.find_all('div', {'class':True, 'id': True, 'title': True}),
```
 然用用for遍历,

搜索单个标签用
```
soup.find('div', {'class':True, 'id': True, 'title': True} )
```
find和find_all可以多次套用.

获取内容用

```
item.get_text().encode('utf-8'), cmd显示的话用'gbk'
```

获取div标签的其他属性用

```
item.get('href')
```

生成所有子标签的列表(list)用contains()函数,

```
childtag = soup.contents()
```
 常用作输出部分子标签的内容. 比如

```
childtag[0].get_text(), childtag[-1].get_text()
```



### 2 python中生成13位时间戳的方法

```
import time

print str(int(time.time() * 1000))
```

###  3 requests的req.encoding如果没有获取到正确的编码

可以用以下方法解决

```
req.encoding = 'gb2312'
```

或者

```
req.encoding = 'utf-8'
```

或者

```
req.encoding = apparent_encoding
```


### 4 模拟登录的时候需要用requsts的senssion()函数.

会话对象让你能够跨请求保持某些参数。它也会在同一个Session实例发出的所有请求之间保持cookies。

```
s = requests.session()
```


