---
title: "bash常用的命令和工具"
description: "工具"
pubDatetime: 2017-07-18T18:40:26
draft: false
---

+ 工具
    + 1 # thefuck
    用于输错命令后的自动纠正
        + 安装
        ```
        brew install thefuck
        ```
        + 使用
        ```
        pythn
        # zsh: command not found: pythonn
        fuck
        # python [enter/↑/↓/ctrl+c]
        ```
    + 2 # tldr
    用于bash命令的提示和示例
        + 安装
        ```
        brew install tldr
        ```
        + 使用

        ![](http://ww1.sinaimg.cn/large/4399c9a5gy1fho22cpfopj20oz0exad6.jpg)

    + 3 # mycli
    支持自动补全和语法高亮的mysql命令行工具
        + 安装
        ```
        brew install mycli
        ```

+ 常用命令

|命令|作用|
|:---:|:---:|
|history|查看命令行历史记录，再用 !n（n 是命令编号）就可以再次执行|
|ctrl-a|将光标移至行首|
|ctrl-e|将光标移至行尾|
|alt-b 和 alt-f|以单词为单位移动光标|
|pstree -p|进程树|
|ps -ef grep python| 显示python的进程|
|netstat -lntp 或 ss -plat|检查哪些进程在监听端口|
|alias|alias ll='ls -latr' 创建了一个新的命令别名 ll|
|ln -s |创建软连接|
|df -h|查看硬盘分区|
|exec $SHELL|重启shell|

+ 技巧
    + 删除大量文件的最快方法之一
    ```
    mkdir empty && rsync -r --delete empty/ some-dir && rmdir some-dir
    ```
