---
title: "hexo新版的一个重大bug或者说改动"
description: "连续hexo g出错,害的我还以为我系统坏掉了."
pubDatetime: 2014-07-16T08:20:39
draft: false
tags: ["hexo"]
---

连续hexo g出错,害的我还以为我系统坏掉了.
重装了好几次.
原来是hexo 最新版本2.8.0跟主题出现冲突了
更改了一些东西.

### 官网的回答
tommy351 commented 2 days ago
YAML parser was changed in Hexo 2.8. You have to wrap strings like this with quotation marks.

archive_b: Archives: %s => archive_b: "Archives: %s"

https://github.com/hexojs/hexo/issues/722
