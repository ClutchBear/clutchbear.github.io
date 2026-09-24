---
title: "selenium所需要的chromedriver的安装方法"
description: "selenium是一个常用分析javascript动态网页的python第三方库."
pubDatetime: 2015-08-25T22:50:36
draft: false
tags: ["python"]
---

selenium是一个常用分析javascript动态网页的python第三方库.
在mac下安装很简单,

```
sudo pip install selenium
```

但是在运行示例代码时候会提示错误

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("http://google.com")
driver.quit()
```

```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home
```

根据提示是没有下载chromedriver并把它放到path里面.
搜索好久才找到详细的操作方法,
下载很简单,官方有下载地址.
mac下放到path的具体方法是:
- 打开finder,选择'前往'--'前往文件夹',然后弹出的窗口输入

```
/usr/bin
```

- 把解压缩好的chromedriver文件复制拷贝到bin文件夹.

再运行示例代码就弹出一个chrome窗口,表示运行成功.
