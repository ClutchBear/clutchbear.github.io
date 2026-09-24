---
title: "辗转相除法找最大公约数的python实现"
description: "辗转相除法,参加维基百科:连接"
pubDatetime: 2014-11-06T01:23:31
draft: false
tags: ["python"]
---

辗转相除法,参加维基百科:[连接](http://zh.wikipedia.org/wiki/%E8%BC%BE%E8%BD%89%E7%9B%B8%E9%99%A4%E6%B3%95)

最大公约数的python最常见算法:

```
def gcd(a, b):
    if a < b:
        a, b = b, a
    while b:
        a, b = b, a % b

    return a
```

最小公倍数就是 两个数的乘积除以最大公约数.

```
def ICM(a, b):
    return a * b / GCD(a, b)

```