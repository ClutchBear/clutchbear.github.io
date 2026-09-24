---
title: "mac 安装和设置java maven"
description: "### 1 安装和设置java"
pubDatetime: 2017-11-20T18:38:36
draft: false
---

+ ### 1 安装和设置java
    + 1: 搜索官方下载jdk相应版本, 然后双击安装
    + 2: iterm运行
    ```
    /usr/libexec/java_home -V
    ```
    出现类似
    ```
    /Library/Java/JavaVirtualMachines/jdk1.8.0_151.jdk/Contents/Home
    ```
    说明安装成功

    + 3: 打开zsh, `vim ~/.zshrc` 最后面添加
    ```
    export JAVA_HOME=$(/usr/libexec/java_home)
    ```
    保存
    4: 重新加载zshrc, `source ~/.zshrc`, 输入`echo $JAVA_HOME`
    出现
    ```
    /Library/Java/JavaVirtualMachines/jdk1.8.0_151.jdk/Contents/Home
    ```
    说明安装成功

+ ### 2 安装和设置maven
    + 用brew安装maven `brew install maven`
    + item 运行 `mvn -v`
    出现这样结果说明安装成功
    ```
    Maven home: /usr/local/Cellar/maven/3.5.2/libexec
    Java version: 1.8.0_151, vendor: Oracle Corporation
    Java home: /Library/Java/JavaVirtualMachines/jdk1.8.0_151.jdk/Contents/Home/jre
    Default locale: zh_CN, platform encoding: UTF-8
    OS name: "mac os x", version: "10.12.6", arch: "x86_64", family: "mac"
    ```
    + 改成阿里源, 参考[来源](http://blog.csdn.net/liangyihuai/article/details/57406870) `/usr/local/Cellar/maven/3.5.2/libexec/conf` 这个目录下找到setting.xml文件, 打开.
    在`mirrors`字段下填入
    ```
    <mirror>
            <id>alimaven</id>
            <name>aliyun maven</name>
            <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
            <mirrorOf>central</mirrorOf>
      </mirror>
    ```
    + 修改idea的默认maven, 参考[来源1](http://www.jianshu.com/p/43b65774cc15), [来源2](http://blog.csdn.net/cherrycheng_/article/details/51729272)

    ![](http://ww1.sinaimg.cn/large/7293e3b7gy1flopsvyxqoj20s008oq4k.jpg)
    
    ![](http://ww1.sinaimg.cn/large/7293e3b7gy1fp8xo07akqj20ri05j3z1.jpg)

