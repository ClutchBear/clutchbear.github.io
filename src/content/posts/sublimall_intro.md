---
title: "备份sublime text3个人配置的插件Sublimall(已经无效)"
description: "最近浏览v2ex网站发现了一款sublime text3的插件,名字叫sublimall,主要作用是备份sublime text3的个人配置.很适合我这样,经常折腾黑苹果,经常格式化硬盘的人."
pubDatetime: 2014-08-07T20:26:37
draft: false
tags: ["软件"]
---

最近浏览v2ex网站发现了一款sublime text3的插件,名字叫sublimall,主要作用是备份sublime text3的个人配置.很适合我这样,经常折腾黑苹果,经常格式化硬盘的人.
sublimall的网站是https://sublimall.org

- 点击绿色的sign up for free按钮,输入账号密码等信息后在自己邮箱里面收取验证邮件.
- 在自己[账号页面](https://sublimall.org/account/),左下角是email和API key信息
- 通过package control安装sublimall插件.
- sublimall会将配置和插件打包发送到这个网站上,用的压缩软件是7zip,因此需要安装7zip.

在终端输入:
    
    brew install p7zip


安装完成后,再输入:
    
    where is 7za

安装正常的话,会在终端显示:

    /usr/local/bin/7za
- 打开sublimall的setting-users
 ```{
    ////////////////////////////
    //// Sublimall settings ////
    ////////////////////////////
    "api_root_url": "http://sublimall.org",
    "api_upload_url": "/api/upload/",
    "api_retrieve_url": "/api/retrieve/",
    //上面几行不用管
    ///////////////////////
    //// User settings ////
    ///////////////////////
    "email": "roc100year@gmail.com",
    //这里输入自己注册sublimall网站的邮箱
    "api_key": "xxxxxxxxxxxxxxxxxxxx",
    //这里输入网站账户页面左下角api key给的一串数字和字母
    // Paths must be: "Packages/SublimeCodeIntel" or "Installed Packages/Sublimall"
    "ignore_packages": [],
    // Set true if you want to exclude packages managed by Package Control
    "exclude_from_package_control": false,
    // Set false if you don't want to encrypt your configuration
    "encrypt": true,
    // Upload timeout in seconds
    "http_upload_timeout": 120,
    // Download timeout in seconds
    "http_download_timeout": 120,
    // Path to 7zip executable, though Sublimall tries to find it out itself
    "7za_path": "/usr/local/bin/7za",
    //这里输入压缩软件所在的路径   
    // HTTP proxy to use for HTTP requests. Support for authentication
    // Examples: http://user:password@host:port or http://ip:port
    "http_proxy": ""
    }       
```    
- 打开preferences--package setting--sublimall--upload有一个压缩密码的空白行出现,输入压缩包的密码或者直接打回车.等待压缩和上传就好了.
- sublimall--retrieve 是取回备份的个人配置.