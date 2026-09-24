---
title: "sublime text3 侧边栏字体的修改方法"
description: "正常情况下sublime text3的侧边栏字体很小,不仔细看的话,很难看清楚."
pubDatetime: 2015-09-24T19:00:47
draft: false
tags: ["软件"]
---

正常情况下sublime text3的侧边栏字体很小,不仔细看的话,很难看清楚.
![](http://ww1.sinaimg.cn/large/7293e3b7jw1ewdr2r13pnj20c40hetb8.jpg)

需要把字号修改的大一些,
网上搜索说,要下载一个插件然后打开主题的配置文件.我找到一个更简单的方法,

- 在sublime text3的属性里面找到Browse packages,打开插件所在文件夹,进入主题目录,找到要修改的配置文件,拖到sublime text中.

- 搜索"sidebar_label", 在后面添加上

```
"font.size": 16,
```

 windows系统下的话, 再加一句字体修改

 ```
 "font.face": "courier",
 ```

- 如果觉得行之间空间太挤,可以通过搜索"sidebar_tree",将padding[8, 3]后面的数值改成5或者6.
  同一个class下面的"indent"是文件名的缩进, 也可以根据自己的情况修改一下.
  
  ![](http://ww4.sinaimg.cn/large/7293e3b7jw1ewdrfq3xlwj20d20e0jtw.jpg)
  
  最后这样,感觉好多了.
 