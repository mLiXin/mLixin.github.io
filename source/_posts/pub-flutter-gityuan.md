---
title: GitYuan Flutter相关tag学习笔记
date: 2019-09-11 14:04:24
tags:
- Flutter
categories:
- Flutter
- 学习笔记
---
#### Tips
啃不啃C++，这是个问题。

<!--more-->
#### [Flutter渲染机制-UI线程](http://gityuan.com/2019/06/15/flutter_ui_draw/)
- 渲染相关的两个线程：
    - UI线程：运行UI Task Runner，是Flutter Engine用于执行Dart root isolate代码，将其转换为layer tree视图结构
    - GPU线程：在GPU上执行，运行GPU Task Runner，处理Layer tree，将其转换成GPU命令并发送到GPU
    - 通过Vsync信号，使UI线程和GPU线程有条不紊的周期性渲染界面。

- 渲染流程：
    - 需要渲染的时候，会调用Engine的scheduleFrame()来注册Vsync信号回调，触发回调doFrame()执行完成后便后移除回调方法，也就是说一次注册一次回调
    - 当再次绘制则需要重新调用scheduleFrame()方法，该方法的唯一重要参数`regenerate_layer_tree`决定在帧绘制过程是否需要重新生成layer tree，还是直接复用上一次的layer tree
    - UI线程的绘制过程，核心的是执行WidgetsBinding的drawFrame()方法，然后会创建layer tree视图树
    - 再交由GPU Task Runner将layer tree提供的信息转化为平台可执行的GPU指令

- UI绘制核心工作：
    - Vsync单注册模式：保证在一帧的时间窗口里UI线程只会生成一个layer tree发送给GPU线程
    - drawFrame()包含的过程：
        - Animate：遍历_transientCallbacks,执行动画回调方法
        - Build：对于dirty的元素回执行build构造，没有dirty的元素不会执行，对应于buildScope()
        - Layout：计算渲染对象的大小和位置，对应于flushLayout(),这个过程可能会嵌套再调用build操作
        - Compositing bits：更新具有脏合成位的任何渲染对象，对应于flushCompositingBits() TODO ???
        - Compositing：将Compositing bits发送给GPU，对应于compositeFrame()
        - Semantics：编译渲染对象的语义，并将语义发送给操作痛，对应于flushSemantics

- UI线程的耗时时长？
    - 从doFrame(frameTimeNanos)中的frameTimeNanos为七店，以Animator::Render()方法结束为终点，并将结果保存到LayerTree的成员变量。

- Timeline工具使用
    - Frame Request Pending：从Animator::RequestFrame到Animator::BeginFrame()结束
    - PipelineProduce：从Animator::BeginFrame()到Animator::Render()结束

- UI线程渲染流程
    - Vsync注册流程
        - 当调用到引擎的scheduleFrame()方法过程， 则会注册Vsync信号回调，当有Vsync信号到达，则会调用doFrame()方法。
        - 动画的执行AnimationController.forward()、surface创建的时候shell::surfaceCrated()等场景都会调用scheduleFrame()方法。
    - Engine层绘制
        - doFrame()经过多层调用后通过PostTask将任务异步post到UI TaskRunner线程来执行，最后调用到Window的BeginFrame()方法
    - Framework层绘制
        - window.cc中的BeginFrame()方法会调用到window.dart中的onBeginFramne()和onDrawFrame()两个方法

- Flutter中核心类：
    - Window类：是连接Flutter框架层(Dart)与引擎层(C++)的关键类，在框架层中的window.dart文件里的一些方法在引擎层的window.cc文件有相对应的方法。
    - RuntimeController类：可通过其成员root_isolate找到window类
    - Shell类：
    - PlatformViewAndroid类：在Android平台上PlatformView的实例采用的便是PlatformViewAndroid类
    - Dart层与C层之间可以相互调用，从Window一路能调用到Shell类，也能从Shell类一路调用会Window

