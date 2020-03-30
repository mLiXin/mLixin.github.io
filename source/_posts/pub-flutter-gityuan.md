---
title: GitYuan Flutter相关tag学习笔记
date: 2019-09-11 14:04:24
tags:
- Flutter
- Pub
categories:
- Flutter
---
#### Tips
原博客源码基于`Flutter1.5`，我对应查看的源码基于`Flutter1.9`.

#### [深入理解Flutter引擎启动 - TODO 基于Android，很多C++代码，先留着](http://gityuan.com/2019/06/22/flutter_booting/)
1. Flutter引擎启动过程分为以下几个阶段：
    - FlutterApplication启动：执行其onCreate()方法，初始化配置，获取是否预编译模式，提取资源文件；加载libflutter.so库，并记录启动时间戳；
    - FlutterActivity启动：执行其onCreate()方法，创建FlutterActivityDelegate、FlutterView、FlutterNativeView、FlutterMain、FlutterJNI等对象，也会初始化以下这些引擎核心类：
        - AndroidShellHolder
        - DartVM
        - Shell
        - PlatformViewAndroid
        - VsyncWaiterAndroid
        - ShellIOManager
        - Rasterizer
        - Animator
        - Engine
        - RuntimeController
        - Window
        - DartIsolate

#### [深入理解Dart虚拟机启动 - TODO 又见C++](http://gityuan.com/2019/06/23/dart-vm/)
1. Dart虚拟机拥有自己的Isolate，完全由虚拟机自己管理的，Flutter引擎也无法直接访问。Isolate之间内存并不共享，而是通过Port方式通信，每个Isolate是有自己的内存以及相应的线程载体。Isolate中的代码是按顺序执行，因为Dart没有共享内存的并发，没有竞争的可能性，故不需要加锁，也没有死锁风险。对于Dart程序的并发则需要依赖多个isolate来实现。
2. 同一个进程只有一个Dart虚拟机，所有的Shell共享该进程中的Dart虚拟机， 当leak_vm为false则在最后一个Shell对象退出时会回收dart虚拟机， 当leak_vm为true则即便Shell对象全部退出也不会回收dart虚拟机，这是为了优化再次启动的速度。
3. DartVM创建过程：
    - 创建名为”dart:io EventHandler”的线程，然后进入该线程进入poll轮询方法；
    - 创建名为”vm-isolate”的Isolate对象；
    - 执行InitForGlobal()过程会注册各种Native方法，用g_natives记录UI相关类，用g_natives_secondary记录非UI相关类；
4. Isolate创建过程：
    - 创建DartIsolate和UIDartState对象；
    - 向task_observers_中添加TaskObserver，并所对应的操作方法为FlushMicrotasksNow();
    - 创建名为“Isolate-xxx”的Isolate对象，其中xxx是通过PortMap::CreatePort所创建port端口号；
    - 加载”dart:ui”和”dart:io”库，并安装DartRuntimeHooks。
5. 关于Isolate有以下四种：
    - Dart虚拟机的Isolate：”vm-isolate”；
    - 服务Isolate：”vm-service”；
    - 内核Isolate：”kernel-service”；
    - 常见Isolate：“Isolate-xxx”，对于RootIsolate则属于这个类别；
6. Runtime Mode运行时模式有3种：debug，profile，release，其中debug模式使用JIT，profile/release使用AOT。在整个源码过程会有不少通过宏来控制针对不同运行模式的代码。 比如当处于非预编译模式(DART_PRECOMPILED_RUNTIME)，则开启Assert断言，否则关闭断言。

#### [深入理解Flutter应用启动](http://gityuan.com/2019/06/29/flutter_run_app/)
- 参考其他[Flutter Dart Framework原理简解](https://www.stephenw.cc/2018/05/28/flutter-dart-framework/)
1. Flutter App的启动入口是`void main() => runApp(MyApp());`，我们就从这行代码来看看Flutter 应用是如何启动的。
    - WidgetsFlutterBinding.ensureInitialized()
        - 这是一个单例模式，负责创建WidgetsFlutterBinding对象，WidgetsFlutterBinding继承抽象类BindingBase，并且附带7个mixin，初始化渲染、语义化、绘制、平台消息以及手势等一系列操作；
    - attachRootWidget(app)
        - 遍历挂载整个视图树，并建立Widget、Element、RenderObject之间的连接与关系，此处Element的具体类型为RenderObjectToWidgetElement；
    - scheduleWarmUpFrame();
        - 调度预热帧，执行帧绘制方法handleBeginFrame和handleDrawFrame。
2. Flutter中3个比较重要的树：
    - Widget，继承自DiagnosticableTree
        - Describes the configuration for an Element.(为Element提供配置信息)
        - 可以理解为，widget只是用来保存属性的容器
        - Widget里面存储了一个视图的配置信息，包括布局、属性等待。所以它只是一份轻量的，可直接使用的数据结构。
    - Element，继承自DiagnosticableTree
        - An instantiation of a Widget at a particular location in the tree.(Element是在树中特定位置Widget的实例)
        - Element是Widget的实例
        - Element是 Widget的抽象，它其实承载了视图构建的上下文数据。构建系统通过遍历 Element树来构建 RenderObject数据，比如视图更新时，只会标记 dirty Element，而不会标记 dirty Widget。所以 Widget“无状态”，而 Element“有状态” （这个状态指框架层的构建状态）。
    - RenderObject，继承自AbstractNode
        - An object in the render tree.(渲染树中的一个对象。)
        - 只负责渲染工作
        - 在 RenderObject树中会发生 Layout、Paint的绘制事件，所以 Flutter中大部分的绘图性能优化发生在这里。RenderObject树构建的数据会被加入到 Engine所需的 LayerTree中，Engine通过 LayerTree进行视图合成并光栅化，提交给 GPU。

#### [深入理解Flutter消息机制 - TODO 又是C++，过。感觉要先复习一下C++才看的下去，这是个问题](http://gityuan.com/2019/07/20/flutter_message_loop/)
- Flutter引擎启动过程，会创建UI/GPU/IO这3个线程，并且会为每个线程依次创建MessageLoop对象，启动后处于epoll_wait等待状态。对于Flutter的消息机制跟Android原生的消息机制有很多相似之处，都有消息(或者任务)、消息队列以及Looper，有一点不同的是Android有一个Handler类，用于发送消息以及执行回调方法，相对应Flutter中有着相近功能的便是TaskRunner。
	



