---
title: "hexo主题Jacman配置文件的备份"
description: "主配置文件"
pubDatetime: 2015-09-06T17:52:19
draft: false
tags: ["hexo"]
---

主配置文件

```
# Hexo Configuration
## Docs: http://hexo.io/docs/configuration.html
## Source: https://github.com/hexojs/hexo/

# Site
title: 小信' Blog
subtitle:
description:
author: ClutchBear
language: zh-CN
timezone:

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://playbear.github.io
root: /
permalink: :year/:month/:day/:title/
permalink_defaults:

# Directory
source_dir: source
public_dir: public
tag_dir: tags
archive_dir: archives
category_dir: categories
code_dir: downloads/code
i18n_dir: :lang
skip_render:

# Writing
new_post_name: :title.md # File name of new posts
default_layout: post
titlecase: false # Transform title into titlecase
external_link: true # Open external links in new tab
filename_case: 0
render_drafts: false
post_asset_folder: false
relative_link: false
future: true
highlight:
  enable: true
  line_number: true
  auto_detect: true
  tab_replace:

# Category & Tag
default_category: uncategorized
category_map:
tag_map:

# Date / Time format
## Hexo uses Moment.js to parse and display date
## You can customize the date format as defined in
## http://momentjs.com/docs/#/displaying/format/
date_format: YYYY-MM-DD
time_format: HH:mm:ss

# Pagination
## Set per_page to 0 to disable pagination
per_page: 10
pagination_dir: page

# Extensions
## Plugins: http://hexo.io/plugins/
## Themes: http://hexo.io/themes/
theme: jacman
stylus:
  compress: true
# Deployment
## Docs: http://hexo.io/docs/deployment.html
deploy:
  type: git
  repository: https://github.com/playbear/playbear.github.io.git
  branch: master

index_generator:
  per_page: 5 ##首页默认10篇文章标题 如果值为0不分页

archive_generator:
    per_page: 10 ##归档页面默认10篇文章标题
    yearly: true  ##生成年视图
    monthly: true ##生成月视图

tag_generator:
    per_page: 10 ##标签分类页面默认10篇文章

category_generator:
    per_page: 10 ###分类页面默认10篇文章

feed:
    type: atom ##feed类型 atom或者rss2
    path: atom.xml ##feed路径
    limit: 20  ##feed文章最小数量
```

主题配置文件:

