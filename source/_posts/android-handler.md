---
title: Android简析 - Handler机制
date: 2018-01-03 11:39:26
tags:
- Android
- TODO
categories:
- Android
- 内部机制
---
#### Tips
Base on API 27

#### 使用
```Java
// 这样写Lint会提示"This Handler class should be static or leaks might occur"，后面分析为什么这样写可能导致内存泄漏
Handler handler = new Handler(){
	public void handleMessage(Message msg){
		// doSomething
	}
}
...
Message msg = handler.obtainMessage();
handler.sendMessage(msg);
```

#### 源码解读
##### 构造函数 `new Handler()`
```Java
public Handler() {
	this(null, false);
}
...
// callback == null,async == false
public Handler(Callback callback, boolean async) {
        ...
	mLooper = Looper.myLooper();
	if (mLooper == null) {
		throw new RuntimeException(
                "Can't create handler inside thread " + Thread.currentThread()
                        + " that has not called Looper.prepare()");
        }
	mQueue = mLooper.mQueue;
	mCallback = callback;
	mAsynchronous = async;
}
```
1. 通过Looper.myLooper()获得Looper对象实例
	
	```Java
	static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
	...
	public static @Nullable Looper myLooper() {
        return sThreadLocal.get();
    }
	```
	通过sThreadLocal拿到当前线程的Looper对象，这里可以看出来，一个线程都有一个对应的Looper对象。
	- 那主线程中的Looper对象是在哪里创建的？
		- 如果之前了解过Activity的启动流程，就知道Activity的启动是通过主线程的Handler发送`LAUNCH_ACTIVITY`事件来启动的，所以在ActivityThread的main方法里面就初始化了一个主线程的Handler和Looper对象，大家可自行查看`ActivityThread#main(String[] args)`，调用流程是：
			- `Looper.prepareMainLooper();`
			- `prepare(false);`
			-  `sThreadLocal.set(new Looper(quitAllowed));`
			-  `mQueue = new MessageQueue(quitAllowed);`
		- 上面的调用流程可以看出来，Looper对象在生成自己的实例对象的时候也生成了对应的MessageQueue对象实例。
	- 子线程中如何使用Handler呢？
		- 如果直接在子线程中`new Handler()`，会报异常，就是上面代码9~11行中，因为通过`Looper.myLooper()`拿不到当前线程的mLooper对象，所以需要在子线程中创建一个。
		- 我们在`ActivityThread#main`中知道主线程的Looper是通过`Looper.prepareMainLooper()`然后调用`Looper#prepare`方法来创建的，而这个prepare方法是一个public的静态方法，那直接在子线程中先调用`Looper.prepare()`就可以创建一个子线程对应的Looper对象了。
2. 通过mLooper.mQueue获得MessageQueue对象实例

##### 获取Message `handler.obtainMessage()`
其实获取Message有三种方法：

1. new Message()
2. handler.obtainMessage()
	- 这种方式第三种是一样的，方法里面就是调用的`Message.obtain(this);`来获取Message的
3. Message.obtain()
	
	```Java
	Message next;
	public static final Object sPoolSync = new Object();
    private static Message sPool;
	...
	public static Message obtain() {
        synchronized (sPoolSync) {
            if (sPool != null) {
                Message m = sPool;
                sPool = m.next;
                m.next = null;
                m.flags = 0; // clear in-use flag
                sPoolSize--;
                return m;
            }
        }
        return new Message();
    }
	```
	- 为什么这里要有一个synchronized锁？
		- 因为Handler还可以在子线程中使用，就存在并发的情况。如果两个线程同时通过obtain去拿Message，而Message又是一个单链表，不加锁就可能存在两个线程拿到同一个Message的对象，这样就会有问题。 
	- 这种方式比直接new Message()比有什么优势？
		- 对象的创建是有一系列的操作的：分配内存、初始化、赋值，使用完以后还要再回收等等，如果每次使用Message的时候都要创建一个新的Message对象，肯定会有一定的性能消耗；这种方式就是在发送完消息以后，将这个消息对象clear，然后缓存到`spool`中，这里的实现方式是直接将当前Message添加到spool链表头中：
		
		```Java
		void recycleUnchecked() {
			...
        	synchronized (sPoolSync) {
            	if (sPoolSize < MAX_POOL_SIZE) {
                	next = sPool;
                	sPool = this;
                	sPoolSize++;
            	}
			}
    	}
		```

##### 发送Message `handler.sendMessage(msg)`
不管是sendMessage还是sendMessageDelay等等，最后都是调用的`Handler#sendMessageAtTime`:

