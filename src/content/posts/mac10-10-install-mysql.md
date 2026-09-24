---
title: "MAC10.10 下安装mySQL方法和设置"
description: "mac10.10下可以用brew安装mySQL,"
pubDatetime: 2015-09-18T19:12:20
draft: false
tags: ["- python"]
---

mac10.10下可以用brew安装mySQL,

```
brew install mysql
```
安装完成后, 正常可以用

```
mysql.server start
```
启动mysql.

但是我这次安装后提示,

```
mysql.server start
zsh: command not found: mysql.server
```
往前翻brew安装记录找到这个

```
The `brew link` step did not complete successfully
The formula built, but is not symlinked into /usr/local
Could not symlink share/man/man8/mysqld.8
/usr/local/share/man/man8 is not writable.

You can try again using:
  brew link mysql
```

然后根据'Could not symlink share/man/man8/mysqld.8
/usr/local/share/man/man8 is not writable.'搜到网上高手的解决办法,[高手](http://apple.stackexchange.com/questions/192227/make-files-in-usr-local-writable-for-homebrew)
就是运行一个命令

```
sudo chown -R `whoami` /usr/local
```

再启动mysql服务器就行了.
进入mysql的命令是:

```
mysql -uroot -p
```
初始登陆没有密码,直接按回车.
如果需要设置密码可以用以下命令.

```
/usr/local/bin/mysqladmin -u root password 'root'
```
分号里面root就是密码,可以根据需要改成自己的.

在mysql里面,如果输入错误命令后,再输入其他命令也无效了,输入"\c"后就可以重新返回命令行了.

还有就是windows下mysql安装完成后,需要设置环境变量后才能使用mysql命令.



在python中操作MySQL数据库,需要安装一个叫MySQL db的第三方库才行.

```
sudo pip install MySQL-python
```