#### [Flutter渲染机制—GPU线程](http://gityuan.com/2019/06/16/flutter_gpu_draw/)
- GPU线程是指运行着GPU Task Runner的名叫GPU的线程，其实依然是在CPU上运行，用于将UI线程传递过来的layer tree转换为GPU命令，并发送到GPU

- GPU渲染原理
    - GPU线程的主要工作是将layer tree进行光栅化再发送给GPU，其中最为核心方法ScopedFrame::Raster()，主要工作如下：
        - LayerTree::Preroll：绘制前的准备工作
        - LayerTree::Paint：嵌套调用各个不同的layer的绘制方法
        - SkCanvas::Flush：将数据flush到GPU，需要注意saveLayer的耗时
        - AndoridContextGL::SwapBuffers：缓存交换操作

- 渲染过程是生产者-消费者模式
    - 当管道中待处理的光栅化任务等于2个的时候(池子满了)，则UI线程无法执行Animator::BeginFrame()，而是等下一次Vsync信号再尝试执行
    - 当管道中没有待处理的光栅化任务的时候(池子空了)，则GPU线程无法执行Rasterizer::Draw()，而是直接返回，等待UI线程向其添加任务。

- Timeline说明
    - UI线程是PipelineProduce，对应的GPU线程是PipelineConsume，贯穿整个Rasterizer::onDraw过程

- GPU线程绘制流程
    - Flutter渲染机制在UI线程执行到compositeFrame()过程经过多层调用，将栅格化的任务Post到GPU线程来执行。GPU线程一旦空闲则会执行Rasterizer的draw()操作。图中LayerTree::Paint()过程是一个比较重要的操作，会嵌套调用不同layer的Paint过程，比如TransformLayer，PhysicalShapeLayer，ClipRectLayer，PictureLayer等都执行完成会执行flush()将数据发送给GPU。

- 三种不同的AndroidSurface
    - 硬件Vsync方式，且开启Vulkan，则采用AndroidSurfaceVulkan，这是当前默认的方式
    - 硬件Vsync方式，未开启Vulkan，则采用AndroidSurfaceGL
    - 使用软件模拟的Vsync方式，则采用AndroidSurfaceSoftware

- ContainerLayer9个子类组合成为了一个layerTree：
    - ClipRectLayer：矩形裁剪层，可指定矩形和裁剪行为参数，四种行为：Clip.none/hardEdge/antiAlias/antiAliasWithSaveLayer
    - ClipRRectLayer：圆角矩形裁剪层，可指定圆角矩形和裁剪行为参数
    - ClipPathLayer：路径裁剪层，可指定路径和裁剪行为参数
    - OpacityLayer：透明层，可指定透明度和偏移量参数，其中偏移量是指从画布坐标系圆点到调用者坐标系圆点的偏移量
    - ShaderMaskLayer：着色层， 可指定着色器、矩阵和混合模式参数
    - ColorFilterLayer：颜色过滤层， 可指定颜色和混合模式参数
    - TransformLayer：变换图层，可指定转换矩阵参数
    - BackdropFilterLayer：背景过滤层，可指定背景图参数
    - PhysicalShapeLayer：物理形状层，可指定颜色等八个参数

#### [深入理解Flutter引擎启动](http://gityuan.com/2019/06/22/flutter_booting/)
- FlutterApplication启动过程
    - Andorid应用在启动的时候会执行FlutterApplication.onCreate()方法，里面调用FlutterMain.startInitialization()方法，主要工作如下：
        - 调用FlutterLoader的startInitialization()方法，先通过looper判断是不是出于主线程中，不是的话直接抛出异常
        - 初始化配置参数
        - 获取应用根目录下的所有assets资源路径，提取产物资源，加载到内存中
        - 加载flutter库
            - Android进程自身会创建JavaVM，这里会将当前进程的JavaVM实例保存到静态变量中，再将当前线程和JavaVM建立关联
            - 注册FlutterMain的JNI方法
            - 注册PlatformViewAndroid的以为了方法，完成Java和C++的一些方法互调
            - 注册VsyncWaiter的nativeOnVsync()用于Java调用C++，asyncWaitForVsync()用于C++调用Java
        - 通过FlutterJNI记录FlutterApplication的启动耗时记录

