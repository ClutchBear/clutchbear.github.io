---
title: "python和java的类当做map的键"
description: "python和java的类当做dict(map)键时候, 如果不覆写hash()和equals方法, 默认使用地址值的hash值存储到map里面, 两个同样属性的类, 虽然内容是一样的,但是地址不一样"
pubDatetime: 2018-04-14T00:49:51
draft: false
tags: ["python", "java"]
---

python和java的类当做dict(map)键时候, 如果不覆写hash()和equals方法, 默认使用地址值的hash值存储到map里面, 两个同样属性的类, 虽然内容是一样的,但是地址不一样, 会被当做两个map的key存在. 

两个内容相同,但是地址不同的**字符串**当做key的时候, map存储一个key. 

```python
string_dict = {}
string1 = "data"
string2 = "data"
string_dict[string1] = "value1"
string_dict[string2] = "value2"
print(string_dict)
{'data': 'value2'}
```

这样的意义在于在A函数定义了一个dict(map), B函数用这个dict获取key对应值的时候, 虽然这两个key的类的地址一般不会一致, 但是A和B函数的两个类key内容一样, 就可以获取到同一个value.

类需要覆写hash()和equals方法才能实现同样的功能


### python测试代码
覆写了hash()和equals方法

```python
class ClassName(object):
    """docstring for ClassName"""

    def __init__(self, arg):
        self.data = arg

    def __eq__(self, another):
        return hasattr(another, 'data') and self.data == another.data

    def __hash__(self):
        return hash(self.data)

    def __lt__(self, another):
        return self.data - another.data


def func_a() -> dict:
    class_a = ClassName(1234)
    print("class_a address_id=", id(class_a))
    class_dict = {class_a: "value"}

    return class_dict


def func_b(class_dict: dict):
    class_b = ClassName(1234)
    print("class_b address_id=", id(class_b))
    value = class_dict.get(class_b)
    print(value)


def main():
    class_dict = func_a()
    func_b(class_dict)


if __name__ == '__main__':
    main()
```

输出是:

```
class_a address_id= 4492965144
class_b address_id= 4492965200
value
```

### java相应测试代码:
没有覆写hash()和equals方法

```java
用lombok注解实现构造方法方法
@Setter
@Getter
@AllArgsConstructor
public class Student {
    private String name;
    private Integer age;
}
```

测试类

```java
public class App {
    public static void main(String[] args) {
        Map<Student, String> map =getStudentMap();
        printStudent(map);
    }
    static private Map<Student, String> getStudentMap(){
        Map<Student, String> map = new HashMap<>(16);
        Student studentA = new Student("xin", 20);
        System.out.println("studentA's address = " + studentA);
        map.put(studentA, "value");
        return map;
    }

    static private void printStudent(Map<Student, String> map){
        Student studentB = new Student("xin", 20);
        System.out.println("studentB's address = " + studentB);
        System.out.println("两个函数是否相等: " + Objects.equals(studentB, map.keySet().toArray()[0]));
        System.out.println("从map中获取到的值是:" + map.get(studentB));
    }

}
```

输出是: 

```
studentA's address = com.example.demo002.zhihu.Student@548c4f57
studentB's address = com.example.demo002.zhihu.Student@1218025c
两个函数是否相等: false
从map中获取到的值是:null
```


参考地址: 
[Java 用自定义类型作为HashMap的键](https://segmentfault.com/a/1190000002655085)
[python: my classes as dict keys. how?](https://stackoverflow.com/questions/5221236/python-my-classes-as-dict-keys-how)