```
##### Menu
menu:
  Home: /
  Archives: /archives
  About: /about
## you can create `tags` and `categories` folders in `../source`.
## And create a `index.md` file in each of them.
## set `front-matter`as
## layout: tags (or categories)
## title: tags (or categories)
## ---

#### Widgets
widgets:
- category
- tag
- links
- douban
- rss
## provide seven widgets:category,tag,rss,archive,tagcloud,links,weibo,douban


#### RSS
rss: /atom.xml ## RSS address.

#### Image
imglogo:
  enable: false             ## display image logo true/false.
  src: #img/logo.png        ## `.svg` and `.png` are recommended,please put image into the theme folder `/jacman/source/img`.
favicon: img/favicon.ico   ## size:32px*32px,`.ico` is recommended,please put image into the theme folder `/jacman/source/img`.
apple_icon: #img/jacman.jpg ## size:114px*114px,please put image into the theme folder `/jacman/source/img`.
author_img: #img/author.jpg ## size:220px*220px.display author avatar picture.if don't want to display,please don't set this.
banner_img: #img/banner.jpg ## size:1920px*200px+. Banner Picture
### Theme Color
theme_color:
    theme: '#21272D'    ##the defaut theme color is blue

# 代码高亮主题
# available: default | night
highlight_theme: night

#### index post is expanding or not
index:
  expand: true           ## default is unexpanding,so you can only see the short description of each post.
  excerpt_link: Read More

close_aside: false  #close sidebar in post page if true
mathjax: false      #enable mathjax if true

### Creative Commons License Support, see http://creativecommons.org/
### you can choose: by , by-nc , by-nc-nd , by-nc-sa , by-nd , by-sa , zero
creative_commons: none

#### Author information
author:
  intro_line1:  #"Hello ,I'm Larry Page in Google."    ## your introduction on the bottom of the page
  intro_line2:  #"This is my blog,believe it or not."  ## the 2nd line
  weibo:      ## e.g. wuchong1014 or 2176287895 for http://weibo.com/2176287895
  weibo_verifier:  ## e.g. b3593ceb Your weibo-show widget verifier ,if you use weibo-show it is needed.
  tsina:      ## e.g. 2176287895  Your weibo ID,It will be used in share button.
  douban:     ## e.g. wuchong1014 or your id for https://www.douban.com/people/wuchong1014
  zhihu:      ## e.g. jark  for http://www.zhihu.com/people/jark
  email:      ## e.g. imjark@gmail.com
  twitter:    ## e.g. jarkwu for https://twitter.com/jarkwu
  github:     ## e.g. wuchong for https://github.com/wuchong
  facebook:   ## e.g. imjark for https://facebook.com/imjark
  linkedin:   ## e.g. wuchong1014 for https://www.linkedin.com/in/wuchong1014
  google_plus:    ## e.g. "111190881341800841449" for https://plus.google.com/u/0/111190881341800841449, the "" is needed!
  stackoverflow:  ## e.g. 3222790 for http://stackoverflow.com/users/3222790/jark
## if you set them, the corresponding  share button will show on the footer

#### Toc
toc:
  article: true   ## show contents in article.
  aside: true     ## show contents in aside.
## you can set both of the value to true of neither of them.
## if you don't want display contents in a specified post,you can modify `front-matter` and add `toc: false`.

#### Links
links:
  我的github: https://github.com/playbear
  我的知乎: http://www.zhihu.com/people/ClutchBear



#### Comment
duoshuo_shortname: clutchbear
disqus_shortname:     ## e.g. wuchong   your disqus short name.

#### Share button
jiathis:
  enable: false ## if you use jiathis as your share tool,the built-in share tool won't be display.
  id:    ## e.g. 1889330 your jiathis ID.
  tsina: ## e.g. 2176287895 Your weibo id,It will be used in share button.

#### Analytics
google_analytics:
  enable: false
  id:        ## e.g. UA-46321946-2 your google analytics ID.
  site:      ## e.g. wuchong.me your google analytics site or set the value as auto.
## You MUST upgrade to Universal Analytics first!
## https://developers.google.com/analytics/devguides/collection/upgrade/?hl=zh_CN
baidu_tongji:
  enable: false
  sitecode:  ## e.g. e6d1f421bbc9962127a50488f9ed37d1 your baidu tongji site code
cnzz_tongji:
  enable: false
  siteid:    ## e.g. 1253575964 your cnzz tongji site id

#### Miscellaneous
ShowCustomFont: false  ## you can change custom font in `variable.styl` and `font.styl` which in the theme folder `/jacman/source/css`.
fancybox: true        ## if you use gallery post or want use fancybox please set the value to true.
totop: true           ## if you want to scroll to top in every post set the value to true


#### Custom Search
google_cse:
  enable: false
  cx:   ## e.g. 018294693190868310296:abnhpuysycw your Custom Search ID.
## https://www.google.com/cse/
## To enable the custom search You must create a "search" folder in '/source' and a "index.md" file
## set the 'front-matter' as
## layout: search
## title: search
## ---
baidu_search:     ## http://zn.baidu.com/
  enable: false
  id:   ## e.g. "783281470518440642"  for your baidu search id
  site: http://zhannei.baidu.com/cse/search  ## your can change to your site instead of the default site

tinysou_search:     ## http://tinysou.com/
  enable: false
  id:  ## e.g. "4ac092ad8d749fdc6293" for your tiny search id

```

其中Rss需要按装插件:

```
npm install hexo-generator-feed@1 --save
```

参考: 

- [Jacman基于Pacman修改的Hexo主题](http://wsgzao.github.io/post/hexo-jacman/)

- [如何使用 Jacman 主题](http://wuchong.me/blog/2014/11/20/how-to-use-jacman/)