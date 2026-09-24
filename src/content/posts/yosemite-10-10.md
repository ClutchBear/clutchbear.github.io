---
title: "YOSEMITE 10.10 安装记录"
description: "2015年9月20日更新, 更新完10.10.5补丁后再安装声卡驱动(MultiBeast 7.3.0)才有效."
pubDatetime: 2014-11-08T00:06:21
draft: false
tags: ["黑苹果"]
---

### 2015年9月20日更新, 更新完10.10.5补丁后再安装声卡驱动(MultiBeast 7.3.0)才有效.


Yosemite 10.10出来后,跟风安装了,但是总有各种各样的问题,比如键盘无效 声卡没法驱动等等,与10.9.5有很多不同的地方.
折腾了好几天终于算是弄好了.
自己将步骤记录一下,以后备用:

## 1. 下载

- 下载pcbeta论坛’七月流火’大神的u盘版yosemite([pcbeta链接](http://bbs.pcbeta.com/viewthread-1552254-1-1.html)),由于只提供了1021版本,需要自己转换成没有重装bug的1024版本.

- 在windows下运行smartvs.exe,打开1021 to 1024.svf,然后根据提示找到”黑苹果安装U盘.20141021.七月流火.10.10.dmg”(md5:82D2EBAC6FA794FD3147D0BD40371FCD),然后提取出”黑苹果安装U盘.20141024.七月流火.10.10.dmg”(md5:27F84982358D7C06AE2339EA950D7E6B)

- 运行transmac.exe, 将七月流火的yosemite恢复到u盘上.

## 2.分区

- 用10.9.3的u盘启动电脑,进入winpe,讲要安装黑苹果的硬盘分成两个分区,第一个分区大小为1g,剩下是第二个盘.
- 运行diskgenius, 用分区克隆工具将u盘的boot分区克隆到第一个分区.
更换成10.10的安装u盘

## 3. 安装

- 重启电脑, 按del进入bios,硬盘模式改成achi,关闭vt-x
选择u盘启动, 进入启动界面选择clover,然后选择安装10.10,
图形界面出现后,选择’硬盘工具’,将前面分好的第二个分区格式化成’MAC OS 扩展(日志)’
- 开始安装10.10,一步一步next到底.
安装完成,重启,u盘启动,选择clover,选择硬盘mac启动.之后输入用户名密码,不要选择联网.

## 4. 驱动和设置

- 运行MultiBeast,选择drivers-network-realtek- realtekRTLxx v0.0.90,然后build,重启
下载cover2953的Mac 版 MBR+GPT 分区专用 pkg 安装包([下载链接](http://bbs.pcbeta.com/viewthread-1516502-1-1.html)),解压缩安装到硬盘的启动盘中.将10.10安装u盘的efi拷贝到第一个分区中替换原来的.这样就可以硬盘直接启动clover了.
- 下载运行Clover Configurator,打开第一个分区也就是启动分区中的config.plist,
- 选择Boot选项,然后勾选kext-dev-mode=1,
- 选择Devices选择,在Audio处填入1,保存
- 重新运行MultiBeast,选择drivers-atheros,然后勾选ALC887/888b current v100302 和 optional efi installed bootloader support,选择build,重启
- 系统偏好设置—声音—输出,选择内置扬声器.这样就有声音了.
声卡驱动步骤主要参考pcbeta论坛的帖子,[请参考链接](http://bbs.pcbeta.com/viewthread-1551705-1-1.html)

## 5. 其他类似以前写的.