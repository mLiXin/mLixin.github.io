---
title: 设计模式之禅 学习笔记
date: 2018-09-28 10:29:33
tags:
- book
- 设计模式之禅
categories:
- 设计模式
---
#### 第1、2、3、4、5、6章 六大设计原则
1. 6大设计原则都是什么？
    - 单一职责原则
    - 里氏替换原则
    - 依赖倒置原则
    - 接口隔离原则
    - 迪米特原则
    - 开闭原则

2. 什么是单一职责原则(Single Responsibility Principle)？
    - 应该有且仅有一个原因引起类的变更。(There should never be more than one reason for a class to change.)

3. 什么是里氏替换原则(Liskov Substitution Principle)？
    - 所有引用基类的地方必须能透明地使用其子类的对象，(Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it.).即只要父类能出现的地方，子类就可以出现，而且替换为子类也不会产生任何错误或异常，使用者可能根本不序言知道是父类还是子类，但是反过来就不行了，有子类出现的地方，父类未必就能适应。
    - 4层含义：
        - 子类必须完全实现父类的方法
        - 子类可以有自己的个性
        - 覆盖或实现父类的方法时输入参数可以被放大
        - 覆写或实现父类的方法时输出结果可以被缩小

4. 什么是依赖倒置原则(Dependence Inversion Principle)？
    - 高层模块不应该依赖底层模块，两者都应该依赖其抽象；抽象不应该依赖细节；细节应该依赖抽象。(High level modules should not depend upon low level modules.Both should depend upon abstractions.Abstractions should not depend upon details.Details should depend upon abstractions.)

5. 什么是接口隔离原则(Interface Segregation Principle)？
    - 建立单一接口，不要建立臃肿庞大的接口。就是接口尽量细化，同时接口中的方法尽量少。
    - 4层含义：
        - 接口要尽量小
        - 接口要高内聚
        - 定制服务
        - 接口设计是有限度的。

6. 什么是迪米特原则(Law of Demeter)？
    - 一个对象应该对其他对象有最少的了解。就是一个类应该对自己需要耦合或调用的类知道得最少。
    - 四层含义：
        - 只和朋友交流
        - 朋友间也是有距离的
        - 是自己的就是自己的：如果一个方法放在本类中既不增加类间关系，也对本类不产生负面影响，那就放置在本类中
        - 谨慎使用Serializable

7. 什么是开闭原则(Open Closed Principle)？
    - 一个软件实体如类、模块和函数应该对扩展开放，对修改关闭。(Soft entities like classes,modules and funtions should be open for extension but closed for modifycations.)

#### 第7章 单例模式
1. 单例模式是怎样的？有什么优缺点？
    - 确保某一个类只有一个实例，而且自行实例化并向整个系统提供这个实例。(Ensure a class has only one instance,and provide a global point of access to it.)
    - 优点：
        - 减少内存开支；减少系统的性能开销；避免对资源的多重占用；优化和共享资源访问。
    - 缺点：
        - 扩展困难，只能修改代码实现；与单一职责原则有冲突。

2. 懒汉式、懒汉式、双重校验、静态内部类、枚举，这五种单例模式分别是怎样的？

```Java
/**
 * 懒汉模式，线程安全
 */
public class LazySingleTon {
    private static LazySingleTon instance;

    private LazySingleTon(){}

    public static synchronized LazySingleTon getInstance(){
        if(instance == null){
            instance = new LazySingleTon();
        }
        return instance;
    }

}
```

```Java
/**
 * 饿汉单例模式
 */
public class HungrySingleTon {
    private static HungrySingleTon instance = new HungrySingleTon();
    private HungrySingleTon(){

    }

    public static HungrySingleTon getInstance(){
        return instance;
    }
}

```

```Java
/**
 * 双重校验单例模式
 */
public class DoubleCheckSingleTon {
    private static volatile DoubleCheckSingleTon instance;

    private DoubleCheckSingleTon(){}

    public static DoubleCheckSingleTon getInstance(){
        if (instance == null){
            synchronized (DoubleCheckSingleTon.class){
                if (instance == null){
                    instance = new DoubleCheckSingleTon();
                }
            }
        }
        return instance;
    }
}

```

```Java
/**
 * 静态内部类单例模式
 */
public class StaticInnerClassSingleTon {
    private static class SingleTonHolder{
        private static final StaticInnerClassSingleTon instance = new StaticInnerClassSingleTon();
    }

    private StaticInnerClassSingleTon(){}

    public static StaticInnerClassSingleTon getInstance(){
        return SingleTonHolder.instance;
    }
}

```

```Java
/**
 * 枚举单例模式
 */
public enum EnumSingleTon {
    INSTANCE;
}

```

