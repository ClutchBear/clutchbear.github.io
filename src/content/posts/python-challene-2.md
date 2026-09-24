---
title: "21一个挑战题的python解决方法"
description: "2) 一百万"
pubDatetime: 2014-11-14T01:36:26
draft: false
tags: ["python"]
---

### 2) 一百万

挑战：将 1,000,000 写成两个数的乘积，两个数都不包含零

```
for i in range(1, 500000):
    for j in range(1, 50000):
        if i * j == 1000000:
            if '0' not in str(i) and '0' not in str(j):
                print i, j
                break

```

结果是:

```
64 15625
```