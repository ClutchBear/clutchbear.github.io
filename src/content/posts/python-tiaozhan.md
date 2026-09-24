---
title: "pythontip 网站难题答案汇总"
description: "pythontip 网站的挑战python题目中有些很难和需要算法来解出."
pubDatetime: 2015-09-02T22:09:11
draft: false
tags: ["python"]
---

pythontip 网站的挑战python题目中有些很难和需要算法来解出.

#### 9:给你两个正整数a和b， 输出它们的最大公约数。
解题思路:用辗转相除法

```
if a < b:
    a, b = b, a

while b:
    a, b = b, a % b

print a
```

#### 11:给你一个正整数列表 L, 如 L=[2,8,3,50], 输出L内所有数字的乘积末尾0的个数,如样例L的结果为2.(提示:不要直接相乘,数字很多,可能溢出)

思路: 利用每个数字包含2和5的个数来判断,存在一对2 * 5 就是一个0

```
a, b = 0, 0
for i in L:
    j = i
    while i % 2 == 0:
        i /= 2
        a += 1
    while j % 5 == 0:
        j /= 5
        b += 1

print min(a, b)
```

#### 12:给你一个正整数列表 L, 如 L=[2,8,3,50], 判断列表内所有数字乘积的最后一个非零数字的奇偶性,奇数输出1,偶数输出0. 如样例输出应为0

```
a, b = 0, 0

for i in L:
    j = i
    while i % 2 == 0:
        i /= 2
        a += 1

    while j % 5 == 0:
        j /= 5
        b += 1

if a > b:
    print 0
else:
    print 1
```

#### 13: 光棍们对1总是那么敏感，因此每年的11.11被戏称为光棍节。鄙人光棍几十载，光棍自有光棍的快乐。让我们勇敢面对光棍的身份吧，
####现在就证明自己：给你一个整数a，数出a在二进制表示下1的个数，并输出。

```
count = 0
while a:
    count += a % 2
    a /= 2
print count
```

#### 20:信息加密
####给你个小写英文字符串a和一个非负数b(0<=b<26), 将a中的每个小写字符替换成字母表中比它大b的字母。
####这里将字母表的z和a相连，如果超过了z就回到了a。例如a="cagy",b=3, 则输出 fdjb

```
out_string = ''
for i in a:
   if ord(i) + b <= ord('z'):
        out_string += chr(ord(i)+b)
   else:
        out_string += chr(ord(i)+b-26)

print out_string
```