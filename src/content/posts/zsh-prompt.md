---
title: "修改zsh命令提示符"
description: "修改zsh命令提示符"
pubDatetime: 2016-09-13T14:05:35
draft: false
tags: ["系统"]
---

修改zsh命令提示符

+ 安装好zsh后， 打开终端，输入
```
vim ~/.zshrc
```
打开zsh配置文件

+ 在.zshrc最下面加入
```
autoload -U compinit promptinit
compinit
promptinit

# 设置 redhat 主题的默认命令行提示符
prompt redhat
```
启动tab命令补全 和 命令提示符主题,
可以用终端命令'prompt -l'或者'prompt -p'查看可用主题
+ 修改保存后,重启终端,可能出现警告
```
zsh compinit: insecure directories, run compaudit for list.
Ignore insecure directories and continue [y] or abort compinit [n]?
```
按y后,可以出现修改后命令提示符

如果想取消这个警告,在On OSX 10.11下,输入
```
cd /usr/local/share/
sudo chmod -R 755 zsh
sudo chown -R root:staff zsh
```
