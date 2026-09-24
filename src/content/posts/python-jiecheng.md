---
title: "给定数字N的阶乘N!的末尾有多少个0"
description: "当n到二三十时候,N!已经非常大了,会溢出."
pubDatetime: 2015-09-02T22:13:38
draft: false
tags: ["python"]
---

当n到二三十时候,N!已经非常大了,会溢出.
肯定不能用直接计算出阶乘的方式来统计0的个数.

通常用1到n的数字中,每个数字分解出2和5的个数,因为2 * 5 = 10
因为2个数非常多,因此只要算出5的个数就可以了

```
def zero_num(N):
    count = 0
    for j in range(1, N + 1):
        while j % 5 == 0:
           j /= 5
           count += 1
    return b
```