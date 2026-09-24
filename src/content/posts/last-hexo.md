---
title: "hexo最新版本的安装和数据恢复"
description: "最近用webstorm运行编辑好的html网页文件,总是显示无法打开,改localhost端口不行. 网上搜索了半天,发现很少人出现这种问题. 我怀疑是MAC osx系统以前装的东西跟webstorm"
pubDatetime: 2016-09-14T18:47:57
draft: false
tags: ["hexo"]
---

   最近用webstorm运行编辑好的html网页文件,总是显示无法打开,改localhost端口不行. 网上搜索了半天,发现很少人出现这种问题. 我怀疑是MAC osx系统以前装的东西跟webstorm冲突了. 只好重新安装我的黑苹果系统.

   安装一帆风顺,各种软件也安装配置正常. 但是安装和恢复hexo博客文件的时候遇到的问题, 按照以前的方法总是没法恢复成功.只好按hexo 官网的最新方法一步一步的重新安装了.

- 更新github的SSH key, 在终端输入命令一路回车生成SSH


 ```
  ssh-keygen -t rsa -C "your_email@example.com"

  cd ~/.ssh
  subl id_rsa.pub
 ```

  将sublime text里面的ssh密钥拷贝粘贴到github账户里面.


  ```
  ssh -T git@github.com

  ```

  验证ssh配置是否成功.

  ```
  git config --global user.name "用户名"
  git config --global user.email "邮箱地址"
  ```
  运行上面命令,可以避免每次hexo d提交的时候都输入账户密码



- 安装Node.js, hexo官网提供的是用命令安装的方式, 我发现还是去Node.js官网下载一个安装程序方便.
 [下载地址](https://nodejs.org/download/)

- 安装Hexo

```
npm install -g hexo-cli
```

- 初始化

```
hexo init mrxin.github.io
cd mrxin.github.io
npm install
```
完成后, 用 sublime text打开 _config.yml进行配置, 参考以前的配置文件, 需要注意的是, 最后deploy部分,以前type是github,现在改成了git.

```
deploy:
  type: git
  repository: https://github.com/MrXin/MrXin.github.io.git
  branch: master
```


这里还有一个重要的步骤是现在需要安装"hexo-deployer-git",方法:

```
npm install hexo-deployer-git --save
```

- 主题安装和配置:
   我喜欢的主题叫"Landscape-plus", 不知道是hexo的bug还是这个主题的不过,标签或者分类只能显示10篇文章的主题.
   我又挑了一款不好看的主题,叫maupassant,其[官网](https://github.com/tufu9441/maupassant-hexo).
   使用方法比较简单,按照官方步骤来就行了,最后在多说参数后填上:clutchbear即可.


- 最后将以前备份的md文件拷贝到_posts目录里面, 生成静态页面传到github上.

```
hexo g
hexo d
```

- Rss需要按装插件:

```
npm install hexo-generator-feed@1 --save
```