- FlutterActivity启动过程（基于Channel master, v1.18.0-5.0.pre.46，原文基于Flutter1.5，略有差异，建议直接查看原文）
    - FlutterActivity对应FlutterActivityAndFragmentDelegate代理类，工作都交给这个代理类去实现,FlutterActivity中onCreate方法中有以下几句代码:
        - `this.delegate = new FlutterActivityAndFragmentDelegate(this);`：创建一个代理类，其中的this参数为一个Host接口，在FlutterActivityAndFragmentDelegate中定义的
        - `this.delegate.onAttach(this);`：调用代理类的onAttach()方法，里面会确保绑定了Flutter引擎并初始化完成
        - `this.delegate.onActivityCreated(savedInstanceState);`：调用代理类的onActivityCreated()方法
        - `this.setContentView(this.createFlutterView());`：调用代理类的onCreateView方法，创建FlutterSplashView
    - onCreate执行完后，FlutterActivity会调用onStart，代理类中的onStart方法中会调用`doInitialFlutterViewRun()`方法，里面应该就是原文作者说的加载Dart代码，然后经过层层调用开始执行Dart层的main方法， 执行runApp()过程。 
    - 上面说的代理类的生命周期划分是为了兼容FlutterFragment，除了onCreate，其他生命周期都一致(说的是什么话。。。)
    - 要开始啃C++吗？好像没啥太大的必要？

- Flutter引擎启动流程
    - 过程就不看了， 晕C++
    - 结论是，每一个FlutterActivity都有相对应的FlutterVIew、AndroidShellHolder、Shell、Engine、Animator、PlatformViewAndroid、RuntimeController、Window等对象，每一个进程Dart独有一份。
    - 这里可以猜一下，FlutterFragment和FlutterActivity也类似，但是这里进程有点疑问，如果一个页面组合了多个FlutterFragment，里面就有多个Dart进程？ TODO 

#### [深入理解Dart虚拟机启动](http://gityuan.com/2019/06/23/dart-vm/)
- Dart虚拟机概述
    - Dart虚拟机拥有自己的Isolate，完全由虚拟机自己管理，Flutter引擎也无法直接访问相关操作，而是由Root Isolate通过Dart的C++调用，或者是发送消息通知的方式，将UI渲染相关的任务调教到UI Task Runner执行，这样就可以跟Flutter引擎相关模块进行交互。
    - Isolate直接内存并不共享，而是通过Port方式通信，每个Isolate是有自己的内存以及相应的线程载体
    - Dart没有共享内存的并发，没有竞争的可能性，不需要加锁，也没有死锁风向。Dart程序的并发需要依赖多个Isolate来实现。

- 一个进程只有一个Dart虚拟机，所有Shell共享该进程中的Dart虚拟机。
- 每个Engine对应需要一个Isolate对象。

