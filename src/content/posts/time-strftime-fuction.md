---
title: "time.strftime()用法"
description: "参考 链接 和 链接"
pubDatetime: 2015-09-02T22:28:40
draft: false
tags: ["python"]
---

参考 [链接](http://www.w3cschool.cc/python/att-time-strftime.html) 和 [链接](https://github.com/qiwsir/ITArticles/blob/master/Python/%E8%8E%B7%E5%8F%96%E6%97%B6%E9%97%B4%E7%9A%84%E6%96%B9%E6%B3%95.md)

### 描述
Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。

### 语法
strftime()方法语法：

    time.strftime(format[, t])
### 说明
python中时间日期格式化符号：

%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身

### 实例
- ###获取时间的方法

```
>>>import time
>>>this_time=time.localtime()
>>> this_time
time.struct_time(tm_year=2013, tm_mon=6, tm_mday=6, tm_hour=13, tm_min=42, tm_sec=38, tm_wday=3, tm_yday=157, tm_isdst=0)
>>> type(this_time)
<type 'time.struct_time'>

>>> this_year=this_time[0]
>>> this_year
2013
>>> for time in this_time:
...     print time
...
2013
6
6
13
42
38
3
157
0

time.strftime('%Y-%m-%d %T',time.localtime(time.time())
 # 2014-09-04 23:42:34
```

- ### 取过去具体时间的方法:

```
import time

 #取一天前的当前具体时间
time.strftime('%Y-%m-%d %T',time.localtime(time.time()-24*60*60))

 #取20天前的当前具体时间
time.strftime('%Y-%m-%d %T',time.localtime(time.time()-20*24*60*60))

 #取20天前当前具体时间的前2小时
time.strftime('%Y-%m-%d %T',time.localtime(time.time()-20*24*60*60-2*60*60))
```
