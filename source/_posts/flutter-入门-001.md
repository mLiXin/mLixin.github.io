---
title: Flutter入门(一) Dart基础
date: 2020-04-09 13:44:08
tags:
- Flutter
- Dart
categories:
- Flutter
---
#### 摘要
总结Dart语言入门基础

<!--more-->
#### 基础语法
#####  内置数据类型
- 类型：
    - num
        - int：-2^53 ~ 2^53
        - double：64位双精度浮点数
    - String
    - bool
    - List
    - Map
    - Runes
- 所有的变量都是对象，所有对象都集成与Object类，所有类型没有初始化的变量默认值为null。

##### 变量与常量
- 两种方式定义变量：
    - 显式指定变量类型：`String name = "hello";`
    - 不指定类型：`var name = "hello";`
- 使用dunamic或Object定义的变量可以动态改变变量的数据类型
- 定义常量的两种方式：
    - final：运行时常量，可以是一个变量
    - const：编译时常量，必须是一个字面常量值。

##### 内置类型的常用操作
- String转int
    - `var one = int.parse('1');`
- String转double
    - `var onePointOne = double.parse('1.1');` 
- int转String
    - `String oneStr = 1.toString();`
- double转String
    - `String paiAsStr = 3.14159.toStringAsFixed(2);//保留两位小数`
- 数位操作
    - `print((3<<1) == 6);` 
    - `print((3>>1) == 1);`
    - `print((3|4) == 7);`
- 字符串操作
    - 可以用单引号、双引号来创建字符串
    - 可以使用三引号来创建多行字符串
    - 前面加r可以创建原始字符串，特殊字符不用转义
    - 支持“+”拼接字符串
    - 支持插值表达式“${}”
    - 使用“==”比较字符串内容
- 布尔类型默认值为null，只有flase、true两个值
- 列表操作：
    - 创建列表：`var list = [1,2,3];`
    - 可以通过数组下标方式访问列表item：`list[0];`
    - 可以使用add添加元素
    - 可以在lsit字面量钱添加const关键字来定义一个不可改变的列表
- 映射操作：
    - 字面量创建Map：`var keyMap = {"first":1,"secode":2};`
    - 构造函数创建Map：`var keyMap = new Map(); keyMap['first'] = 1;`
    - 通过可以下标查找map：`keyMap['first']`

##### 函数
- 定义函数：
    - `返回值类型 函数名(参数){ 处理和return}`
- 不指定函数返回类型，则返回null，除非指定void，则函数没有返回值
- 函数的参数
    - 命名可选参数：
        - 定义函数的时候，给参数列表中的参数设置默认值，则该参数是可选的，函数调用的时候可以忽略
    - 位置可选参数
        - 使用中括号来定义参数列表，中括号中的参数是可选的

- 匿名函数：
    - 没有名字的函数，也被称为lambda表达式或者闭包。
    - 和普通函数基本相同，只是省去了函数名而已。
    - `var func = (x,y){ return x + y;}; print(func(10,11));`
- 箭头函数
    - 函数体只包含一条语句的时候，就可以使用=>箭头语法进行缩写。仅仅是一个简洁表达的语法糖。

##### 运算符
- 整除运算符：`~/`，将相除后的结果取整返回。
- 类型判定运算符：
    - `as`：类型转换
        - 无法转换会抛出异常，注意判断类型
    - `is`：对象是指定类型
    - `is!`：对象不是指定类型
- 三元表达式：
    - `condition ? expr1 : expr2`
- 判空
    - `expr1?? expr2`：expr1不为空，取自己值；为空，则取expr2的值。
- 级联运算符
    - `..`：可以在同一个对象上连续滴啊用多个方法以及访问成员变量。可以避免创建临时变量。
- 条件成员访问符
    - `?.`：如果左边的对象为null，则直接返回null

##### 分支与循环
- switch中的case可以使用整数、字符串、枚举类型和编译时常量。
- 循环支持for循环、while循环，do-while循环
- List的遍历：
    - for...in...循环
    - forEach循环：`list.forEach((var it){ print(it);});`
    - 箭头函数简写：`list.forEach((it) => print(it));`
- Map的遍历
    - for...in...：`for(var k in map.keys){ }`
    - forEach：`map.forEach((k,v) => print());`

