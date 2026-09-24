---
title: "vagrant的安装和设置"
description: "下载和安装"
pubDatetime: 2019-01-08T10:08:20
draft: false
---

+ 下载和安装

  + [vagrant官方网址](https://www.vagrantup.com/downloads.html) , 下载后双击安装
  + [VirtualBox官方网址](https://www.virtualbox.org/wiki/Downloads) , 下载后双击安装

+ vagrant 官方box的下载方法:

  + 参考 [vagrant 的 box 哪里下？镜像在哪儿找？教你在 vagrant 官网下载各种最新. box 资源](https://my.oschina.net/cxgphper/blog/1940644)

  + 进入[Vagrant box](https://app.vagrantup.com/centos/boxes/7)找到centos box镜像最新的版本号

  + 拼接下载链接

    ```
    https://app.vagrantup.com/centos/boxes/7/versions/{版本号}/providers/virtualbox.box
    ```

+ 初始化vagrant

  ```
  mkdir centos && cd centos # 新建centos目录
  vagrant box add centos_base d:/vagrant_images/vagrant-centos-7.2.box # 添加镜像到vagrant
  vagrant init centos_base # 初始化配置
  ```

+ 修改vagrant配置

  + 单台虚拟机的配置, 参考: [Vagrant 实战](https://www.jianshu.com/p/2724cd5f28e5)

  ```
  #Vagrant的三种网络配置
    #端口映射(Forwarded port) 把宿主计算机的端口映射到虚拟机的某一个端口上，访问宿主计算机端口时，请求实际是被转发到虚拟机上指定端口的。
    #例如下面的配置，将访问宿主计算机8080端口的请求都转发到虚拟机的80端口上进行处理       #访问localhost:8080,对应访问虚拟机的80端口
    #优点：容易实现外网访问虚拟机
    #缺点：端口比较多时，配置麻烦；不支持在宿主机器上使用小于1024的端口来转发。比如：不能使用SSL的443端口来进行https连接。
    config.vm.network "forwarded_port", guest: 80, host: 8080
    
    #私有网络（Private network） ，只有主机可以访问虚拟机，如果多个虚拟机设定在同一个网段也可以互相访问，当然虚拟机是可以访问外部网络的。
    #优点：安全，只有自己能访问
    #缺点：因为私有的原因，所以团队成员其他人不能和你协作
    config.vm.network "private_network", ip: "192.168.33.10"
    
    #公有网络（Public network） ，虚拟机享受实体机器一样的待遇，一样的网络配置，vagrant1.3版本之后也可以设定静态IP。
    #优点：方便团队协作，别人可以访问你的虚拟机
    #缺点：需要有网络，有路由器分配IP
    config.vm.network "public_network", ip: "192.168.12.253"
    
    
    #设置文件同步，如下 ../work 是本地目录， /vagrant_data是虚拟机文件目录
    #两个目录设置为同步，这样就可以直接本地编辑文件，使用虚拟机配置的软件环境了。
    config.vm.synced_folder "../work", "/vagrant_data",
    :mount_options => ["dmode=775","fmode=664"]
    
    # 设置虚拟机的内存
    config.vm.provider "virtualbox" do |vb|
       vb.memory = "4096"
    end
    
  
  ```

  + 多台虚拟机的配置, 参考: [vagrant系列二：vagrant的配置文件vagrantfile详解](https://blog.csdn.net/hel12he/article/details/51089774)

  ```
  Vagrant.configure("2") do |config|
    config.vm.define :web do |web|
      web.vm.provider "virtualbox" do |v|
            v.customize ["modifyvm", :id, "--name", "web", "--memory", "512"]
      end
      web.vm.box = "CentOs7"
      web.vm.hostname = "web"
      web.vm.network :private_network, ip: "192.168.33.10"
    end
  
    config.vm.define :redis do |redis|
      redis.vm.provider "virtualbox" do |v|
            v.customize ["modifyvm", :id, "--name", "redis", "--memory", "512"]
      end
      redis.vm.box = "CentOs7"
      redis.vm.hostname = "redis"
      redis.vm.network :private_network, ip: "192.168.33.11"
    end
  end
  ```

+ v1811.02版本centos box需要修改sshd的设置, 改成ssh允许用户名和密码登录

  + 参考 [CentOS SSH 密钥登陆改为密码登陆](https://blog.csdn.net/zjqlovell/article/details/79399265)

  + 用`vagrant ssh`命令进入centos

  + 打开/etc/ssh/sshd_config

    ```
    vim /etc/ssh/sshd_config
    PermitRootLogin yes 删除前面的 #注释
    PasswordAuthentication no 改成 PasswordAuthentication yes
    ```

  + 重启sshd

    ```
    service sshd restart
    ```

+ 启动和ssh链接, vagrant镜像有两个user,  root和vagrant, 密码都是: vagrant, 开启xshell, 填入ip(192.168.33.10), 用户root和密码vagrant

  ```
  vagrant up  # 启动虚拟机
  vagrant halt  # 关闭虚拟机
  vagrant reload  # 重启虚拟机
  vagrant ssh  # SSH 至虚拟机
  vagrant status  # 查看虚拟机运行状态
  vagrant destroy  # 销毁当前虚拟机
  ```

+ 打包

  ```
  vagrant package --vagrantfile Vagrantfile #将配置文件一块打包
  vagrant package --output centos.box # 要打包成的box名称，不会自动添加.box后缀，要手动加.默认值package.box
  ```

+ pycharm 的python项目用vagrant虚拟环境的python作为解释器, 参考 [Pycharm 解释器配置](https://pengzhendong.cn/2018/05/26/Pycharm-python-interpreter/)

+ pycharm 配置terminal为vagrant虚拟机环境,



  + 开启ssh terminal, 勾选为current vagrant, 编码设置为utf-8

  ![](https://ww1.sinaimg.cn/large/005YhI8igy1fx8kl17blhj311n0ix75n)



  + tools选择start ssh sessions

    ![](https://ww1.sinaimg.cn/large/005YhI8igy1fx8kmt5iq4j309w0atmxp)





  + 在terminal中就可以直接使用远程terminal

    ![](https://ww1.sinaimg.cn/large/005YhI8igy1fx8kog1jsoj30rv0c3t9l)

+ mysql连接速度慢的解决方法

  + 参考: [连接Vagrant中mysql变慢了是什么原因](https://talk.ninghao.net/t/lian-jie-vagrantzhong-mysqlbian-man-liao-shi-shi-yao-yuan-yin/3521)

  + 打开mysql的配置文件`/etc/my.conf`,  增加`skip-name-resolve`参数

    ```
    [mysqld]
    skip-name-resolve
    ```

  + 重启mysql

    ```
    service mysqld restart
    ```


+ ssh 连接速度慢的解决方法

  + 编辑 /etc/ssh/sshd_config

    ```
    UseDNS no, 找到此行取消注释,并且把yes改成no
    ```

  + 重启ssh

    ```
    service sshd restart
    ```

+ 出现文件夹同步失败的解决方法

  + 参考 [vagrant up报错：unable to mount VirtualBox shared folders](https://zj-john.github.io/tips/cjhpvs7vl000r64f01suposfq.html)

  + ```
    vagrant plugin install vagrant-winnfsd
    vagrant plugin install vagrant-vbguest
    ```

