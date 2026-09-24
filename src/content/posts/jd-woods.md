---
title: "python获取京东商品信息"
description: "!/usr/bin/env python"
pubDatetime: 2016-08-23T17:47:04
draft: false
tags: ["python"]
---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'http://list.jd.com/list.html?cat=9987%2C653%2C655&page=1'
req = requests.get(url)


soup = BeautifulSoup(req.text, "html.parser")
items = soup.select('li.gl-item')
# print len(items)
for item in items:
    sku = item.find('div')['data-sku']
    print sku,
    price_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(sku)
    price = requests.get(price_url).json()[0]['p']
    print price,
    nameinfo = item.find('div', class_="p-name").find('a')
    name = nameinfo['title']
    item_url = 'http:' + nameinfo['href']
    print name, item_url,
    commit = item.find('div', class_="p-commit").find('a')
    if commit:
        print commit.get_text()
```

其中价格是json获取的,

```
http://p.3.cn/prices/mgets?skuIds=J_ + skuId
```

还有几个获取获取json的方法:

```
http://c0.3.cn/stock?skuId=965009&cat=652,829,854&area=1_2812_51141_0&extraParam={"originid":"1"}

```

其中skuid是商品id,cat可以在商品网页里面获取到, area是地区码,
返回京东网页版商品的价格,当地商品是否有货.

```
http://item.m.jd.com/ware/thirdAddress.json?address=jd1356&wareId=965009&provinceId=1&cityId=2812&countryId=51141

```

其中wareID是商品id,area是地区码,返回京东手机版商品的价格,当地商品是否有货.

```
http://pe.3.cn/prices/pcpmgets?skuids=965012&origin=5&area=1_2812_51141

```

其中skuid是商品id,cat可以在商品网页里面获取到, area是地区码,
返回商品网页版价格和手机版微信版价格.