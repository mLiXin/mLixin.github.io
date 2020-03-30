---
title: Android 四大组件之Activity
date: 2019-07-08 15:51:22
tags:
- Android
categories:
- Android
---

#### 启动流程

##### 源码调用流程图，基于api27
![Android启动流程](/images/android-activity-launch.jpg)
	
<!--more-->
![进程不存在情况下，新建进程](/images/android-activity-launch-new-thread.jpg)
	
##### 启动流程总结
- 流程[1~3]:运行在调用者所在进程，比如从桌面启动Activity，则调用者所在进程为launcher进程，launcher进程会调用ActivityManagerService的startActivity方法，进入system_server进程(AMS相应的Server端)。
	- `ActivityManager.getService()`返回的是`ActivityManagerService`对象，以前好像是`ActivityManagerProxy`
- 流程[4~13]:运行在system_server系统进程，整个过程最为复杂、核心的过程，下面其中部分步骤：
	- 流程[6]：会调用到resolveActivity()，借助PackageManager来查询系统中所有符合要求的Activity，当存在多个满足条件的Activity则会弹框让用户来选择;
	- 流程[7]：创建ActivityRecord对象，并检查是否运行App切换，然后再处理mPendingActivityLaunches中的activity;
	- 流程[9]：为Activity找到或创建新的Task对象，设置flags信息；
	- 流程[12]：当没有处于非finishing状态的Activity，则直接回到桌面； 否则，当mResumedActivity不为空则执行startPausingLocked()暂停该activity;然后再进入startSpecificActivityLocked()环节;
	- 流程[13]：当目标进程已存在则直接进入流程[14]，当进程不存在则创建进程，经过层层调用还是会进入流程[14];
	- 流程[14]：system_server进程利用的ATP(Binder Client)，经过Binder，程序接下来进入目标进程。
- 流程[16~23]:运行在目标进程，通过Handler消息机制，该进程中的Binder线程向主线程发送H.LAUNCH_ACTIVITY，最终会通过反射创建目标Activity，然后进入onCreate()生命周期。

##### 进程创建流程
- 启动进程会通过`startActivity`等方式，通过Binder发送消息给system_server进程；
- system_server进程会调用`Process.start()`方法，通过Socket方式向Zygote进程发送创建进程的请求；
- Zygote进程在执行`ZygoteInit.main()`之后会进入`runSelectLoop()`循环体中，当接收到客户端的连接时会执行`ZygoteConnection.processOneCommand()`方法(以前叫runOnce())，再经过层层调用后fork出新的应用进程；
- 新进程创建完成以后，会继续执行`handleChildProc`方法，里面会先关闭socket连接，然后执行目标类的main()方法，App中则是调用`ActivityThread.main()`。

##### 参考资料
- Android Source Code
- [理解Android进程创建流程](http://gityuan.com/2016/03/26/app-process-create/)  
- [App 启动过程（含 Activity 启动过程](https://blankj.com/2018/09/29/the-process-of-app-start/)
	
#### 启动模式
- 四种启动模式：
	- `standard`：标准模式，也是系统的默认模式。每次启动一个Activity都会重新创建一个新的实例。不管这个实例是否已经存在。
		- 这种模式下，谁启动了这个 Activity，那么这个Activity就会运行在启动它的那个Activity所在的栈中。非Activity类型的Context并没有所谓的任务栈，所以用ApplicationContext启动的时候就会有问题。解决的方法是未待启动的Activity指定FLAG_ACATIVITY_NEW_TASK标记位，这样启动的是哦户就会为它创建一个新的任务栈，这时待启动Activity实际上是以singleTask模式启动的
    - `singleTop`：栈顶复用模式，如果新Activity已经位于任务栈的栈顶，那么这个Activity不会被重新创建，同事它的onNewIntent方法会被回调，通过此方法的参数我们可以取出当前请求的信息。
    	- 注意这个Activity的onCreate、onStart不会被系统调用，因为它并没有改变
    - `singleTask`：栈内复用模式，这是一种单实例模式，在这种模式下，只要Activity在一个栈中存在，那么多次启动此Activity都不会重新创建实例，同时也会回调onNewIntent。
    - `singleInstance`：单实例模式，这是一种加强的singleTask模式，除了具有singleTask模式的所有特性外，还加强了一点，那就是具有此种模式的Activity只能单独的位于一个任务栈中。
- TaskAffinity
    - 配合SingleTask使用，个人理解为指定任务栈名
- Activity的Flags：
    - FLAG_ACTIVITY_NEW_TASK:为Activity指定SingleTask启动模式，效果和在AndroidMenifest中指定启动模式相同。
    - FLAG_ACTIVITY_SINGLE_TOP:为Activity指定SingleTop启动模式，效果和在AndroidMenifest中指定启动模式相同。
    - FLAG_ACTIVITY_CLEAR_TOP:一般配合NEW_TASK flag一起使用
    - FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS:不会出现在历史Activity的列表中
- IntentFilter的匹配规则
    - 同时匹配action、category、data信息，否则匹配失败
	
#### 生命周期
##### 流程
- onCreate
- onNewIntent
- onRestart
- onStart
- onResume
- onPause
- onStop
- onDestroy	

##### tips:
- Activity不可见时才会执行`onStop`，所以如果新启动的Activity是透明的，则旧Activity不会执行`onStop`
- Activity新启动一个activity，必须当前activity的`onPause`执行后，新activity的`onCreate(、onStart、onResume)`才会执行。
- 可能导致Activity被杀死并重建的情况：
   - 资源相关的系统配置发生改变导致Activity被杀死并重新创建
   - 资源内存不足导致低优先级的Activity被杀死
- `onSaveInstanceState`在`onStop`之前执行，与`onPause`没有确定的时序关系；`onRestoreInstanceState`在`onStart`之后执行。
- 每个View也有对应的`onSaveInstanceState`和`onRestoreIntanceState`方法，可以查看每个View都会保存哪些数据，如果当前View没有，可以去父类查找
- 保存和恢复View的层次结构：首先Activity被意外终止时，Activity会调用`onSaveInstanceState`去保存数据，然后Activity会委托Window去保存数据，接着Window再委托它上面的顶级容器去保存数据；顶级容器是一个ViewGroup，一般来说它可能是DecorView，最后顶级容器再去一一通知它的子元素来保存数据，这样整个数据保存过程就完成了。这是一种典型的委托思想，上层委托下层，父容器委托子元素去处理一种事情，这种思想在Android中有很多应用，比如View的绘制过程、事件分发等都是采用的类似的思想。数据恢复过程也是类似的。
- 举例说明TextView保存了自己的文本选中状态和文本内容。
- Activity按照优先级从高到底可以分为以下三种：
    - `前台Activity`--正在和用户交互的Activity，优先级最高
    - `可见但非前台Activity`--比如Activity中弹出了一个对话框，导致Activity可见但是位于后台无法和用户直接交互
    - `后台Activity`--已经被暂停的Activity，比如执行了onStop，优先级最低
- 当系统内存不足时候，系统会按照上述的优先级去杀死目标Activity所在的进程，并在后续通过onSaveInstanceState和onRestoreInstanceState来存储和恢复数据。如果一个进程中没有四大组件在执行，那么这个进程将很快被系统杀死，因此，一些后台工作不适合脱离四大组件而独自运行在后台中，这样进程很容易被杀死。比较好的方法是将这些后台工作放入Service中从而保证进程有一定的优先级，这样就不会轻易被系统杀死。 
