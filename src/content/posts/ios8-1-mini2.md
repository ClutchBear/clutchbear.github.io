---
title: "ipad mini2 ios 8.1越狱和广告屏蔽"
description: "越狱注意事项"
pubDatetime: 2014-11-21T17:25:56
draft: false
tags: ["iOS"]
---

### 越狱注意事项

1: 用iTunes备份,如果应用不是在官方appstore下载的,iTunes是没法备份的,可以截图,越狱后在一个个安装

2:下载盘古越狱工具(或者太极越狱工具),如果越狱失败,可以先恢复ios固件,然后新系统重新越狱后,恢复备份.

3: 广告屏蔽,
- ios 8.1越狱后cydia里面一个源有广告,可以用ifile修改hosts,在后面添加

```
127.0.0.1 a.adorika.net
127.0.0.1 a.ad-sys.com
127.0.0.1 ads.glispa.com
127.0.0.1 c.gltrkk.net
127.0.0.1 hastrk3.com
```

参考:http://jailbreak.25pp.com/jiaocheng/yueyu_66924.html

- 普通app广告屏蔽也是在hosts里面添加字段

```
127.0.0.1 analytics.admob.com
127.0.0.1 api.admob.com
127.0.0.1 e.admob.com
127.0.0.1 c.admob.com
127.0.0.1 media.admob.com
127.0.0.1 mm.admob.com
127.0.0.1 mmv.admob.com
127.0.0.1 p.admob.com
127.0.0.1 r.admob.com
127.0.0.1 config.adsage.cn
127.0.0.1 config.adsage.com
127.0.0.1 config.mobisage.cn
127.0.0.1 config.minesage.com
127.0.0.1 config.soqugame.com
127.0.0.1 mobi.adsage.com
127.0.0.1 trc.adsage.com
127.0.0.1 mws.adsage.com
127.0.0.1 api.domob.cn
127.0.0.1 e.domob.cn
127.0.0.1 r.domob.cn
127.0.0.1 r.ow.domob.cn
127.0.0.1 s.domob.cn
127.0.0.1 sdl.domob.cn
127.0.0.1 api.immob.cn
127.0.0.1 adserving.immob.cn
127.0.0.1 c1.guomob.com
127.0.0.1 t3.guomob.com
127.0.0.1 umeng.co
127.0.0.1 umeng.com
127.0.0.1 alog.umeng.co
127.0.0.1 alog.umeng.com
127.0.0.1 au.umeng.co
127.0.0.1 au.umeng.com
127.0.0.1 oc.umeng.co
127.0.0.1 oc.umeng.com
127.0.0.1 ex.umengcloud.com
127.0.0.1 uyunad.com
127.0.0.1 www.uyunad.com
127.0.0.1 a-ad.adwo.com
127.0.0.1 ad-count.adwo.com
127.0.0.1 apiconfig.adwo.com
127.0.0.1 static.adwo.com
127.0.0.1 track.adwo.com
127.0.0.1 r3 adwo.com
127.0.0.1 googleads.g.doubleclick.net
127.0.0.1 google-analytics.com
127.0.0.1 ssl.google-analytics.com
127.0.0.1 static.googleadsserving.cn
127.0.0.1 mobads.baidu.com
127.0.0.1 api.adcome.cn
127.0.0.1 adbc.renren.com
127.0.0.1 mob.adwhirl.com
127.0.0.1 ios.ijinshan.com
127.0.0.1 push.icastlewar.com
```

参考:http://jailbreak.25pp.com/jiaocheng/yueyu_66924.html

### 非官方软件app的下载

1: 影梭即shadowsocks,在cydia里面搜索下载.主要作用是翻墙

2: GoodReader AVPlayerHD 欧陆字典 Calculator等软件在pp翻墙助手里面下载.

3: ifile的安装,首先在源里面添加 apt.178.com
   然后搜索ifile后下载安装.主要作用是修改系统文件比如hosts
   参考:http://bbs.25pp.com/forum.php?mod=viewthread&tid=273064

4: photo manager pro 在pp助手里面可以下载, 作用是 重命名图片,建立图片文件夹.