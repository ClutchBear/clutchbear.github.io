---
title: "个人wsl设置"
description: "#### win10开启wsl并安装ubuntu"
pubDatetime: 2018-08-13T19:14:05
draft: false
tags: ["软件", "windows", "linux"]
---

+ #### win10开启wsl并安装ubuntu
    + win左下角搜索, 输入 `功能`, 找到 `启用或者关闭windows功能`
    + 找到`适用于Linux的Windows子功能`, 勾选
    + 重启电脑
    + 开始菜单MicroSoft Store, 搜索Ubuntu,找到ubuntu18.04安装
    + 开始菜单,启动ubuntu18.04
    + 等待一会后, 输入账号和密码
    + 更改源, 换成清华源, 参考[Ubuntu 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)


+ #### 系统更新
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```

+ #### 开启ssh
    + 安装
    ```
    sudo apt-get remove openssh-server
    sudo apt-get install openssh-server
    ```
    + 修改配置,
    ```
    sudo vim /etc/ssh/sshd_config
    ```
    ```
    Port 2222
    PasswordAuthentication yes
    ```
    + 启动
    ```
    sudo service ssh --full-restart
    ```

+ #### 安装mysql
    + 安装

    ```
    sudo apt-get update
    sudo apt-get install mysql-server
    ```
    + 配置, 这一项可能与下面添加root账号冲突.
    ```
    sudo service mysql start
    sudo mysql_secure_installation
    ```
    + 修改并添加root账户密码, 参考  [Ubuntu 18.04 安装记录 - 简书](https://www.jianshu.com/p/4ca115648939)

    ```
    sudo service mysql start
    sudo mysql -u root -p
    DROP USER 'root'@'localhost';
    CREATE USER 'root'@'%' IDENTIFIED BY 'root';
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
    FLUSH PRIVILEGES;
    ```

    + 开启远程访问, 参考, [mysql【一】：mysql在ubuntu上安装配置](https://zhuanlan.zhihu.com/p/28102425)
    修改 /etc/mysql/mysql.conf.d 下的mysqld.cnf，找到bind-address，把127.0.0.1 改为0.0.0.0

    + 开启服务

    ```
    sudo service mysql start
    ```

+ #### 安装redis
    + 安装
    ```
    sudo apt-get install redis-server
    ```
    + 配置远程访问
    ```
    sudo vim /etc/redis/redis.conf
    ```
    找到并注释掉下面一行, 或者把127.0.0.1改成0.0.0.0
    ```
    # bind 127.0.0.1
    ```
    + 开启服务
    ```
    sudo service redis-server start
    ```


+ #### 中文支持和字体
    ```
    sudo apt install language-pack-zh-hans
    sudo update-locale LANG=zh_CN.UTF-8
    sudo mkdir /usr/share/fonts
    sudo ln -s /mnt/c/Windows/Fonts /usr/share/fonts/windows
    sudo apt install fontconfig
    sudo fc-cache -fv
    ```

+ #### 安装zsh
    ```
    sudo apt-get install zsh
    sudo chsh -s $(which zsh)
    sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

    ```


+ #### 启动zsh,  ~/.bashrc
    ```
    # Launch Zsh
    if [ -t 1 ]; then
    exec zsh
    fi
    ```

+ #### 开机启动mysql redis 和ssh, 在~/.zshrc加入
    ```
    echo "检测开机启动项"
    if [ ! -e "/var/run/sshd.pid" ]; then
        echo '启动sshd'
        sudo service ssh start
    fi

    if test $( pgrep -f mysql | wc -l ) -lt 1
        then
        echo "启动mysql"
        sudo service mysql start
    fi

    if test $( pgrep -f redis | wc -l ) -lt 1
        then
        echo "启动redis"
        sudo service redis-server start
    fi
    ```


+ #### 启动显示 ~/.zshrc
    ```
    umask 0022
    export DISPLAY=localhost:0.0
    ```

+ #### 修改wsl里面查看windows磁盘文件的颜色1, 参考
    [在WSL环境下修改文件夹的颜色] (https://blog.royink.li/post/ls_color_in_wsl)
    [LS_COLORS](https://github.com/trapd00r/LS_COLORS/blob/master/README.markdown)

    ```
    dircolors -p > $HOME/.dircolors
    vim $HOME/.dircolors
    ```
    将
    STICKY_OTHER_WRITABLE 后面的数字改成02;32
    OTHER_WRITABLE 后面的数字改成01;34

    然后在`$HOME/.bashrc`(如果用zsh, `$HOME/.zshrc`)后面添加
    ```
    eval $(dircolors -b $HOME/.dircolors)
    ```

+ #### 修改wsl里面查看windows磁盘文件的颜色2, 参考[Quick rundown on my current setup on the Windows Subsystem for Linux.](https://github.com/lloydstubber/my-wsl-setup)
    ```
    #Change ls colours
    LS_COLORS="ow=01;36;40" && export LS_COLORS

    #make cd use the ls colours
    zstyle ':completion:*' list-colors "${(@s.:.)LS_COLORS}"
    autoload -Uz compinit
    compinit
    ```

+ #### 安装anaconda
    + 安装用清华的下载, [Anaconda | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)
    + 根据清华源的教程,设置源
    + 把path加入~/.zshrc

    ```
    export PATH=/home/xin/anaconda3/bin:$PATH
    ```

    + 更改权限

    ```
    sudo chown -R xin:xin /home/xin/anaconda3
    ```

    或者

    ```
    sudo chmod 777 -R /home/xin/anaconda3
    ```
    + 修改pip源

+ #### 安装jdk
    + 官网下载相应的jdk, 解压并拷贝到/opt目录下

    ```
    sudo cp jdk-8u171-linux-x64.tar.gz /opt
    sudo tar -zxvf jdk-8u171-linux-x64.tar.gz
    ```

    + 配置path, 打开~/.zshrc

    ```
    export JAVA_HOME=/opt/jdk1.8.0_171
    export PATH=$JAVA_HOME/bin:$PATH
    ```
+ #### 安装pycharm和idea
    官网下载, 拷贝到/opt目录里面解压缩,类似于jdk,
    运行
    ```
    sh /opt/pycharm-2018.2/bin/pycharm.sh &
    ```

+ #### 安装maven
    + 下载, 设置类似于jdk
    + 设置阿里云源

+ #### 安装多个wsl的linux, 修改默认版本
    开始菜单右键, 选择管理员模式打开powershell

    ```
    wslconfig /list # 列出安装的wsl不同linux版本
    wslconfig /s ubuntu-18.04 # 设置默认版本
    ```

+ #### 下载并安装vcxsrv, [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/),
  双击桌面xserver图标启动, 在Clipboard设置界面去掉 Clickboard勾选和Primary Selection. 这样可以屏蔽pycharm里面的select and copy(选择并拷贝).

  ![](https://ww3.sinaimg.cn/large/005YhI8igy1fu886ttxelj30if0dkt97)

  参考:
    + [copy on select seems to be enable...somewhere](https://sourceforge.net/p/vcxsrv/discussion/986201/thread/8dc32d4d/)
    + [Xming clipboard only works one way](https://superuser.com/questions/440128/xming-clipboard-only-works-one-way)