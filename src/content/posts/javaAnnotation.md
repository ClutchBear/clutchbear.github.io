---
title: "java注解笔记"
description: "1. 注解的作用"
pubDatetime: 2018-03-19T14:30:46
draft: false
---

1. 注解的作用
    + 读懂别人写的代码, 特别是框架的相关代码
    + 让编程更加简洁, 代码更清晰
    + 会写自定义注解 提升自己的能力
2. 定义:
    java提供了一中原程序中的元素关联任何信息和任何元数据的途径和方法.

3. 常见注解
    + jdk自带
        + @Override   表示当前方法覆盖了父类的方法
        + @Deprecation   表示方法已经过时,方法上有横线，使用时会有警告
        + @SuppviseWarnings 表示关闭一些警告信息(通知java编译器忽略特定的编译警告), 比如使用过期的(即用@Deprecation标识的方法)时, 会有编译器警告, 加上这个注解可以消除这个警告.
    + Spring 注解
        + @Autowired spring 自动装配
        + @Qualifier(“JavaBea”) 配合 @Autowired 实现自动装配
        + @Resource(name="JavaBean") spring 自动装配, 不写参数直接装配同类型的类
        + @PostConstruct 类初始化的方法
        + @PreDestroy 类销毁的方法
        + @Component 表名类为 JavaBean
        + @Scope(“prototype” ) 指定Bean的作用范围, prototype为每次都重新实例化
        + @Repository 与 @Component 作用相同, 常用于数据持久层
        + @Service 与 @Component 作用相同, 常用于业务逻辑层
        + @Controller 与 @Component 作用相同, 常用于控制表现层 
    + Mybatis 注解
        + @Select
        + @Option
     
    + Autowired 举例
    
        1. 用类实习创建类的实例
        
            ```java
            public class UerManagerImpl implements UserManager{
                private UserDao userDao;
                public void setUserDao(UserDao userDao){
                    this.userDao = userDao;
                }
            }
            
            ```
        ------
        2. 用配置文件实现创建类实例
            ```java
            <bean id="UerManagerImpl" class="xxx.service.UserManager">
                <property name ="userDao" ref="userDao" />
            </bean>
            <bean id="userDao" class="xxx.UerManagerImpl"
                <property name ="sessionFactory" ref="mySessionFactory" />
            </bean>
            ```
        ------
        3. 用注解实现类实例的创建
    
            ```java
            public class UerManagerImpl implements UserManager{
                @Autowired
                private UserDao userDao;
            }
            ```
             
+ 注解分类
    + 按照运行机制分类
        + 源码注解 : 注解只在源码里面存在, 编译生成.class文件时就不存在了. (这里的源码指自己编写的java代码.)
        + 编译时注解: 注解在源码和.class文件中存在, jdk自带的3个注解都属于编译时注解
        + 运行时注解: 在运行阶段还起作用, 甚至影响运行逻辑的注解. spring的  @Autowired 属于运行时注解
    + 注解来源:
        + jdk注解
        + 第三方注解
        + 自定义注解
    + 元注解:
        + 注解的注解  
