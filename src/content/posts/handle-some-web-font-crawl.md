---
title: "某8网站字体加密爬虫的处理方法"
description: "某8网站的一些数据在浏览器里面显示是正常的, 但是渲染前和渲染后的html源码都看不到字体, 渲染前看到的是16进制的4位字符, 渲染后看到的是一些方块."
pubDatetime: 2018-04-14T16:48:38
draft: false
tags: ["python"]
---

![](http://ww1.sinaimg.cn/large/7293e3b7gy1fqbijxv90kj217a0f4go4.jpg)

某8网站的一些数据在浏览器里面显示是正常的, 但是渲染前和渲染后的html源码都看不到字体, 渲染前看到的是16进制的4位字符, 渲染后看到的是一些方块.

搜索找到猫眼和汽车之家的解决方法, 某8网站比这些都复杂, 经过多次尝试得到解决.

首先在html源码里面找到woff字体的base4编码, 保存成"font.woff"字体文件, 用fontTools库将这个字体文件存储为"font.xml"文件.


![](http://ww1.sinaimg.cn/large/7293e3b7gy1fqbiw8ot0zj20pu0e3tbp.jpg)

然后在xml里面找到`TTGlyph`字段, 这个字段下面的 子字段都是用来画字符(包括中英文数字)的坐标. 同一个字符的坐标是一样的. 解析xml, 然后把这些坐标的属性字典按顺序都存到一个list里面, 然后序列化成json(加sort_keys=True参数)字符串. 用这个字符串当key, value是实际的字符, 存成一个constant_dict. 每次遇到新网页, 取出这个字符串, 然后根据字符串从constant_dict获取实际的字符.

每次获取font里面坐标list字符串的代码:

```python
# font_decryption.py
from fontTools.ttLib import TTFont
from lxml import etree
from io import BytesIO
import base64
import config
import os
import json
import pub.common.error as error

_xml_file_path = os.path.join(config.temp_file_path, "tongcheng58.xml")


def make_font_file(base64_string: str):
    bin_data = base64.decodebytes(base64_string.encode())
    return bin_data


def convert_font_to_xml(bin_data):
    font = TTFont(BytesIO(bin_data))
    font.saveXML(_xml_file_path)


def parse_xml():
    xml = etree.parse(_xml_file_path)
    root = xml.getroot()
    font_dict = {}
    all_data = root.xpath('//glyf/TTGlyph')
    for index, data in enumerate(all_data):
        font_key = data.attrib.get('name')[3:].lower()
        contour_list = []
        if index == 0:
            continue
        for contour in data:
            for pt in contour:
                contour_list.append(dict(pt.attrib))
        font_dict[font_key] = json.dumps(contour_list, sort_keys=True)
    return font_dict


def make_path():
    if not os.path.isdir(config.temp_file_path):
        os.makedirs(config.temp_file_path)


def get_font_dict(base64_string):
    try:
        make_path()
        bin_data = make_font_file(base64_string)
        convert_font_to_xml(bin_data)
        font_dict = parse_xml()
    except Exception as e:
        return (error.ERROR_UNKNOWN_RESUME_CONTENT, 'cannot_get_font, err=[{}]'.format(str(e))), None
    return None, font_dict


```

调用

```python
def decrypt_font(text, font_dict):
    decryption_text = ""
    for alpha in text:
        hex_alpha = alpha.encode('unicode_escape').decode()[2:]
        if hex_alpha in font_dict:
            item_text = decryption_font_dict.get(font_dict[hex_alpha])
            if item_text is None:
                _logger.error("op=[DecryptFont], err={}".format("decryption_font_dict_have_no_this_font"))
        else:
            item_text = alpha
        decryption_text += item_text
    return decryption_text


def parse(html: str, request: ParseRequest):
    user_info_dict = {}
    # print(html)
    base64_string = html.split("base64,")[1].split(')')[0].strip()
    err, font_dict = get_font_dict(base64_string)
    if err is not None:
        return err, None
    html = decrypt_font(html, font_dict)


if __name__ == "__main__":
    html = open(file_name, "r", encoding="utf-8").read()

    parse(html)
```


参考: 
[解析某电影和某招聘网站的web-font自定义字体](https://www.jianshu.com/p/5400bbc8b634)
[The ramblings of atbrask](http://www.atbrask.dk/?cat=11)
[python3 汉字转十六进制unicode](https://blog.csdn.net/xyq046463/article/details/58606657)