```Java
public boolean sendMessageAtTime(Message msg, long uptimeMillis) {
        MessageQueue queue = mQueue;
        ...
        return enqueueMessage(queue, msg, uptimeMillis);
    }
...
private boolean enqueueMessage(MessageQueue queue, Message msg, long uptimeMillis) {
        msg.target = this;
        ...
        return queue.enqueueMessage(msg, uptimeMillis);
    }
```
1. 根据方法名去理解，就是将这个消息放到消息队列中，这个过程是怎样的？
	- 直接查看`MessageQueue.enqueueMessage`方法：

	```Java
	boolean enqueueMessage(Message msg, long when) {
        ...
        synchronized (this) {
            ...
            msg.when = when;
            Message p = mMessages;
            boolean needWake;
            if (p == null || when == 0 || when < p.when) {
                // New head, wake up the event queue if blocked.
                msg.next = p;
                mMessages = msg;
                ...
            } else {
                Message prev;
                for (;;) {
                    prev = p;
                    p = p.next;
                    if (p == null || when < p.when) {
                        break;
                    }
                    ...
                }
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }
        }
        return true;
}
	```
	- mMessages指向消息链表的队头，当队列为空、或者消息的when==0、或者当前队头消息的when比新入队的消息的when大一些的时候，直接将新入队消息放在队头；其他情况下，从mMessages开始遍历这个消息队列，根据消息的when的大小，将新入队消息插入对应的位置
	- 总结来说就是，根据消息的发送时间顺序，将Message插入对应的位置。
2. 为什么将消息放到了消息队列中，handler的handleMessage就能收到这条消息？
	- 在`ActivityThread#main`里面，除了`Looper.prepareMainLooper`之外，还有一行`Looper.loop()`，我们先来看一下这个方法：

	```Java
	public static void loop() {
		final Looper me = myLooper();
		...
		final MessageQueue queue = me.mQueue;
		...
		for (;;) {
			Message msg = queue.next(); // might block
			...
			try {
			msg.target.dispatchMessage(msg);
			...
			} finally {
			...
		}
		...
		msg.recycleUnchecked();
	}
	```
	- 可以看出，就是一个死循环去拿消息队列中的消息;然后通过`msg.target.dispatchMessage(msg)`去分发msg,这里的target就是Handler，dispatchMessage就是调用Handler的dispatchMessage方法，然后调用它的handleMessage方法;最后的`msg.recyclerUnchecked`就是我们上面讲到的通过Message.obtainMessage获取消息而进行的msg的重用。

#### 使用注意
1. 内存泄漏
	- 前面说的，直接`new Handler()`会提示可能存在内存泄漏，为什么会内存泄漏呢？
		- 非静态内部类会持有外部类的引用，所以Handler会持有外部类Activity的引用
		- 拿到消息后对消息进行分发是通过`msg.target.disaptchMessage`来实现的，说明Message会持有Handler的引用
		- 当handler.sendMessageDelayed()之后，当前Activity就onDestroy了，但是这个时候消息队列中还有消息没分发完，还持有了handler的引用，而handler又还持有activity的引用，这样就导致这个Activity不能被回收，从而导致了内存泄漏。
	- 如何避免内存泄漏？
		- 新建静态内部类继承自Handler，静态内部类不会持有外部的引用
		- 在Activity的onDestroy方法中将这个Handler的消息队列清空
2. 子线程中使用Handler
	- 在new Handler之前要先通过`Looper.prepare()`创建一个当前子线程的Looper对象；
	- 创建完Handler之后，需要通过`Looper.loop()`让Looper不断的从MessageQueue中拿消息来处理。

#### 扩展
- MessageQueue内部是怎样的？
	- MessageQueue内部是通过维护一个Message的单链表来实现的队列，因为Message有发送时间的参数，用单链表可以方便插入，时间复杂度是O(1)；同时是将当前when最小的msg放在链表头部，取消息的时候也是O(1)
- ThreadLocal是什么？内部是怎么实现的？会不会存在内存泄露问题？
	- ThreadLocal是一个关于创建线程局部变量的类。通常情况下，我们创建的变量是可以被任何一个线程访问并修改的。而使用ThreadLocal创建的变量只能被当前线程访问，其他线程则无法访问和修改。 
	- [具体可以看这里](https://droidyue.com/blog/2016/03/13/learning-threadlocal-in-java/)
- 为什么非静态内部类会持有外部类的引用而静态内部类不会？
	- 查看Java对应的class文件可以看出，编译器会自动为非静态内部类添加一个成员变量，这个成员变量的类型和外部类的类型相同，指向外部类对象(this)的引用；为内部类的构造方法添加一个参数，参数的类型是外部类的类型，在构造方法内部使用这个参数为内部类中添加的成员变量赋值；在调用内部类的构造函数初始化内部类对象时，会默认传入外部类的引用。
	- TODO tag - 实际通过javap命令查看内部类的时候，查看到的class和网上出来的不一样，可能是Java版本问题，但是这个问题有点存疑，tag一下，看后面能不能get到点。
