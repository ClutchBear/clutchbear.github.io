---
title: "用python的selenium实现京东夺宝岛最后一秒自动下单"
description: "!/usr/bin/env python"
pubDatetime: 2016-08-18T16:51:09
draft: false
tags: ["python"]
---

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
import time
import datetime
import json
def get_endTime(paimaiID):
    endTimeURL = 'http://paimai.jd.com/services/currentList.action?paimaiIds={0}&callback=jQuery5542114'.format(
        paimaiID)
    req = requests.get(endTimeURL)
    data = json.loads(req.text[15: -2])
    return data['endTime'] - 900
def paimai(endTime, paimaiID, name, passWord, want_price):
    driver = webdriver.Firefox()
    driver.get(
        'https://passport.jd.com/new/login.aspx?ReturnUrl=http://paimai.jd.com/{0}'.format(paimaiID))
    email = driver.find_element_by_xpath('//input[@id="loginname"]')
    email.clear()
    email.send_keys(name)
    password = driver.find_element_by_xpath('//input[@id="nloginpwd"]')
    password.clear()
    password.send_keys(passWord)
    form = driver.find_element_by_xpath('//a[@id="loginsubmit"]')
    form.click()
    try:
        captcha = driver.find_element_by_xpath('//input[@id="authcode"]')
        if captcha:
            input_captcha = raw_input()
            captcha.send_keys(input_captcha)
        form.click()
    except:
        pass
    while 1:
        nowTime = int(time.time() * 1000)
        if nowTime == endTime:
            break
    current_price_url = 'http://paimai.jd.com/json/current/englishquery?paimaiId={0}&skuId=0&start=0&end=9'.format(
        paimaiID)
    current_price = json.loads(
        requests.get(current_price_url).content)['currentPrice']
    last_price = int(eval(current_price) + 1)
    print last_price
    if last_price > want_price:
        return
    price = driver.find_element_by_xpath('//input[@id="bidPrice"]')
    price.clear()
    price.send_keys(str(int(last_price)))
    botton = driver.find_element_by_xpath(
        '//div[@id="auctionStatus1"]/div[2]/a[1]')
    botton.click()
if __name__ == "__main__":
    # 夺宝岛商品id
    paimaiID = '11087928'
    # 登录名
    name = "xxxxxx"
    # 密码
    password = 'xxxxxx'
    # 预期心理价位
    want_price = 1000
    endTime = get_endTime(paimaiID)
    print endTime
    paimai(endTime, paimaiID, name, password, want_price)
```