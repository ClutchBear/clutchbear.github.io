---
title: "重新安装MAC后必做的设置步骤"
description: "1: 运行RealtekRTL81xx-0_0_90.pkg,安装显卡驱动."
pubDatetime: 2014-08-15T23:13:55
draft: false
tags: ["黑苹果"]
---

1: 运行RealtekRTL81xx-0_0_90.pkg,安装显卡驱动.


2: 运行MultiBeast,选择Drivers—Audio—Realtek ALCXXX—Without DST—ALC887/888b Current v100302,安装声卡驱动.


3: 运行Appstore,升级到10.9.4.


4: 安装完成,重启. 


5: 点击左上苹果标志,选择打开System Preferences 

- 选择打开Network,选择Ethernet,自动获取ip变成绿色后,点击Apply

- 选择打开Mouse,去掉Scroll direction:natural的勾选,左侧两个速度拉到最大.

- 选择打开Desk&Screen Saver,选择Screen Saver,Start after选择Never

- 选择打开Energy Saver, Computer sleep和Display sleep都拉到Never

- 选择打开Keyboard,选择Modifier Keys, Option key改成Command, Command key改成Option.                                 选择Shortcuts—Input Sources, 勾选Select the previous input source 并将Spotlight的快捷键勾选去掉

- 选择打开Security&Privacy,点击左下角的锁标志,输入密码,点选Allow apps download from: Anywhere,                                                并将Put hard disks to sleep when possible和Wake for Ethernet network access的勾选去掉


6:  Mac终端添加 sublime text 3打开方式,打开终端输入命令:

```
        sudo ln -s "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl" /usr/bin/subl
```

7: 运行Appstore,下载并安装Xcode,运行然后点击agree.然后打开终端,输入命令,用来安装Command Line Tools(命令行工具):

```    
       xcode-select --install
```

8: 安装brew:

```   
       ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
9: 安装新版的iTerm2,命令行安装zsh

```
       curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
```    
   更新zsh的命令: 

```   
  upgrade_oh_my_zsh
```


