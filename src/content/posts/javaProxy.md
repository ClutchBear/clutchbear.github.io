---
title: "jdk动态代理和Cglib代理笔记"
description: "动态代理"
pubDatetime: 2018-03-19T16:36:53
draft: false
tags: ["java"]
---

## 动态代理

https://www.imooc.com/video/4704 这个视频的笔记

![](http://ww1.sinaimg.cn/large/7293e3b7ly1fph53nxdxdj21gk0mmgoj.jpg)

java动态代理类位于java.lang.reflect包下, 一般主要是设计到一下两个类:

+ Interface InvocationHandler: 该接口种仅仅定义了一个方法
`public object invoke(Object obj, Method method, Object[] args)` 
在实际使用时, 第一个参数obj一般指代理类, method只被代理的方法, args为该方法的参数数组.
这个抽象方法在代理类种动态实现.

+ Proxy: 该类是动态代理类
`Static Object newProxyInstance(ClassLoader loader, Class[] interfaces, InvocationHandler h)`, 返回代理类的一个实例, 返回后的代理类可以被代理类使用(可使用被代理类种在接口中声明过的方法)

+ 描述
所谓动态代理是这样一中class, 它在运行时生成的class(没有.java文件),
该class实现了被代理对象的一组interface, 使用动态代理类是, 必须实现InvocationHandler接口

+ 步骤
    + 1: 创建一个实现接口 InvocationHandler的类, 必须实现invoke方法, 在被代理类的方法前后添加要实现的功能
    + 2: 创建被代理类以及接口
    + 3: 调用Proxy类的静态方法, 创建一个代理类
    Static Object newProxyInstance(ClassLoader loader, Class[] interfaces, InvocationHandler h)
    + 通过代理调用方法
    


接口
```java 
//定义接口
public interface Moveable {
    void movie() throws InterruptedException;
}
```

被代理的类
```java
public class Car implements Moveable {
    @Override
    public void movie() throws InterruptedException {
        TimeUnit.SECONDS.sleep(new Random().nextInt(5));

    }
}
```

动态代理
```java
//实现InvocationHandler接口, 复写invoke, 在被代理对象方法前后增加新的功能, 返回被代理对象的返回值
public class TimeHandler implements InvocationHandler{
    private Object target;

    public TimeHandler(Object target) {
        this.target = target;
    }

    /**
     *
     * @param proxy 被代理的对象
     * @param method 被代理对象的方法
     * @param args 被代理对象方法的参数
     * @return 被代理Object对象 方法的返回值
     * @throws Throwable
     */
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {

        long start = System.currentTimeMillis();
        System.out.println("汽车开始行驶");
        method.invoke(target);
        long end = System.currentTimeMillis();
        System.out.println("汽车终止行驶!");
        System.out.println((end - start)/ 1000.0);
        return null;
    }
}
```

代理类的测试
```java
public class Test {
    /**
     * jdk动态代理测试类
     */
    public static void main(String[] args) throws InterruptedException {
        Car car = new Car();
        InvocationHandler handler = new TimeHandler(car);
        Class<?> carClass = car.getClass();

        /**
         * loader: 类加载器
         * interfaces 类实现的接口
         * h InvocationHandler
         */
        Moveable moveable = (Moveable) Proxy.newProxyInstance(
                carClass.getClassLoader(),
                carClass.getInterfaces(),
                handler);
        moveable.movie();

    }
}
```

## Cglib代理
也叫做子类代理. 用被代理类的子类对象增加功能来实现的.

被代理类
```java
public class Train {
    public void move(){
        System.out.println("火车行驶中...");
    }
}
```

创建cglib代理类
```java
import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

import java.lang.reflect.Method;

public class CglibProxy implements MethodInterceptor {
    private Enhancer enhancer = new Enhancer();

    public Object getProxy(Class cls) {
        // 设置创建子类(代理类)的类(被代理的类)
        enhancer.setSuperclass(cls);
        enhancer.setCallback(this);
        return enhancer.create();
    }

    /**
     * cglib通过继承父类方法来实现代理
     * 拦截所有目标类方法的调用
     *
     * @param o           目标类的实例
     * @param method      目标方法的反射对象
     * @param objects     目标方法的参数
     * @param methodProxy 代理类的实例
     * @return 目标类方法的返回值
     */
    @Override
    public Object intercept(Object o, Method method, Object[] objects, MethodProxy methodProxy)
            throws Throwable {
        System.out.println("日志开始记录");
        // 代理类调用父类的方法
        methodProxy.invokeSuper(o, objects);
        System.out.println("日志结束...");
        return null;
    }
}
```

测试cglib代理
```java
public class Client {
    public static void main(String[] args) {
        CglibProxy proxy = new CglibProxy();
        Train train = (Train) proxy.getProxy(Train.class);
        train.move();
    }
}
```

输入结果, 在被代理类功能前后都增加了新功能.
```
日志开始记录
火车行驶中...
日志结束...
```






