---
title: Java集合(一) 详解Java中的List接口
date: 2019-12-09 16:08:22
tags:
- Java
categories:
- Java
- 原理解析
---
#### 摘要
List是有序、可重复的容器。

#### 常用方法
- `size();`
- `isEmpty();`
- `contains(Object o)`
- `add(E e)`
- `remove(Object o)`
- `get(int index)`
- `set(int index, E element);`

#### 常见实现类
##### ArrayList
###### 根据名字猜实现
数组实现，需要考虑数组需要动态扩容的情况
###### 源码分析
- 构造函数
    - 两种常用的构造函数
        - 无参数
            - elementData会初始化为一个空数组，容量为0
        - 传入一个initialCapacity参数
            - elementData会初始化为一个容量为initialCapacity的数组
    - 使用的时候如果事先知道List的大小，优先使用带参数的构造函数，可以减少一次数组的动态扩容，效率更高。
    - 即使传入了initialCapacity参数，后续如果ArrayList超过了这个参数的值，ArrayList仍然不会报错，只是会触发动态扩容来增大数组容量。
- add方法：`boolean add(E e)`
    - 确保数组容量满足add一个新的元素
        - 容量不够的时候，会通过数组拷贝，动态扩容elementData，通过`int newCapacity = oldCapacity + (oldCapacity >> 1);`可以知道，每次扩容为之前的1.5倍
        - 如果是以无参数的构造函数初始化的，默认的容量是10
    - 将元素放入elementData数组size位置，并将size++
- get方法：`E get(int index)`
    - 判断当前index是否小于size
    - 直接取elementData数组的第index位，时间复杂度为O(1)
- remove方法：`E remove(int index)`
    - 判断参数index是否小于size
    - 从elementData数组中拿到当前index的value
    - 将index后面的数据都往前一位
    - 将elementData最后一位置为null，并将size减一

###### 实现原理
- 数组实现，都是基本的数组操作。数组容量不够的时候会扩容为之前容量的1.5倍，默认容量是10.
- 线程不安全，比如说add方法中`elementData[size++] = e;`实际是分成了两句：`elementData[size] = e; size++;`，举例说size=0的时候，线程1将elementData[0]赋值1，此时线程切换，size还是等于0，则线程2将elementData[0]赋值2，然后进行size++，这个时候elementData[0] = 2，而elementData[1]没有值，而此时size=2，1的位置就空洞了。

###### Tips
- 如果事先知道容量的时候，可以优先使用带容量参数的构造函数，这样能减少数组扩容导致的性能消耗
- add/get时间复杂度都是O(1)，add(index)/remove(index)需要批量移动元素，时间复杂度比较高，使用的时候如果一个List只有add和get操作，可以使用ArrayList，如果涉及里面的添加和删除操作，则使用LinkedList效率更高。
- 线程不安全的，可以用CopyOnWriteArrayList替换
- elementData是用transient修饰的，因为elementData里面不是所有的元素都有数据，因为容量的问题，elementData里面有一些元素是空的，这种是没有必要序列化的。ArrayList的序列化和反序列化依赖writeObject和readObject方法来实现。可以避免序列化空的元素，节省空间

##### LinkedList
###### 根据名字猜实现
链表实现的List

###### 源码分析
- 构造函数
    - 无参构造函数，链表实现，无需提前指定容量，没意义，链表可以是容量无限的List
- add方法：`boolean add(E e)`
    - 直接将元素的Node添加到链表尾部即可
- get方法：`E get(int index)`
    - 成员变量有size，首先检查index是否在size范围内
    - 判断index位于前半段还是后半段，如果前半段就从first开始遍历查找，如果在后半段就从last开始遍历查找。
    - 里面的Node是有前后指针的双向链表实现的。
- remove方法：`remove(Object o)`
    - 如果o为空，则从first开始遍历链表，如果x.item == null则将这个Node从链上unlink
    - 不为空，同样从first开始遍历链表，当o和Node.item相等(equals)的时候,将这个Node从链上unlink。
    - 这里要注意，unlink后直接return true了，所以如果LinkedList添加了多个同样的object，remove方法只会remove第一个object，后面的不会处理

###### 实现原理
- 通过双向链表实现，成员变量size表示当前List的容量；
- 当查找index位置的值的时候，通过index和size的对比判断index位于前半段还是后半段，前半段从first开始遍历，后半段则从last开始遍历(所以需要双向链表来实现，单链表后后面开始遍历是无解的。)
- 线程不安全

###### Tips
- first/last都是transient修饰的，因为first、last是持有的对象引用，序列化的时候这些都失效没意义了，所以用transient修饰，同时自己实现Serializable接口的writeObject、readObject。
- 双向链表实现，大容量的情况下，性能肯定会比单链表好一些，单链表只能从表头开始遍历，双向链表可以从两头开始遍历。

##### CopyOnWriteArrayList
###### 根据名字猜实现
线程安全的ArrayList？

###### 源码分析
- 构造函数
- add方法：`boolean add(E e)`
    - 局部lock(可重入锁)指向当前成员变量lock并加锁，所以锁的是当前类
    - 拿到当前的array，拷贝并将容量加1，将元素放到数组最后面，并将当前array指向这新的数组
    - 最后释放锁，其他的线程可以获取该锁
    - 获取锁和释放锁将add的操作可以看成是原子操作，内部职能有一个线程运行代码块
- get方法：`E get(int index) `
    - 直接拿array中index位置的值，这里array有volatile修饰保证对array写之后，每次读都是最新的,所以在add方法里进行了setArray完成之后，其他的线程再读这个array，都是最新的array；setArray完成之前，则读的都是之前的array
- remove方法：`public E remove(int index)`
    - 和add类似，通过加锁将remove操作变成原子操作，这里注意，锁对象是同个lock，锁的是类变量lock，所以add和remove只有一个会被执行
    - 根据index知道remove的位置，然后进行对应的拷贝动作，最后将array指向新数组。

###### 实现原理
- List的变化add、remove等都先加锁再操作，保证只有一个线程可以修改List
- 修改完成之后会将array指向新数组，完成之前，其他线程读的时候还是读的旧数组

###### Tips
- 多线程情况下可以使用CopyOnWriteArrayList替代ArrayList，没有线程并发问题还是用ArrayList性能更好。
- CopyOnWriteArrayList每次的add或remove操作都会拷贝一次数组，性能低下