#### [深入理解Flutter应用启动](http://gityuan.com/2019/06/29/flutter_run_app/)
- 参考其他[Flutter Dart Framework原理简解](https://www.stephenw.cc/2018/05/28/flutter-dart-framework/)
- 从runApp()开始
    - `WidgetsFlutterBinding.ensureInitialized()`
        - WidgetsFlutterBinding是一个单例模式，负责创建WidgetsFlutterBinding对象，该对象类继承多个父类，父类方法相同， 则后面的会覆盖前面的，注意顺序
            - BindingBase：抽象基类，用来调用每个Binding的initInstances方法进行初始化
            - GestureBinding：绑定手势事件，用于检测应用的各种手势相关操作
            - SchedulerBinding：绑定帧绘制回调函数，以及widget生命周期相关事件
            - ServicesBinding：绑定平台服务消息，注册Dart层和C++层的消息传输服务
            - PaintingBinding：绑定绘制操作
            - SemanticsBinding：绑定语义树
            - RendererBinding：绑定渲染树
            - WidgetsBinding：绑定组件树
    - `..scheduleAttachRootWidget(app)`：遍历挂载整个视图树，并建立Widget、Element、RenderObject之间的连接与关系，这里的Element的具体类型为：RenderObjectToWidgetElement
    - `..scheduleWarmUpFrame();`：调度预热帧，执行帧绘制方法handleBeginFrame和handleDrawFrame。

- MyApp是用户定义的根Widget，为了建立三棵树的关系，RenderObjectToWidgetAdapter起到重要的桥接功能，该类的createElement方法创建RenderObjectToWidgetElement对象，createRenderObject()方法获取的是RenderView。

#### [深入理解setState更新机制](http://gityuan.com/2019/07/06/flutter_set_state/)
- setState()不应该在dispose()之后调用，可以通过mounted属性值来判断父widget中是否包含该widget

- setState()过程主要是：记录所有的脏元素，添加到BuildOwner对象的_dirtyElements成员变量，然后调用scheduleFrame来注册Vsync回调。 当下一次vsync信号的到来时会执行handleBeginFrame()和handleDrawFrame()来更新UI。

- SchedulerPhase五个枚举值含义：
    - idle：没有政治处理的帧，可能正在执行的是WIdgetsBinding.scheduleTask等其他的回调
    - transientCallbacks：SchedulerBinding.handleBeginFrame过程， 处理动画状态更新
    - midFrameMicrotasks：处理transientCallbacks阶段触发的微任务（Microtasks）
    - persistentCallbacks：WidgetsBinding.drawFrame和SchedulerBinding.handleDrawFrame过程，build/layout/paint流水线工作
    - posFrameCallbacks：主要是清理和计划执行下一帧的工作

#### [深入理解Flutter动画原理](http://gityuan.com/2019/07/13/flutter_animator/)
- Flutter动画分类：
    - 补间动画
    - 物理动画：遵循物理学定了的动画，实现了弹簧、阻尼、中立三种物理效果

- 核心类：
    - Animation：核心
    - AnimationController：管理Animation
    - CurveAnimation：过程是非线性曲线
    - Tween：补间动画
    - Listeners和StatusListener：用于监听动画状态改变

- AnimationStatus枚举类型
    - dismissed：动画在开始时停止
    - forward：从头到尾绘制动画
    - reverse：反向绘制动画，从尾到头
    - complete：结束时停止

- 原理分析：
    - AnimationController初始过程一般都是设置duration和vsync初值，调用类型为TickerProvider的vsync对象的createTicker()方法来创建Ticker对象

- TickerPRovider两个子类区别是，是否支持创建多个TickerProvider

#### [深入理解Flutter消息机制 - 这里看的不是很了解，然后大部分都是C++代码，有疑问](http://gityuan.com/2019/07/20/flutter_message_loop/)
- MessageLoop在什么时候启动的？
    - FLutter引擎启动阶段会创建AndroidShellHolder对象，在该过程会执行ThreadHost初始化，MessageLoop便是在这个阶段启动的。

- Fluter引擎启动过程会创建哪些线程？
    - UI/GPU/IO

- MessageLoop的消息循环过程， 会同时消费Dart层的Microtask和引擎层Task
- Flutter引擎启动过程，会创建UI/GPU/IO这三个线程，并且会为每个线程一次创建MessageLoop对象，启动后处于epoll_wait等待状态。(这里说明每个线程都会有自己的MessageLoop对象。)
- 在引擎中每次消费任务时调用FlushTasks()方法，遍历整个延迟任务队列，将到期的任务加入invocations，然后会遍历执行FlushMicrotaskNow()来消费所有的微任务。

#### [深入理解Flutter异步Future机制](http://gityuan.com/2019/07/21/flutter_future/)
- Dart是单线程执行模型，Dart应用在其主isolate执行应用的main()方法时开始运行，当main()执行完成后，主isolate所在的线程再逐个处理队列中的任务，包括但不限于通过Future所创建的任务，但整个过程都运行在同一个单线程。
- Dart的并行操作需要isolate或者worker
- Future创建过程
    - 创建Timer，并将_timer._handleMessage()放入到_handlerMap
    - 对于无延迟的Future则会将该Timer加入到ZeroTimer链表尾部
    - 创建的新端口号port和回调handler一起记录到一条的entry，再把该entry加入到map的第port槽位
    - 创建ReceivePort和SendPort对象

- Future处理过程
    - 任务发送过程
        - 通过message记录的port值从map中找到handler，再通过该handler找到的MessageHandler来发送消息
        - 根据message优先级，如果是普通消息，则加入到queue队列；如果是OOB消息，则加入到oob_queue队列
        - 通过PostTask来向UI线程发送任务
    - 任务接收过程
        - 先从oob_queue队列中取出头部的消息，当该消息为空且接收到待处理的优先级别为普通消息，则从queue队列取出头部消息
        - 通过port从_handlerMap中找到Dart层回调方法_timer._handleMessage()
        - 再从ZeroTImer链表中添加所有时间已过期的消息以及无延迟的消息
        - 然后回调执行真正的future中定义的业务逻辑代码

- Future操作只是异步执行，不会阻塞本次在UI线程的执行，但是其执行关键点中通过TaskRunner::PostTask()将Task放入UI线程，意味着如果Future中存在耗时操作，依然是影响UI线程的后续渲染绘制流畅度，所以不能在Future中做耗时操作。为保证应用的即时响应，应该将任务放到独立线程的isolate或者worker中。

#### [深入理解Flutter的Isolate创建过程](http://gityuan.com/2019/07/27/flutter-isolate/)
- Root isolate负责UI渲染以及用户交互操作，需要即时响应，当存在耗时操作的时候，必须创建新的isolate，否则UI渲染会被阻塞。
- 创建isolate的方法便是isolate.spawn()。
- Isolate创建流程
    - 创建IsolateSpawnState对象、SpawnIsolateTask对象
    - Dart虚拟机创建过程会初始化线程池ThreadPool，从该线程池中查找worker
        - 存在空闲状态的worker，则调用Notify唤醒该worker处理刚创建的SpawnIsolateTask对象
        - 没有空闲状态的worker，则新建worker并创建响应的线程，该线程停留在worker的loop()过程
    - 对于worker的loop过程说明：
        - 当线程池ThreadPool关闭，则会退出该worker的loop()过程
        - 当连续等待超过5秒，则释放并退出该worker的loop()过程
        - 除以上两种情况外，当收到MonitorLocker的Notify过程，则会继续开始处理task，task可以是SpawnIsolateTask、MessageHandlerTask、ParallelMarkTask等Task
    - 创建isolate对象
    - 调用worker->setTask()向worker中添加task，worker的loop()过程取出并执行  

- 耗时操作需要创建新的isolate，isolate采用的是同一进程内的多线程间内存不共享的设计方案。
    - 避免线程竞争出现。
    - 因为isolate之间无法共享内存数据，因此设计了SendPort/ReveivePort的Port端口通信机制，让各isolate间彼此独立，但又可以相互的通信。Port通信的实现原理是异步消息机制
    - Dart的isolate是由Dart VM管理的，Flutter引擎无法直接访问。

- 每次创建新的isolate的同时会通过pthread_create()来创建一个OSThread线程，isolate的工作便是在该线程中运行，可以理解为isolate是一种内存不共享的线程，isolate只是在系统现在线程基础之上做了一层份额改装而已。可通过Dart_CreateIsolate和Dart_ShutdownIsolate分别对应isolate的创建和关闭。

#### [搭建Flutter Engine源码编译环境](http://gityuan.com/2019/08/03/flutter_engine_setup/)
#### [搭建Flutter Framework开发环境](http://gityuan.com/2019/08/04/flutter_framework_setup/)

#### [深入理解Flutter的Platform Channel机制](http://gityuan.com/2019/08/10/flutter_channel/)
- 核心原理
    - Flutter应用通过Platform Channel将传递的数据编码成消息的形式，跨线程发送到该应用缩在的宿主
    - 宿主接收到Platform Channel的消息后，调用相应平台的API，也就是原生编程语言来执行相应方法
    - 执行完成后将结果数据通过同样的方式原路返回给应用程序的Flutter部分。
    - 整个过程的消息和响应是异步的，所以不会阻塞用户界面。

- Flutter提供的三种不同的Channel
    - BasicMessageChannel：传递字符串和半结构化数据
    - MethodChannel：方法调用
    - EventChannel：数据流的通信

- MethodChannel的执行流程涉及到主线程和UI线程的交互，代码从Dart到C++再到Java层，执行完相应逻辑后原路返回，从Java层到C++层再到Dart层

#### [源码解读Flutter tools机制](http://gityuan.com/2019/09/01/flutter_tool/)

#### [源码解读Flutter run机制](http://gityuan.com/2019/09/07/flutter_run/)

#### [Flutter前端编译frontend_server](http://gityuan.com/2019/09/14/flutter_frontend_server/)

#### [Flutter机器码生成gen_snapshot](http://gityuan.com/2019/09/21/flutter_gen_snapshot/)

#### [解读Dart虚拟机的参数列表](http://gityuan.com/2019/09/22/dartvm_flags/)

#### [Dart虚拟机运行原理](http://gityuan.com/2019/10/05/dart_vm/)
- Dart VM为高级编程语言Dart提供执行环境，但是Dart在虚拟机上执行时，不仅仅可以采用解释执行或者JIT编译，还可以使用Dart虚拟机的AOT管道将Dart代码编译为机器代码，然后运行在Dart虚拟机的精简版环境，称之为预编译运行时环境，环境不包含任何编译器组件，且无法动态加载Dart源代码
- Dart VM执行代码的方式：
    - 源码或者Kernel二进制(JIT)
    - snapshot
        - AOT snapshot
        - APPJIT snapshot

- Isolate组成
    - Isolate中的Heap管理GC内存中所有对象的内存存储分配
    - vm isolate是一个伪isolate，里面包含不可变对象，如null/true/false等
    - Isolate中的Heap能引用vm isolate Heap中的对象的，但是vm isolate不能引用Isolate中的Heap
    - Isolate彼此之间不能相互引用
    - 每个Isolate都有一个执行Dart代码的Mutator Thread，还有很多的Hepler Thread用来处理虚拟机内部任务，如GC、JIT等

- Isolate拥有内存Heap和控制线程，虚拟机中可以有很多Isolate，但是彼此之间不能直接通信，只能通过Dart特有的端口通信。
- Isolate拥有一个Mutator控制线程，还有一些Hepler线程：
    - 后台JIT编译线程
    - GC清理线程
    - GC编发标记线程

- 线程和Isolate的关系
    - 同一个线程在同一时间只能进入一个Isolate，当需要进入另一个Isolate则必须先退出当前Isolate
    - 一次只能有一个Mutator线程关联对应的Isolate，Mutator线程是执行Dart代码并使用虚拟机的公共C语言API的线程。

- 虚拟机采用线程池的方式来管理线程
    - 核心变量
        - all_workers_：记录所有的workers
        - idle_workers_：记录所有空闲的workers
        - count_started_：记录该线程池的历史累计启动workers个数
        - count_stopped_：记录该线程池的历史累计关闭workers个数
        - count_running_：记录该线程池当前正在运行的worker个数
        - count_idle_：记录该线程池当前处于空闲的worker个数，也就是idle_workers的长度
    - 核心方法
        - Run(Task*)
        - Shutdown()
        - SetIdleLocked(Worker*)
        - ReleaseIdleWorker(Worker*)