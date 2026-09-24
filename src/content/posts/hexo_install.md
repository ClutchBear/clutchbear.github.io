---
title: "hexo的安装步骤(已经失效)"
description: "1.设置git的SSH公钥"
pubDatetime: 2014-08-18T02:12:11
draft: false
tags: ["hexo"]
---

### 1.设置git的SSH公钥
- 打开终端,输入命令:
      
      ssh-keygen -t rsa -C "skywater@gmail.com"

-  继续输入命令:
-  
```
cd .SSH      
subl id_rsa.pub
```

拷贝SSH公钥到github账户的SSH keys里面.

- 输入命令:

```
git config --global user.email "skywater@gmail.com"
git config --global user.name "playbear"

```

### 2. 安装hexo环境,参考[官网](http://hexo.io/docs/)
- 安装node.js,打开终端,输入命令:

```    
      brew install node
```

- 安装nvm,命令:

```  
      curl https://raw.githubusercontent.com/creationix/nvm/v0.13.1/install.sh | bash
```
 
- 安装完成后重启终端,然后运行:

``` 
      nvm install 0.10
```
 
- 安装Hexo:

```  
      npm install -g hexo
```

- 初始化Hexo:

```mkdir playbear.github.io
cd playbear.github.io
hexo init
npm install
hexo g
hexo d
```

### 3. 常用hexo命令

```hexo n "new_file"(之后用mou编辑new_file.md)
hexo g
hexo d
```

### 4. hexo版本更新

```
    npm update -g
```
    
### 如果重装系统后的安装，在hexo g之后将备份的文件夹拷贝覆盖即可。