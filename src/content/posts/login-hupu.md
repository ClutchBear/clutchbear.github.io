---
title: "python实现虎扑（hoopchina）自动登录和点亮"
description: "1:自动登录的代码"
pubDatetime: 2015-09-25T20:57:53
draft: false
tags: ["python"]
---

### 1:自动登录的代码

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import sys
from bs4 import BeautifulSoup

# 登录的头部信息
my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Host': 'passport.hupu.com',
    'Referer': 'http://passport.hupu.com/pc/login?project=bbs&from=pc',
    # 'Cookie ': "_cnzz_CV30020080=buzi_cookie%7Cdc42405e.675b.386f.8396.e1e33e42953b%7C-1; __gads=ID=15c18186521000ee:T=1443103052:S=ALNI_MZ84dig34sQNsPR7xvUlQlQ2H7pFg; _dacevid3=dc42405e.675b.386f.8396.e1e33e42953b; vjuids=8ee89313a.14fffb0fe83.0.32078b2e; vjlast=1443103834.1443103834.30; __dacewap=0xc8e6088248ba6cca; _HUPUSSOID=16672149-8304-4af5-8a1f-924337794477; _CLT=918ebe7bb324d8673460f7af1d701a5c; __dacevst=ce2e6fb5.b67f434d|1443110107591; CNZZDATA30020080=cnzz_eid%3D1429176686-1443106302-http%253A%252F%252Fbbs.hupu.com%252F%26ntime%3D1443106302; _cnzz_CV30020080=buzi_cookie%7Cdc42405e.675b.386f.8396.e1e33e42953b%7C-1"

}
s = requests.session()

# 用户名和密码的post信息
data = {
    'username': '用户名',
    'password': '密码',
}
time.sleep(2)
# 验证码
verifyimg_url = 'http://passport.hupu.com/pc/verifyimg'

f = open('img.jpg', 'wb')
imgreq = requests.get(verifyimg_url)
f.write(imgreq.content)
f.close()

# 验证码目前需要手动输入, 没有找到很精确辨识验证码的库.
verifyimg = raw_input('verifyimg code:\n').strip()
data['verifyCode'] = verifyimg


loginURL = 'http://passport.hupu.com/pc/login/member.action'
try:
    reqlogin = s.post(loginURL, data=data, headers=my_headers)
    print reqlogin.json()
    uid = str(reqlogin.json()['msg']['uid'])
    tag = str(reqlogin.json()['msg']['tag'])
except Exception as e:
    print e
    sys.exit(1)


url = 'http://passport.hupu.com/m/2/login/crossdomain?uid=' + \
    uid + '&freeLogin=true&tag=' + tag
# print url

req = s.get(url, headers=my_headers)
req = s.get('http://passport.hupu.com/pc/redirectJumpUrl', headers=my_headers)

cookies = reqlogin.cookies
time.sleep(2)

# 这个头部信息跟登录时候不一样,不能用那个的.
liangle_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                   'Host': 'bbs.hupu.com',
                   'Referer': 'http://bbs.hupu.com'
                   }

# 用小黑屋测试, 这个版块每有相应有权限的账号是没法参观的.
banzhu_URL = 'http://bbs.hupu.com/66'

banzhu_req = requests.get(banzhu_URL, headers=liangle_headers, cookies=cookies)
f = open('hupu.html', 'w')
f.write(banzhu_req.content)


banzhu_req.encoding = 'GB2312'
soup = BeautifulSoup(banzhu_req.text, "html.parser")


tiezi_lists = soup.find('table', id='pl').find_all('td', class_='p_title')
for tiezi in tiezi_lists:
    print " ".join(tiezi.get_text().split()).encode('utf-8')

```

![](http://ww3.sinaimg.cn/large/7293e3b7jw1ewf002rzcij20pw0fgwiv.jpg)

今天在v2ex上看到一个大神说,如果遇到验证码登录的网站,一般是现在chrome里面手动登陆一次,然后把cookie拷贝出来,放到头文件里面.
我试了一下果然可以,比需要手动输入方便多了.不过这种方法有个缺陷就是不能短时间内登录多次.


### 2: 自动点亮的代码

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import sys

# 登录的头部信息
my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Host': 'passport.hupu.com',
    'Referer': 'http://passport.hupu.com/pc/login?project=bbs&from=pc'
}

s = requests.session()

# 用户名和密码的post信息
data = {
    'username': '',
    'password': '',
}
time.sleep(2)
# 验证码
verifyimg_url = 'http://passport.hupu.com/pc/verifyimg'

f = open('img.jpg', 'wb')
imgreq = requests.get(verifyimg_url)
f.write(imgreq.content)
f.close()

# 验证码目前需要手动输入, 没有找到很精确辨识验证码的库.
verifyimg = raw_input('verifyimg code:\n').strip()
data['verifyCode'] = verifyimg


loginURL = 'http://passport.hupu.com/pc/login/member.action'
try:
    reqlogin = s.post(loginURL, data=data, headers=my_headers)
    print reqlogin.json()['code']
    # uid = str(reqlogin.json()['msg']['uid'])
    # tag = str(reqlogin.json()['msg']['tag'])
except Exception as e:
    print e
    sys.exit(1)


# url = 'http://passport.hupu.com/m/2/login/crossdomain?uid=' + \
#     uid + '&freeLogin=true&tag=' + tag
# # print url

# req = s.get(url, headers=my_headers)
# req = s.get('http://passport.hupu.com/pc/redirectJumpUrl', headers=my_headers)

cookies = reqlogin.cookies
time.sleep(2)

# 这个头部信息跟登录时候不一样,不能用那个的.
liangle_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                   'Host': 'bbs.hupu.com',
                   'Referer': 'http://bbs.hupu.com'
                   }

# authorid是被点亮那个回帖人的数字id, fid是板块数字id, pid此回帖人的第多少个帖子, tid是这个主贴的数字id
# 这些数据可以用bs4在网页中得到.
liangle_data = {
    'authorid': '16920413',
    'fid': '3913',
    'pid': '6103',
    'state': '1',
    'tid': '12615933',
    'token': '2e018203ea6a482c17847289989cf66f',
}
liangle_req = s.post('http://bbs.hupu.com/ajax/lights.ajax.php',
                     data=liangle_data, headers=liangle_headers, cookies=cookies)

print liangle_req.content

```

![](http://ww1.sinaimg.cn/large/7293e3b7jw1ewf070i4voj209r04cglz.jpg)
code是1表示点亮成功, num是被点亮的次数..


