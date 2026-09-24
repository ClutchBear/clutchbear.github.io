---
title: "用python实现冒泡排序 选择排序 插入排序"
description: "### 冒泡法排序"
pubDatetime: 2014-08-31T22:14:21
draft: false
tags: ["python"]
---

- ### 冒泡法排序
第一个循环倒序,相邻两个元素比较大小然后交换.第一次将最大的一个逐渐排序到列表最后一个位置.
```
from __future__ import print_function, unicode_literals, division

arry = [16, 134, 15, 1, 78, 10, 9]


def bubble_sort(arry):
    for i in range(len(arry) - 1, 0, -1):
        for j in range(i):
            if arry[j] > arry[j + 1]:
                arry[j], arry[j + 1] = arry[j + 1], arry[j]

if __name__ == "__main__":
    bubble_sort(arry)
    print (arry)
```

    [1, 9, 10, 15, 16, 78, 134]
    
- ### 选择法排序
第一个元素和后面所有元素对比,找到最小的一个,然后交换.
```
from __future__ import print_function, unicode_literals, division

arry = [16, 134, 15, 1, 78, 10, 9]


def select_sort(arry):
    length = len(arry)

    for i in range(length - 1):
        sort_index = i
        for j in range(i, length):
            if arry[j] > arry[sort_index]:
                sort_index = j
        arry[sort_index], arry[i] = arry[i], arry[sort_index]

if __name__ == "__main__":
    select_sort(arry)
    print(arry)
```

    [1, 9, 10, 15, 16, 78, 134]
- ### 插入排序

最开始以第一个元素为准,第二个元素与第一个比较,排序.第三个与前两个比较然后排序.以此类推.
```
rom __future__ import print_function, unicode_literals, division

arry = [17, 23, 20, 14, 12, 25, 1, 20, 81, 14, 11, 12]


def select_sort(arry):
    length = len(arry)

    for i in range(length - 1):
        sort_index = i
        for j in range(i, length):
            if arry[j] < arry[sort_index]:
                sort_index = j
        if sort_index != i:
            arry[sort_index], arry[i] = arry[i], arry[sort_index]

if __name__ == "__main__":
    select_sort(arry)
    print(arry)
````
  
    [1, 11, 12, 12, 14, 14, 17, 20, 20, 23, 25, 81]
