---
title: "黑苹果MAC os 10.11新安装后的设置和软件安装"
description: "新安装好的系统,需要安装软件和配置,将这些步骤记录下来,以后需要的适合查询."
pubDatetime: 2016-10-22T00:20:01
draft: false
tags: ["黑苹果"]
---

新安装好的系统,需要安装软件和配置,将这些步骤记录下来,以后需要的适合查询.

- 屏蔽”Thunderbolt 1.2 固件更新”
黑苹果在APP store更新界面一直有”Thunderbolt 1.2 固件更新”提醒, 在iterm2运行”

```
softwareupdate --ignore ThunderboltFirmwareUpdate1.2
```

- 安装Xcode Command Line Tools
也就是命令行工具,大概需要10分钟.

```
xcode-select --install
```

- 安装zsh, 命令参考[github](https://github.com/robbyrussell/oh-my-zsh)

```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

```

然后配置iterm2, 去掉General的两个Confirm的勾选, 以防iterm2阻止MAC的关机. Profiles-Text两个字号选择18, 字体选择Hack

修改主题和提示符: `subl ~/.zshrc`, 第10行的主题改成`half-life`,
然后提示符修改代码加入最后,

```
PROMPT=$'%{$purple%}%n%{$reset_color%} in %{$limegreen%}%~%{$reset_color%}$(ruby_prompt_info " with%{$fg[red]%} " v g "%{$reset_color%}")$vcs_info_msg_0_%{$orange%}%{$reset_color%} at %{$hotpink%}%* %{$orange%}
λ%{$reset_color%} '
```


- 安装brew

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

```

- 用brew分别安装各种工具,
比如tree, git, openssl, mongodb等.
tree是mac下生成目录树的工具,

```
brew install tree
brew install git
brew install openssl
brew python3
brew mysql
```

- 安装pip

```
sudo easy_install pip
```

在墙内为了更快的安装各种库, 需要更换pip的安装源,自己建立 “~/.pip/pip.conf”文件

```
mkdir ~/.pip/
cd ~/.pip/
subl pip.conf

```
将

```
[global]
trusted-host = pypi.douban.com
index-url = http://pypi.douban.com/simple/

```
拷贝进去

- 用pip安装各种库,
比如requests, beautifulsoup4, mysql-pyhton, virtualenv等.
