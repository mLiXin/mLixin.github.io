---
title: Android Lib解析之EventBus
date: 2018-02-17 13:50:30
tags:
- Android
categories:
- Android
- 第三方库解析
---

#### 介绍
- GitHub地址：[EventBus](https://github.com/greenrobot/EventBus)
- 官方使用文档：[Documentation](http://greenrobot.org/eventbus/documentation/)
- EventBus 是专门为Android设计的用于、订阅、发布总线的库。可以简单Android组件之间的通信，避免了Android四大组件复杂的生命周期处理，让代码更简洁。
<!--more-->

#### 涉及知识点
##### 线程安全
- ThreadLocal
	- ThreadLocal是一个关于创建线程局部变量的类。通常情况下，我们创建的变量是可以被任何一个线程访问并修改的。而使用ThreadLocal创建的变量只能被当前线程访问，其他线程则无法访问和修改。
- CopyOnWriteArrayList
	- 线程安全的ArrayList变体，有数据变化时先copy一个副本容器，新数据加入新容器中，然后将旧容器的地址复制给新容器，中间操作过程中有线程来访问还是会访问旧容器 
- ConcurrentHashMap
	- 线程安全、支持高效并发的HashMap变体 

##### 注解处理器
- Annotation Processor
	- Auto Service
	- JavaPoet

#### 源码分析

##### 构造函数
```Java
    public static EventBus getDefault() {
        EventBus instance = defaultInstance;
        if (instance == null) {
            synchronized (EventBus.class) {
                instance = EventBus.defaultInstance;
                if (instance == null) {
                    instance = EventBus.defaultInstance = new EventBus();
                }
            }
        }
        return instance;
    }
    
    public EventBus() {
        this(DEFAULT_BUILDER);
    }

    EventBus(EventBusBuilder builder) {
        ......
        subscriptionsByEventType = new HashMap<>();
        typesBySubscriber = new HashMap<>();
        ......
        subscriberMethodFinder = new SubscriberMethodFinder(builder.subscriberInfoIndexes,
                builder.strictMethodVerification, builder.ignoreGeneratedIndex);
        ......
    }
```

- `getDefault()` ： DoubleCheck的单例模式，保证线程安全
- `EventBusBuilder` ： 建造者模式，可以通过builder来获取实例
- `ignoreGeneratedIndex` ： 策略模式，参数不同，执行不同的代码

##### register
![EventBus resgiter流程](/images/eventbus-register.jpg)

- register传参是subscriber，流程就是将subscriber这个订阅类中的订阅方法、订阅事件等信息收集并缓存到指定Map中，其中:
	- subscriptionsByEventType
		- key类型是Class<?>，是定义的事件，例如MessageEvent
		- value类型是CopyOnWriteArrayList<Subscription>，是一个存储Subscription的线程安全的数组列表，其中Subscription成员变量是订阅类和订阅方法
	- typesBySubscriber 
		- key类型是Object，是订阅类
		- value是List<Class<?>>，是这个订阅类订阅的所有事件列表

	这里要注意，订阅方法是有筛选的，必须是`Public修饰的`、`非static`、`参数只有一个`的方法，不符合这三条的订阅方法都不会被缓存到Map中，如果是用注解处理器，在build的时候就会报错。

##### post
![EventBus post流程](/images/eventbus-post.jpg)

- post传参是event，流程是根据eventType获取到订阅了这个event事件的subscriptions，遍历并通过invoke的方法调用订阅方法，这里涉及到ThreadMode：
	- `POSTING`
		- 在哪个线程post的事件，就在哪个线程执行订阅方法。查看源码也可以知道，这个case直接invokeSubscriber，就是直接执行了订阅方法，没有判断当前是处于哪个线程的。在Android中，因为一般都是在主UI线程中post事件的，所以订阅方法里面不能执行耗时操作，不然会导致ANR

		> Subscriber will be called directly in the same thread, which is posting the event 
	- `MAIN`
		- 不管post是在哪个线程中，订阅方法都会在主UI线程中执行。查看源码可以看出，如果post是在主UI线程的话，会直接invokeSubscriber；如果是在其他的线程post的事件，会将事件加入到mainThreadPoster队列中，由这个poster去执行订阅方法。

		> On Android, subscriber will be called in Android's main thread (UI thread). If the posting thread is the main thread, subscriber methods will be called directly, blocking the posting thread. Otherwise the event is queued for delivery (non-blocking).
	- `MAIN_ORDERED`
		- 和`MAIN`有点类似，但是这里不管post是在哪个线程中，都会将event加入到mainThreadPoster中，而不会直接invoke。

		> On Android, subscriber will be called in Android's main thread (UI thread). Different from {@link #MAIN},the event will always be queued for delivery.
	- `BACKGROUND`
		- 如果是在主线程中post的事件，则将事件加入到backgroundPoster中，这个poster会在后台线程中处理事件；如果是在其他线程中post的事件，则直接会在这个线程执行订阅方法。

		> On Android, subscriber will be called in a background thread. If posting thread is not the main thread, subscriber methods will be called directly in the posting thread. If the posting thread is the main thread, EventBus uses a single background thread, that will deliver all its events sequentially. 
	- `ASYNC`
		- 不管是在哪个线程中post事件，最后都会在一个单独的线程中执行订阅方法。

		> Subscriber will be called in a separate thread. This is always independent from the posting thread and the main thread.  

##### unregister
![EventBus unresgiter流程](/images/eventbus-unregister.jpg)

- unregister传参是subscriber，流程是根据subscriber找到它订阅的所有事件集合subscribedTypes，遍历这个事件集合，根据事件找到它所有的subscriptions，并将这个subscriber对应的subscription从subscriptions中移除。这样主要是为了高效，不然缓存的事件越来越多，查找事件去传递会越来越低效。

#### 小结
EventBus就是通过register将subscriber中订阅事件、订阅方法存到Map中，当post事件之后，从这个Map中找到相关subscriber的订阅方法进行invoke来实现事件的传递。
