---
title: "terminus的安装和配置"
description: "下载git for windows并安装, 个人习惯安装时候不勾选git集成到右键菜单的的两个选项, 官方下载地址 Git for windows"
pubDatetime: 2018-11-20T13:31:35
draft: false
---

+ 下载git for windows并安装, 个人习惯安装时候不勾选git集成到右键菜单的的两个选项, 官方下载地址 [Git for windows](https://gitforwindows.org/)

+ 下载terminus并安装, 官方下载地址 [Terminus](https://eugeny.github.io/terminus/)

+ 设置, 单击左上角的齿轮

  + shell设置页, shell选择为Git-Bash

  + terminal设置页, 右键设置为粘贴, 勾选 软件打开时自动开启一个终端,  勾选 阻止自动执行复制的到终端的内容, 勾选 选择时自动复制

    ![](https://ww1.sinaimg.cn/large/007iUjdily1fxd5cjex8wj30p50j0ab8)

  + hotkeys设置页, 增加ctrl+v为粘贴快捷键. 这样, 最大的复合win的复制粘贴快捷键, 还是mac系统更合理, cmd+c是复制, cmd+v是粘贴. 与terminal的标准中断快捷键ctrl+c没有冲突

  + 新建~/.bashrc文件, 并加入下面的内容,

    ```
    # 按向上向下键自动匹配相应前缀的历史命令
    bind '"\e[A": history-search-backward'
    bind '"\e[B": history-search-forward'
    bind '"\e[C": forward-char'
    bind '"\e[D": backward-char'
    # 最大可能兼容win和linux的命令, 注意等号前后不能有空格
    alias ifconfig='ipconfig'
    alias ll='ls -lah'
    ```

    保存后, 重新打开terminus或者执行`source ~/.bashrc`即可

    参考链接: [Bash (简体中文)](https://wiki.archlinux.org/index.php/Bash_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))