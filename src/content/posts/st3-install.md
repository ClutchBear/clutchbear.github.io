---
title: "sublime text3 安装和设置"
description: "Sublime Text3 是我最常用的python编辑器,"
pubDatetime: 2015-03-05T15:16:16
draft: false
tags: ["软件"]
---

Sublime Text3 是我最常用的python编辑器,

1: 安装Package Control,View--Show console,输入下面数据后回车:(参考来源: https://packagecontrol.io/installation#st3)
     
        import urllib.request,os,hashlib; h = 'eb2297e1a458f27d836c04bb0cbaf282' + 'd0e7a3098092775ccb37ca9d6b2e4b7d'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
 
2: 安装插件,快捷键CMD + Shift + P,输入Install Package.卸载插件时输入: Remove Package
   
   常用的插件包括:
   
   AutoPeP8: 自动格式化python代码
     
   SublimeCodeIntel: python语法提示和自动完成
   
   ConvertToUTF8: 顾名思义转换成UTF8编码格式
   
   SideBarEnhancements: 侧边栏增强
 
   SublimeTmpl: 新建文件模板

3: 修改快捷键,打开Perferences--Key Buildings User将这个内容复制进去保存
```     
      { "keys": ["f5"], "command": "build" },
```
 这样按F5就是编译了,当然以前的CMD + B(windows系统下面是Ctrl + B)也是可以的.


4: 其他参考以前写的 http://playbear.github.io/2015/09/02/sublime-backup/ 和 http://playbear.github.io/2014/08/13/sublime-plugin-sublime-tmpl/  等