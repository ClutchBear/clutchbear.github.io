---
title: "python模拟登陆京东"
description: "首次登录需要手动输入验证码"
pubDatetime: 2016-08-15T15:41:21
draft: false
tags: ["python"]
---

首次登录需要手动输入验证码

```

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-11 19:10:06
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
import time
import os
import json

url = 'https://passport.jd.com/uc/login'
s = requests.session()
data = {
    'chkRememberMe': 'on',
    'loginname': 'xxxx',
    'loginpwd': 'xxxxx',
    'machineCpu': '',
    'machineDisk': '',
    'machineNet': '',
    'nloginpwd': 'xxxxxx'
}
if os.path.exists('jdcookie'):
    with open('jdcookie') as f:
        cookie = json.load(f)
    s.cookies.update(cookie)

else:
    req = s.get(url)

    soup = BeautifulSoup(req.text, "html.parser")
    items = soup.select('form#formlogin > input')
    uuid = items[0].get('value').encode('utf-8')
    data['uuid'] = uuid

    input_name = items[-1].get('name').encode('utf-8')
    input_value = items[-1].get('value').encode('utf-8')
    data[input_name] = input_value
    verify_url = soup.find('img', id='JD_Verification1')[
        'src2'] + '&yys=' + str(int(time.time() * 1000))
    print verify_url
    img = s.get(verify_url)
    f = open('image.jpg', 'wb')
    f.write(img.content)
    f.close()
    print 'input code:'
    authcode = raw_input()
    data['authcode'] = authcode
    print data
    postreq = s.post(
        'https://passport.jd.com/uc/loginService?version=2015', data=data)
    postreq.encoding = 'gbk'
    print postreq.text
    if 'success' in postreq.text:
        with open('jdcookie', 'w') as f:
            json.dump(s.cookies.get_dict(), f)
```