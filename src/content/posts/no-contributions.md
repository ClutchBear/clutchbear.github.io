---
title: "contributions不显示在github上"
description: "最近不知道怎么搞的,hexo提交了茫茫多次到github上,但在github账号页面不显示contributions绿点.自己的努力没有显示出来,十分的不爽."
pubDatetime: 2014-08-11T11:36:01
draft: false
tags: ["hexo"]
---

最近不知道怎么搞的,hexo提交了茫茫多次到github上,但在github账号页面不显示contributions绿点.自己的努力没有显示出来,十分的不爽.
尝试各种方法解决,甚至去hexo的github页面提交issues,别人回答我说,hexo提交后就会有contributions显示的.
最后发现是.gitconfig不知道被哪个软件修改了,删掉.gitconfig配置文件.
再终端重新建立一个就行了:

```
git config --global user.name "你的名字"
git config --global user.email "your_email@youremail.com"
```

最后转帖一个高手的文章:[什么样的contributions会被Github计算在内？](http://blog.segmentfault.com/spacewander/1190000000520300)