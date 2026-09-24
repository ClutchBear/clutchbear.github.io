---
title: "计算素数比较快的方法"
description: "计算素数里面除数最大值用(int(prime 0.5) +1) ,最好不要用(prime / 2 + 1).在素数值非常大的时候,这两者差距非常明显."
pubDatetime: 2014-10-03T01:19:34
draft: false
tags: ["python"]
---

计算素数里面除数最大值用(int(prime ** 0.5) +1) ,最好不要用(prime / 2 + 1).在素数值非常大的时候,这两者差距非常明显.
比如104729的开方值:323
    除以2的值是52365
    
再就是尽量用函数返回Ture Flase的判断,

例如: 求第10000个素数

```
prime = 2
number = 4


def is_prime(num):
    for x in range(2, int((num ** 0.5)) + 1):
        if num % x == 0:
            return False
    return True

while 1:

    if is_prime(number):
        prime += 1
    if prime == 10000:
        break
    number += 1


print number
```
### 用时0.5秒得出结果:104729

如果是

```
prime = 2
number = 4


def is_prime(num):
    for x in range(2, int((num / 2)) + 1):
        if num % x == 0:
            return False
    return True

while 1:

    if is_prime(number):
        prime += 1
    if prime == 10000:
        break
    number += 1


print number
```
### 用时42秒,得出结果104729

如果是

```
prime = 2
number = 4

while 1:
    flag = 0
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            flag = 1
    if flag == 0:
        prime += 1
    if prime == 10000:
        break
    number += 1


print number
```
### 用时3.0秒,得出结果104729