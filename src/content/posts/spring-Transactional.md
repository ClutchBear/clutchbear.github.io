---
title: "一次springboot事务bug的处理"
description: "工作需要将一条数据分别存入es(Elasticsearch)和mysql, 实现方法是: 在 springboot框架里面用@Transactional注解应用的方法保证事务."
pubDatetime: 2018-01-26T11:53:39
draft: false
tags: ["java"]
---

工作需要将一条数据分别存入es(Elasticsearch)和mysql, 实现方法是: 在 springboot框架里面用@Transactional注解应用的方法保证事务.

抄一条事务的解释:
`事务的作用就是为了保证用户的每一个操作都是可靠的，事务中的每一步操作都必须成功执行，只要有发生异常就回退到事务开始未进行操作的状态。`

今天发现一条数据存入了mysql, 但是没有存入es, 也就是事务失败了, es出现异常时候没有回退.
谷歌等各种搜索都说@Transactional处理事务是可以的. 
只能尝试和猜测各种写法的问题, 在一次把方法的private改成public后,发现idea没有提示, 难道是因为这个原因? 再次发送数据后,发现事务成功了.

用 `public 事务` 当关键字在谷歌上一搜发现果然是: 
`只有@Transactional 注解应用到public 方法，才能进行事务管理`


记录一下, 希望以后写事务的时候每次都记住这次大坑.