+ 自定义注解

    1. 注解定义
        ```
        import java.lang.annotation.Documented;
        import java.lang.annotation.ElementType;
        import java.lang.annotation.Inherited;
        import java.lang.annotation.Retention;
        import java.lang.annotation.RetentionPolicy;
        import java.lang.annotation.Target;
        
        /**
         * 下面4个被称为元注解,
         */
        
        // @Target: 注解的作用域, 包括(CONSTRUCTOR(构造方法), FIELD(类属性), LOCAL_VARIABLE(局部变量),
        // METHOD(方法), PACKAGE(包), PARAMETER(参数), TYPE(类, 接口))
        
        @Target({ElementType.METHOD, ElementType.TYPE})
        
        // @Retention: 注解的生命周期, 包括(SOURCE, CLASS, RUNTIME)
        // SOURCE: 只在源码种显示, 编译时丢弃,
        // CLASS 编译时会记录到class中, 运行时忽略
        // RUNTIME 运行时存在, 可以通过反射读取
        @Retention(RetentionPolicy.RUNTIME)
        
        // @Inherited 允许子类继承父类的类注解, 父类的方法注解无法继承
        // 注意, 注解定义到接口上, 实现的时候解析是无效的
        @Inherited
        
        // @Documented 生成javadoc时候回包含注解, 属于标识注解
        @Documented
        
        //使用 @interface 关键字定义注解
        public @interface Description {
            /**
             * 成员类型是受限的, 合法的类型包括原始类型及String, Class, Annotation, Enumeration
             *
             * 如果注解只有一个成员, 则成员名必须取名为value(), 在使用时可以忽略程一鸣和赋值号(=)
             *
             * 注解类可以没有成员, 没有成员的注解称为标识注解
             */
        
        
            //成员以无参无异常方式声明,  成员就是注解里面元素定义的名词
            String desc();
        
            String author();
        
            // 可以用default为成员制定一个默认值
            int age() default 18;
        
        
        }
        ```

    2. 注解使用
    
        ```
        /**
         * 使用自定义注解的语法:
         *
         * @<注解名>(<成员名1>=<成员值1>, <成员名1>=<成员值1>, ...)
         */
        
        @Description(desc = "描述信息, 注解在类上", author = "姓名")
        public class CustomAnnotation {
            public String string;
        
            @Description(desc = "描述信息, 注解在方法上", author = "作者名", age = 30)
            public String eyeColor() {
                return "black";
            }
        
        }
        ```

    3. 解析注解 : 通过反射获取类 函数 或者 属性上 运行时 注解信息, 从而实现动态控制程序运行的逻辑.

        ```
        import java.lang.annotation.Annotation;
        import java.lang.reflect.Method;
        import java.util.Arrays;
        
        /**
         * @author: 个人姓名
         * @date: 2018/3/18 下午10:15
         * @className: TestAnnotation
         * @version: 1.0.0
         * @description:
         */
        public class TestAnnotation {
        
            /**
             * 能运行时候解析到结果的注解都是 运行时注解, 一定要用@Retention(RetentionPolicy.RUNTIME)
             */
        
            public static void main(String[] args) throws ClassNotFoundException {
                //1: 使用类加载器加载类
                Class cls = Class.forName("com.linkzp.jdkproxy.CustomAnnotation");
                // 2: 找到类上的注解,
                System.out.println(Arrays.toString(cls.getAnnotationsByType(Description.class)));
                boolean isExist = cls.isAnnotationPresent(Description.class);
                if (isExist) {
                    // 3: 拿到注解实例
        
                    Description description = (Description) cls.getAnnotation(Description.class);
                    System.out.println(description.author());
                    System.out.println(description.desc());
                    System.out.println(description.age());
                }
        
                // 4: 找到方法的注解
                Method[] methods = cls.getMethods();
        
                for (Method method : methods) {
                    boolean isMethodAnnotation = method.isAnnotationPresent(Description.class);
                    if (isMethodAnnotation) {
                        Description methodDescription = method.getAnnotation(Description.class);
                        System.out.println(methodDescription.author());
                        System.out.println(methodDescription.desc());
                        System.out.println(methodDescription.age());
                    }
                }
        
                // 5: 方法注解解析的另外一种解析方法
        
                for (Method method : methods) {
                    Annotation[] annotations = method.getAnnotations();
                    for (Annotation annotation : annotations) {
                        if (annotation instanceof Description) {
                            Description description = (Description) annotation;
                            System.out.println(description.author());
                            System.out.println(description.age());
                            System.out.println(description.desc());
                        }
                    }
                }
            }
        }
        ```


参考来源
http://blog.csdn.net/zen99t/article/details/49506919
http://blog.csdn.net/zen99t/article/details/49508447
http://blog.csdn.net/zen99t/article/details/49512411
http://blog.csdn.net/zen99t/article/details/50351575
https://www.imooc.com/video/8867


