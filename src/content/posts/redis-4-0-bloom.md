---
title: "redis4.0以上版本开启bloomfilter插件的方法"
description: "安装redis4.0"
pubDatetime: 2018-11-28T15:23:43
draft: false
---

+ 安装redis4.0
    + 参考[CentOS7 下 Redis4 安装与配置教程（Redis开机启动）](https://ken.io/note/centos7-redis4-setup)
    + 安装基础依赖
    ```shell
    sudo yum install -y gcc gcc-c++ make jemalloc-devel epel-release
    ```
    + 下载最新版redis并解压到指定目录, 然后编译和安装
    ```sehl
    wget http://download.redis.io/releases/redis-4.0.2.tar.gz
    sudo tar -zvxf redis-4.0.2.tar.gz -C /usr/
    #进入目录
    cd /usr/redis/redis-4.0.2
    #编译&安装
    sudo make & make install
    
    sudo cp src/redis-cli /usr/local/bin/（將redis-cli拷貝到bin下，讓redis-cli指令可以在任意目錄下直接使用）
    ```
    + 加载配置文件启动redis-server
    ```
    cd /usr/redis/redis-4.0.11
    redis-server redis.conf
    ```

+ 安装Rebloom插件
    + 参考 [ReBloom – Bloom Filter Datatype for Redis](https://redislabs.com/blog/rebloom-bloom-filter-datatype-redis/)
    + 下载并编译
    ```
    $ git clone git://github.com/RedisLabsModules/rebloom
    $ cd rebloom
    $ make
    ```
    + 命令行加载rebloom插件,并且设定每个bloomfilter key的容量和错误率

    ```shell
    cd /usr/redis-4.0.11
    ./src/redis-server redis.conf --loadmodule /usr/rebloom/rebloom.so INITIAL_SIZE 1000000 ERROR_RATE 0.0001
    # 容量100万, 容错率万分之一, 占用空间是4m
    ```

+ 根据也无需求, 大于100万的bloomfilter key需要手动建立

  ```redis
  BF.RESERVE 2018_ccgp 0.0001 28000000
  Memory Usage 2018_ccgp
  # (integer) 67108997 64M
  ```

+ 设置开机启动. `crontab -e` 输入

  ```
  @reboot /usr/redis-5.0.0/src/redis-server /usr/redis-5.0.0/redis.conf --loadmodule /usr/rebloom/rebloom.so INITIAL_SIZE 1000000 ERROR_RATE 0.0001
  
  ```

+ 阿里云服务器或者vangrant的centos镜像不需要设置防火墙的开放端口.