#### 类和对象
- 没有`private`、p`ublic`等成员访问修饰符，类私有成员，前面加`_`变为私有
- 没有构造方法的重载，不能写两个同名的构造方法
- 所有的类中都包含隐式的getter方法；所有非final修饰的成员都包含隐式的setter方法。
- setter、getter方法不仅仅是赋值和访问，而是为了一些额外的处理的时候，需要在方法名前添加set/get关键字
- 命名构造方法：
    - `className.fromData(String data){this.data = data}`
    - 可以为一个类实现多个构造方法，更清晰表明意图

- 常量构造方法：
    - 编译时常量对象：状态永远不变的对象，节省开销。
        - 使用const修饰构造方法：`const Class(this.x,this.y);`
        - 使用const创建对象：`static final Class class = const Class(0,0)`
- 工厂构造方法：
    - 创建一个新的对象或者从缓存中取一个对象的时候使用
    - `factory Class(String name){ if(_cache.containsKey(name)){ return _cacheInstance;} else { return newInstance;}}`
- 构造方法重定向
    - 命名构造方法重定向到同名构造方法，中间使用一个冒号：`Class.fromData(string test):this(test,0);`
- 类的初始化列表：
    - 普通构造方法：`类名(){}`
    - 带初始化列表的构造方法：`类名():赋值语句{}`
- 运算符重载：
    - 即为类重载运算符的操作：`Point operator +(Point p){ return new Point(xxx)};`
- 类的继承
    - 使用关键字`extends`，使用`super`引用父类
    - 可以使用`with`实现多继承
        - `class Son extends father1 with father2,father3`
        - `class Son with father1,father2,father3`

- Dart不支持interface，只有`abstract`
- 隐式接口
    - 每个类都隐式的定义了一个包含所有势力成员的接口，并且该类实现了这个接口。
    - 可以使用`implements`关键字实现某个接口又不用继承。

#### 异常处理
- 异常的两种处理方式：
    - 关心异常，针对不同异常进行不同处理：`try...in`处理异常，`finally`可选，用于最后的处理
    - 不关心异常，只捕获，避免异常继续传递：`try...catch`

#### 库与导入
- 使用`import`语句用来导入一个库
- 使用`as`给库起别名，避免命名空间冲突
- 使用`show`/`hide`控制库中成员的可见性
- 使用`deffered as`延迟导入

#### 异步编程
- 单线程模型，所有代码都只在一个线程上运行，但是Dart代码可以运行在多个isolate上，isolate由虚拟机调度，isolate之间没有共享内存，因此它们之间没有竞争，不需要锁，不用担心死锁。isolate之间唯一的通知只能通过Port进行，而且Dart中的消息传递也是一部的。
- 使用Future对象进行异步编程的两种方式：
    - 使用`async`和`await`
    - 使用Future api

- Dart是事件驱动的体系结构，这种结构基于具有单个事件循环和两个对立的单线程执行模型
    - Dart的两个队列：
        - MicroTask queue 微任务队列
            - 添加任务到MicroTask队列的方法：
                - `scheduleMicrotask(myTask);`
                - `Future.microtask(myTask);`
            - 添加任务到Event队列
                - `new Future(myTask)` 
        - Event queue 事件队列
    - 当事件循环在处理MicroTask队列时，Event队列会被卡住，应用程序无法处理鼠标单击、I/O消息等等事件

- 延时任务：
    - 使用`Future.delayed`方法，将任务加入到Event队列

- Future
    - Future类是对未来结果的一个代理，返回的并不是被调用的任务的返回值
    - 创建方法：
        - `Future()`
        - `Future.microtask()`
        - `Future.sync()`：同步方法，任务会被立即执行
        - `Future.value()`
        - `Future.delayed()`
        - `Future.error()`
- 当Future中的任务完成后，可以使用`then`注册回调，这个回调会立即执行，不会被添加到事件队列
- 可以使用`catchError`处理异常
- 可以使用静态方法`wait`等待多个任务全部完成后回调

- async和await
    - async
        - 被修饰的方法会将一个Future对象作为返回值
        - 该方法会同步执行其中的方法代码知道第一个await关键字，然后它暂停该方法其他部分的执行
        - 当await关键字引用的Future任务执行完成，await的下一行代码将立即执行。

- Isolate
    - 可以理解为微线程，不能共享内存，不存在锁竞争，两个Isolate完全是两条独立的执行线，每个Isolate都有自己的事件循环，它们之间只能通过发送消息通信。
