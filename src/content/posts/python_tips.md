---
title: "自己需要记住和时常复习的python要点和小技巧"
description: "不定时更新中,"
pubDatetime: 2015-06-29T21:45:43
draft: false
tags: ["python"]
---

不定时更新中,
20141007最新更新

- ### 列出100以内被3整除的数更简单的方法:
  
      range(3,100,3)    


- ### 删除读取文本文件换行回车的方法: 
  
      line.strip()

- ### 判断字符串是否是回文的简单方法:
  
      def isPalindrome(s):
          return s == s[::-1]
    
- ### 字符串的一些方法:
   - S.upper() #S中的字母大写
   - S.lower() #S中的字母小写
   - S.capitalize() #首字母大写
   - S.title() #每个单词首字母大写
   - S.count(str,,) #S字符串范围内str字符出现的次数
   - S.find(str,,) #S字符串范围内第一个str字符的索引
   - S.istitle() #每个单词首字母是否大写的，且其它为小写，
   - S.isupper() #S中的字母是否全是大写
   - S.islower() #S中的字母是否全是小写
   - S.isalpha() #S中的字符是否只有字母组成
   - S.isalnum() #S中得字符是否只有字母或者数字组成
   - S.isdigit() #S中的字符是否只有数字组成
   - S.lower() #全部小写
   - S.upper() #全部大写
   - S.join(S1) #以S为分隔符,将S1中所有元素合并成一个新的字符串
   - S.strip() #去掉S前后的空格
   - S.replace(s1,s2) #将S中的s1用s2代替
 
- ### 在collections模块中有一个Counter类
     Counter类的目的是用来跟踪值出现的次数。它是一个无序的容器类型，以字典的键值对形式存储，其中元素作为key，其计数作为value。计数值可以是任意的Interger（包括0和负数）。
     例如:统计一个字符串中重复字母的在字母表最先出现的字符

```
from collections import Counter


def checkio(text):
    count = Counter([x for x in text.lower() if x.isalpha()])
    m = max(count.values())
    return sorted([x for (x, y) in count.items() if y == m])[0]

if __name__ == "__main__":
    print(checkio("Hello World!"))
    print(checkio("How do you do?"))
    print(checkio(u"One"))
    print(checkio(u"Oops!"))
```

   counter的方法有增加(updata)和减少(subtract)两种:
   比如:

```
count = Counter('which')
count['h']
 #结果显示:2
count.update('witch')
count.['h'] 
 #结果显示:3
```

- ### RE
#### B(括号) 
 在正则表达式中有 3 种类型的括号
 方括号"["内是需要匹配的字符,花括号"{"内是指定匹配字符的数量。 圆括号“(“ 则是用来分组的。
#### C(插入符号)
插入符号 “^” 表示正则式的开始。
#### D(美元符号)
美元符号“$” 表示正则式的结束。


注意:类似(com|net|org)的多选一,用圆括号.

年月日的匹配:
yy-mm-dd

    '^(1[9][0-9][0-9]|2[0][0-1][0-9]|[0-9][0-9])[\.-]?([1-9]|0[1-9]|1[0-2])[\.-]?([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$'
 
时间的匹配:
hh:mm:ss

    '^([0-9]|0[0-9]|1[0-9]|2[0-3])[:]([0-9]|0[0-9]|[0-6][0-9])[:]([0-9]|0[0-9]|[0-5][0-9])$'
 
ip地址的匹配:

     '^(([01]?[0-9][0-9]?|2[0-4][0-9]|2[5][0-5])\.){3}([01]?[0-9][0-9]?|2[0-4][0-9]|2[5][0-5])$'
   
- ### 字母 字符与ASCII数字对应的函数:
    ord（）将字符转换成ascii码数字
    chr()将ascii码数字转换为字符
    unichr()将ascii码整数返回成unicode字符
    
    
- ### random.sample(list, n)通常用来产生不重复的n位数字
       print int(''.join(map(str, random.sample(range(10), 10))))
       #3571490628
    
- ### enumerate的用法
  enumerate会将数组或列表组成一个索引序列。使我们再获取索引和索引内容的时候更加方便：
  
  ```
  for index，text in enumerate(list)): 
      print index ,text
  ```
  