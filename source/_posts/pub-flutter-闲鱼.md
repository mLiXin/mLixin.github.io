---
title: Flutter学习笔记 - 闲鱼公众号
date: 2018-05-10 17:23:05
tags:
- Flutter
categories:
- Flutter
- 学习笔记
---
#### 摘要
闲鱼技术 公众号Flutter相关文章学习笔记
<!--more-->
#### [Android Flutter内存初探](https://mp.weixin.qq.com/s/efKCpCtvvHDHUiAsizobBQ)
主要关注Dart VM内存分配和回收相关的部分

- Dart的线程是不共享内存的，各自的堆和栈都是隔离的，彼此通过消息通道来通信。Dart天然不存在数据竞争和变量状态同步的问题，整个Flutter Framework Widget的渲染过程都运行在一个isolate中。
- Dart VM将内存管理分为新生代和老年代
    - 新生代(New Generation)
        - 初次分配的对象的都位于新生代中，该区域主要存放内存较小并且生命周期较短的对象，比如局部变量。
        - 新生代会频繁执行内存回收(GC)，回收采用“复制-清除”算法，将内存分为两块，运行时每次只使用其中一块，另一块备用，当发生GC的时候，当前内存使用的内存块中存活的对象拷贝到备用内存块中，然后清除当前使用内存块，最后交互两块内存的角色。
    - 老年代(Old Generation)
        - 新生代GC留下的对象会被转移到老年代中(这里可能还是和JVM一样会有年龄限制的，不是每次GC留下的对象都会马上转移到老年代中)。老年代存放生命力周期较长，内存较大的对象。
        - 老年代GC采用`标记-清除`算法，分成标记和清除两个阶段。标记阶段，所有线程参与并发的完成对回收对象的标记，降低标记阶段耗时；清除阶段，由GC线程负责清理回收对象，和应用线程同时执行，不影响应用运行。

- Android和Flutter加载图片使用的内存有什么区别？
    - Android原生的ImageView在6.0和7.0版本使用的是Java虚拟机内存，而在Android8.0是使用的Native内存
    - Flutter中的Image Widget使用的内存是Graphics(图形缓冲区队列向屏幕显示像素所使用的内存，这是CPU共享的内存，不是CPU专用内存)，不懂，反正不是Java虚拟机内存，不会出现OOM

- Flutter和原生混合开发的是时候，有两种方案可以实现：
    - 一个Activity里面启动一个新的Flutter View
    - 只用一个FlutterView，跳转的时候复用这个FlutterView
        - Flutter Framework中FlutterView是绑定Activity使用的，必须attach一个Activity，为了避免Activity泄露，可以在detach的时候传入mainActivity，因为运行过程中mainActivity是会一直存在的。
		- 复用FlutterView的时候会有问题，比如Activity切换的时候，就不得不将当前FlutterView detach掉给后面新建的Activity使用，会有空白闪动。

- Flutter首帧渲染耗时较高，优化思路是，预先将要使用的FlutterView加载好首帧，这样在真正使用的时候就很快了。

#### [深入了解Flutter界面开发](https://mp.weixin.qq.com/s/z2r2OmnY7r7dQrkO8ndkFQ)
- Widget、Element、RenderObject分别是什么？有什么关系？
    - Widget：存放渲染内容、视图布局信息，widget的属性最好是immutable的
    - Element：存放上下文，通过Element遍历视图树，Element同时持有Widget和RenderObject
    - RenderObject：根据Widget的布局属性进行layout，paint Widget传入的内容。

- 为什么widget都是immutable？
    - 界面开发是响应式编程，希望数据变更的时候，发送通知到对应的可变更节点，由上到下重新create widget树进行刷新。

- Widget重新创建，element树和renderObject树是否也重新创建？
    - Widget树创建非常轻量，不会带来想呢个问题，但是renderObject涉及到layout、paint等复杂操作，是一个枕着在哪个的渲染的view，整个view树重新创建开销比较大，所以不会重新创建。

- State生命周期
    - initState
        - create之后，被insert到tree的时候调用
    - didUpdateWidget
        - 祖先节点rebuild widget的时候调用
    - deactivate
        - widget被remove的时候调用，一个widget从tree中remove掉，可以在dispose接口被调用前重新insert到一个新的tree中
    - didChangeDependencies
        - initState之后立刻调用
        - 依赖的InheritedWidget rebuild，会触发该接口被调用
    - build
        - initState之后
        - didUpdateWidget之后
        - setState之后
        - 当前State的dependency改变之后
        - deactivate被调用，然后重新将其插入到一另外一个location之后
    - dispose()
        - widget彻底销毁时调用
    - reassemble
        - hot Reload

- 如何触发树的更新？
    - 全局更新，runApp(rootWidget)
    - 局部子树更新，setState()

- Layout的size计算过程
    - parent传constrains给child，child根据自身渲染内容返回size

#### [深入理解flutter的编译原理与优化](https://mp.weixin.qq.com/s/vlHt8jxbdzBqJZDobpsFVw)
- TODO

#### [深入理解Flutter引擎线程模式](https://mp.weixin.qq.com/s/hZ5PUvPpMlEYBAJggGnJsw)
- TODO 可以多看几次
- Flutter比较其他跨平台方案，有哪些高性能特性？
    - FLutter在Release模式下直接将Dart编译成本地机器码，避免了代码解释运行的性能消耗
    - Dart本身针对高频率循环刷新在内存层面进行了优化
    - Flutter实现了自己的图形绘制，避免了Native桥接

- Flutter中如何管理线程？
    - Engine自己不创建管理线程，线程的创建和管理由embedder负责，Embedder指的是将引擎移植到平台的中间层代码。 

- Flutter要求Embedder提供的四个Task Runner分别是什么？
    - Platform Task Runner
        - 可以理解为主线程，其实和其他线程没区别。一般来说，一个Flutter应用启动时会创建一个Engine实例，Engine创建的时候会创建一个线程供Platform Runner使用
        - 不仅仅处理与Engine交互，还处理来自平台的消息
        - 阻塞Platform Thread不会直接导致Flutter应用的卡顿。长时间卡住的Platform Thread应用有可能会被系统Watchdog强行杀死
    - UI Task Runner Thread（Dart Runner）
        - 被Flutter Engine用于执行Dart root isolate代码
        - 处理渲染相关的逻辑、来自Native Plugins的消息响应
        - 生成平台不相关的LayerTree传给GPU Task Runner
        - 过载会导致Flutter应用卡顿
    - GPU Task Runner
        - 执行设备GPU的相关调用，将LayerTree提供的信息转化为实际的GPU指令。
        - 过载会导致Flutter应用卡顿
    - IO Task Runner 
        - 从图片存储中读取压缩的图片格式，将图片数据进行处理为GPU Runner的渲染做好准备

- Dart中的isolate机制
    - 定义
        - Isolate有自己的内存和单线程控制的运行实体，Isolate之间的内存在逻辑上是隔离的，isolate中的代码是按顺序执行的，任何Dart程序的并发都是运行多个isolate的结果。因为不共享内存，没有竞争的可能性，不需要锁，不用担心死锁。
    - 通信
        - 只能通过Port异步传递消息
    - 与普通线程的区别
        - 线程之间是可以共享内存的，但是isolate没有
    - 实现
        - 初始化isolate数据结构
        - 初始化堆内存heap
        - 进入新创建的isolate，使用跟isolate一对一的线程运行isolate
        - 配置Port
        - 配置消息处理机制
        - 配置Debugger
        - 将isolate注册到全局监控器(Monitor)

#### [Flutter Plugin调用Native APIs](https://mp.weixin.qq.com/s/WORru3f5rfABFMoxQ_2nYw)

- Flutter与其他开发框架相比有什么优点？
    - 使用AOT预编译代码为机器码，所以运行效率更高
    - 没有使用底层的原生控件，而是使用Skia渲染引擎绘制而成，不依赖底层控件，多端一致性较好
    - 扩展性强，可以通过Plugin与Native进行通信

- Flutter中的MethodChannel如何实现？
    - Plugin Flutter部分
        - MethodChannel：Flutter api调用Native APis
        - EventChannel：Native调用Flutter App
    - Plugin Android部分
        - 新版本中已经在FlutterActivity中注册过了，只需要重写configureFlutterEngine，重新生成MethodChannel实例并实现即可。

```Dart
    // metehodChannel
    static const MethodChannel _methodChannel = const MethodChannel('samples.flutter.io/battery');
    int result = await _methodChannel.invokeMethod('',{'paramName':'paramValue'，})
    // EventChannle
    static const EventChannel _eventChannel = const EventChannel('samples.flutter.io/charging');
    void listenNativeEvent(){
        _eventChannel.receiveBroadcastStream().listen(_onEvent,onError:_onError);
    }   
    
    void _onEvent(Object event){
    }
    void _onError(Object error){
    }
```
#### [Flutter混合工程改造实践](https://mp.weixin.qq.com/s/Q1z6Mal2pZbequxk5I5UYA)
- TODO 以ios视角来讨论的，暂时不太能立即理解。
- 将Flutter工程包含已有的Native工程，会带来哪些问题？
    - 构建打包问题
        - 引入Flutter后，Native工程对其有依赖和耦合，从而无法独立编译构建。
    - 混合编译带来的开发效率的降低
        - 转型Flutter的过程中必然有许多业务仍使用Native进行开发，工程结构的改动会使开发无法在纯Native环境下进行。

#### [Release Flutter的最后一公里](https://mp.weixin.qq.com/s/xV-FGR9o2ODLFJFq4YwnKg)

1. 选择Dart的原因，有哪些优势？
    - 易学
    - AOT编译、JIT编译
    - 可无锁进行对象分配和垃圾回收

2. 混合栈管理
    - 抽取单一FlutterView或FlutterNativeView，后续没启动一个Activity都对FLutterView或FlutterNativeView进行复用。

3. UI渲染原理
    - GPU的Vsync信号同步到UI线程，UI线程使用Dart构建抽象的视图结构(LayerTree)，接着在GPU线程进行图层合成，且视图数据提供给Skia引擎进行渲染生成GPU数据，最终通过OpenGL或Vulkan提供给GPU，有次可以看出Flutter并不关心显示器、视频控制器以及GPU具体工作细节，它只关心Vsync信号，以求尽可能快的在两个Vsync信号之间计算并合成视图数据并提供给GPU。

4. Flutter播放器可以如何改进？
    - 设置一个EventChannel，用于向Flutter通知视频状态变化
    - 设置一个MethodChannel，用于控制video player
    - 设置一个FlutterTexture，用于显示视频帧
    - 从Native播放器中提取出video frame，贴到FlutterTexture

#### [Flutter React编程范式实践](https://mp.weixin.qq.com/s/GRHvM0BHe2D9Qwb_nW0New)
- TODO
- 
#### [闲鱼Fultter混合工程持续集成的最佳实践](https://mp.weixin.qq.com/s/5opwrgVr48e0YDYtEWFXZQ)
1. Flutter依赖抽取模块，将Flutter的依赖抽取为一个Flutter依赖库发布到远程， 供纯Native工程引用。
2. Native工程对Flutter工程有哪些依赖？
    - Flutter库和引擎
        - Flutter的Framework库和引擎库
    - Flutter工程
        - 自己实现的Flutter模块功能，主要为Flutter工程下lib目录下的dart代码
    - 自己实现的Flutter Plugin

3. Android的Flutter依赖文件都有哪些?
    - Flutter库和引擎
    - Flutter工程产物
        - isolate_snapshot_data 应用程序数据段
        - isolate_snapshot_instr 应用程序指令段
        - wm_snapshot_data VM虚拟机数据段
        - vm_snapshot_instr VM虚拟机指令段
        - flutter_assets
    - Flutter Plugin
        - 各个Plugin编译出来的aar文件

4. Flutter工程中的Android打包如何实现？
    - 在Android的Gradle任务中插入了一个flutter.gradle的任务，而这个flutter.gradle主要做了三件事：
        - 增加flutter.jar的依赖
        - 插入Flutter Plugin的编译依赖
        - 插入Flutter工程的编译任务，最终将产物(连个isolate_snapshot文件、两个vm_snapshot文件和flutter_Assets文件夹)拷贝到mergeAssets.outputDir，最终merge到APK的assets目录下

5. 如何抽取Android的Flutter依赖？
    - 编译Flutter工程
    - 将flutter.jar和Flutter工程的产物打包成一个aar
    - 将这个aar和Flutter Plugin编译出来的aar一起发布到maven仓库
    - 纯粹的Native项目只需要compile我们发布到maven的aar即可。

6. 自动化持续集成如何实现？
    - 每次需要构建纯粹Native工程前自动完成Flutter工程对应的远程库的编译发布工作，整个过程不需要人工干预
    - 在开发测试阶段，采用五段式版本号，最后一位自动递增产生，这样就可以保证测试阶段的所有并行开发的Flutter库的版本号不会产生冲突
    - 发布阶段采用三段式或四段式的版本号，可以和APP版本号保持一致，便于后续问题追溯。

#### [Flutter新锐专家之路：工程研发体系篇](https://mp.weixin.qq.com/s/YMnzLGrUdjd1PFlkZdFMqQ)
- TODO 混合实战的时候看

#### [Flutter新锐专家之路：混合开发篇](https://mp.weixin.qq.com/s/1AMvmuckg9bEODqhULVhPQ)
- TODO 混合实战的时候再来看

#### [万万没想到-Flutter这样外接纹理](https://mp.weixin.qq.com/s/KkCsBvnRayvpXdI35J3fnw)
0. TODO 有些有点深，理解的不是很好
1. Flutter如何实现在Native和FlutterEngine实现UI的隔离？
    - 当Runtime完成Layout输出一个LayerTree之后，在管线中会遍历LayerTree的每一个叶子节点，每一个叶子节点最终会调用Skia引擎完成界面元素的绘制，在遍历完成后，再调用glSwapBuffer完成上屏操作。

2. Flutter中的Texture控件有什么意义？
    - 代表的是在这个控件上显示的数据，需要由Native提供

3. Flutter如何展示Native端大数据？
    - 使用Texture，通过外交纹理的方式，Flutter和Native传输的数据载体PixelBuffer，Native端的数据源(摄像头、播放器等)将数据写入PixelBuffer，Flutter拿到PixelBuffer以后转成OpenGLES Texture，交由Skia绘制

#### [深入理解Flutter Platform Channel](https://mp.weixin.qq.com/s/FT7UFbee1AtxmKt3iJgvyg)
0. Flutter与Native之间的消息传递，如果要了解细节，可以细看这篇。
1. Flutter有哪几种Channel？
    - BasicMessageChannel
        - 用于传递字符串和半结构化的信息
    - MethodChannel
        - 用于传递方法调用(method invocation)
    - EventChannel
        - 用于数据流(event streams)的通信
2. Channel的三个重要的成员变量？
    - name
        - String类型，代表Channel的名字，也是其唯一标识符
        - 当有消息从Flutter端发送到Platform端的时候，会根据其传递过来的channel name找到该channel对应的Handler
    - messager
        - BinaryMessenger类型，代表消息信使，是消息的发送与接收的工具
        - 通信使用的消息格式为二进制格式数据。
        - 初始化一个Channel，并向该Channel注册处理消息的Handler时，实际上会生成一个与只对应的BinaryMessageHandler，并以channel name为key，注册到Binarymessenger中。当Flutter端发送消息到BinaryMessenger时，BinaryMessenger会根据入参channel找到对应的BinaryMessagehandler，并交由其处理。
    - codec
        - MessageCodec类型或MethodCodec类型，代表消息的编解码器。用于二进制格式数据与基础数据之间的编解码。

3. Platform Channel的代码运行在什么线程？
    - 在Platform侧执行的额代码运行在Platform Task Runner中，在Flutter app侧的代码则运行在UI Task Runner中。在Android和iOS平台上，Platform Task Runner跑在主线程上，所以不能在Platform端的Handler中处理耗时操作。

4. Platform Channel是否线程安全？
    - 不是线程安全的。
    - Flutter Engine中多个组件是非线程安全的，故跟Flutter Engine的所有交互必须发生在Platform Thread。故在将Platform端的消息处理结果回传给Flutter端的时候，需要确保回调函数是在Platform Thread中执行。

5. Platform Channel是否支持大内存数据块的传递？
    - 支持。
    - 当需要传递大内存数据块的时候，使用BasicMessageChannel以及BinaryCodec。而整个数据传递的过程中，唯一出现数据拷贝的位置为native二进制数据转化为Dart语言二进制数据。若二进制数据大于阈值时则不会拷贝数据，直接转化，否则拷贝一份再转化。

6. 如何将Platform Channel原理应用到开发工作中？
    - 使用BasicMessageChannel实现Flutter端使用Platform端资源。
    - Flutter端将图片资源名name 传递给Platform端，Native端使用Platform端接收到name后，根据name定位到图片资源，并将该图片资源以为禁止数据格式，通过BasicMessageChannel，传递会Flutter端。

#### [Flutter快速上车之Widget](https://mp.weixin.qq.com/s/kAWPj97w5NfiqAYEpi3zVA)
1. ImageCache默认1000张；可以通过url增加后缀的方式实现cdn优化
2. 如何知道App的生命周期？
    - 通过WidgetsBindingObserver的didChangeApplifecycleState获取。常用状态包含以下几个：
        - resumed：可见，并能响应用户的输入
        - inactive：处于并不活动状态，无法处理用户响应
        - paused：不可见、不能响应用户的输入，在后台继续活动中

#### [Flutter之禅 内存优化篇](https://mp.weixin.qq.com/s/mHBz56OWKBB_g9YavVKTbQ)
1. 使用Dart Observatory观察Dart Image对象的内存情况
2. Dart语言采用垃圾回收机制来管理分配的内存，VM层面的垃圾回收可信
3. Flutter里面所有的图片都是经过ImageProvider来获取的，ImageProvider在获取图片的时候会调用一个Resolve接口，而这个接口会首先查询IamgeCache去读取图片，如果不存在缓存，就new Image实例出来。
4. ImageCache中的缓存实现机制？
    - Flutter中的Image是用Map实现的基于LRU算法缓存。ImageCache缓存的是ImageStream对象，即缓存的是一个异步加载的图片对象，而缓存没有对占用内存总量做限制，而是采用默认最大限制1000个对象。导致穿的问题是，在图片加载解码完成之前，无法知道到底要消耗多少内存，至少在Flutter这个Cache实现中没有处理。
    - 优化的话，就是根据机型的物理内存去做缓存大小的适配，设置ImageCache的合理限制。

#### [揭秘Flutter Hot Reload（基础篇）](https://mp.weixin.qq.com/s/Z9QPUJ3dZy2btBOlhSfyQw)
1. TODO 暂时没必要看

#### [Flutter瘦身大作战](https://mp.weixin.qq.com/s/IIoaY2uw6Bqzc9XWI91YFw)
1. 基于iOS端，暂时略过，需要再看。

#### [Flutter中嵌入Native组件的正确姿势是...](https://mp.weixin.qq.com/s/JM_AB0vVH0uOY7v0ToDamw)
1. 在Flutter中嵌入原生组件，如何实现？
    - AndroidView
2. AndroidView的实现原理
    - TODO 看的不是很顺利

#### [关于Flutter初始化，我必须告诉你的是...（干货）](https://mp.weixin.qq.com/s/5JYzHWmczimYy3QMlLUJ4w)
1. 很多变动，参考意义不大。

#### [做了2个多月的设计和编码，我梳理了Flutter动态化的方案对比及最佳实现](https://mp.weixin.qq.com/s/N5ih-DY5TuKyn_a0P2mz0Q)
1. Flutter页面动态组件

#### [Flutter路由管理代码这么长长长长长，阿里工程师怎么高效解决？（实用）](https://mp.weixin.qq.com/s/YgE9lwEHb31WOWyraHL35w)
1. 使用注解生成映射表，现在已经没有维护，略过。

#### [Flutter Exception降到万分之几的秘密](https://mp.weixin.qq.com/s/JiJ3XwIq_ADM457M6CBSxA)
#### [如何在Flutter上优雅地序列化一个对象（实用）](https://mp.weixin.qq.com/s/W5kQBe0vlnkG7VwIVAmnRA)
1. json_serializable太繁琐，而且大量使用as会给性能和最终产物大小产生不小的影响。
2. Dart中没有反射，如何实现反序列化对象的创建问题？
    - 类似C++的那种回调函数解决
3. 一顿操作猛如虎，一看github没开源。

#### [已开源|码上用它开始Flutter混合开发——FlutterBoost](https://mp.weixin.qq.com/s/v-wwruadJntX1n-YuMPC7g)
1. 如果Flutter与Native混合开发中，使用多引擎的话会导致的问题
    - 冗余的资源问题
        - 每个引擎之间的isolate相互独立，每个引擎底层维护自己一份图片缓存，内存压力会非常大
    - 插件注册的问题
        - 插件依赖Messenger传递消息，而目前Messenger是由FlutterViewController去实现的。如果有多个FLutterViewController，插件的注册和通信会变得非常混乱和难以维护。
    - Flutter Widget和Native的页面差异化问题
        - Flutter页面是widget，native的也没是vc，希望消除两者差异，否则在进行页面买点和其他一些统一操作的时候会遇到额外的复杂度
    - 增加页面之间通信的复杂度
        - 只有一个引擎实例，可以共享一个isolate，使用统一的编程框架进行widget之间的通信。

2. FlutterBoost方案的思路
    - 采用共享引擎的模式实现，由Native容器Container通过消息驱动Flutter页面容器Containner，从而达到NativeContainer与Flutter Container的同步目的。Flutter渲染的内容由Native容器去驱动。

3. TODO 研究一下FlutterBoost源码实现

#### [打通前后端逻辑，客户端Flutter代码一天上线](https://mp.weixin.qq.com/s/hFdBtDQo1TvvxBGHLV3Stw)
1. Flutter动态化方案
    - 官方方案：Code Push
        - DartVM在执行的时候会加载isolate_snapshot_data和isolate_snapshot_instr两个文件，通过动态更改这些文件，就能达到动态更新的目的。
    - 动态模板
        - 定义一套DSL，在端侧解析动态的创建View来实现动态化。闲鱼实现UI2Code，如果实现，可以通过UI2CODE将设计图转为Code，再通过DSL下发。完美。 

#### [燃烧我的卡路里——Flutter瘦内存、瘦包之图片渲染组件](https://mp.weixin.qq.com/s/QwNMm0P2z7RGJ_xzhto1RQ)
#### [Fish Redux中的Dispatch是怎么实现的？](https://mp.weixin.qq.com/s/4hJzGPH8OQ6hkthRFuisBQ)
#### [走近科学，探究阿里闲鱼团队通过数据提升Flutter体验的真相](https://mp.weixin.qq.com/s/26kY9rvRxVDkml2UeBnQfw)
#### [在闲鱼，我们如何用Dart做高效后端开发？](https://mp.weixin.qq.com/s/jAD3hacFMVcOv9GnAfCFOw)
#### [Flutter高内聚组件怎么做？闲鱼闲鱼打造开源高效方案！](https://mp.weixin.qq.com/s/hw24XYmMDNj1iWZ2GAxMiQ)
#### [一个优秀的可定制化Flutter相册组件，看这一篇就够了](https://mp.weixin.qq.com/s/ARKAvDn52irJmyw5tEeD0w)
#### [揭秘！一个高准确率的Flutter埋点框架如何设计](https://mp.weixin.qq.com/s/CMYi-f0-6nwZ4ZyV5K_lKA)
#### [如何低成本实现Flutter富文本，看着一篇就够了！](https://mp.weixin.qq.com/s/CGMwDXQbv_YbwEzblwGqRQ)
#### [编程界的“二向箔”——Dart元编程](https://mp.weixin.qq.com/s/-vEha279U54piV8PGKDzbA)
#### [如何在Flutter上实现高性能的动态模板渲染](https://mp.weixin.qq.com/s/fX6DtXYtKw0hFqf7t---eA)
#### [重磅|庖丁解牛之——Flutter for Web](https://mp.weixin.qq.com/s/krR2XsDXvakMlZWbV-VvSg)
#### [闲鱼公开多年Flutter武功秘籍（又又又开源了！）](https://mp.weixin.qq.com/s/8xOW0jh7sKCw19AZzI9QEw)
#### [即将开源|Flutter页面线上性能数据不再是谜](https://mp.weixin.qq.com/s/L_Hn8kdQsn4eRgrGGgTVJw)
#### [做一个高一致性、高性能的Flutter动态渲染，真的很难么？](https://mp.weixin.qq.com/s/R6IxJqawwbmlWvlwb3ZXww)
#### [怎样的Flutter Engine定制流程，才能实现真正“开箱即用”？](https://mp.weixin.qq.com/s/SB6p4fZuKCOvwtKvSzV1DA)
#### [Flutter+Serverless端到端研发架构实践](https://mp.weixin.qq.com/s/JHqHmb00JEMPSAQbau2FIw)
#### [闲鱼Flutter互动引擎系列——整体设计篇](https://mp.weixin.qq.com/s/oa-XUzWhhsz37Mj-Y6WkzA)
#### [基于Flutter+FaaS的业务框架思考与实践](https://mp.weixin.qq.com/s/yvrz8zMD4q_ngk54-PWK8A)
#### [闲鱼Flutter互动引擎系列——骨骼动画篇](https://mp.weixin.qq.com/s/mpfnA3vcnbaJPtoTdZNJ6g)
#### [FlutterBoost1.0到2.0，我一共做了这几件事...](https://mp.weixin.qq.com/s/cNtyeyIAPB_1TkvMS69znA)
#### [闲鱼Flutter图片框架架构演进（超详细）](https://mp.weixin.qq.com/s/98BxqW5QDHXLKMwHX_E7EQ)
#### [一个易迁移、兼容性高的 Flutter 富文本方案](https://mp.weixin.qq.com/s/uqxLb5ToMdi9sqL6gDRW_g)
#### [复杂业务如何保证Flutter的高性能高流畅度？](https://mp.weixin.qq.com/s/iXFa9C68gUHr7PL8NHnZUA)
- Flutter渲染原理
    - 根据Widget生成Element，然后创建相应的RenderObject并关联到Element.renderObject属性上，在通过RenderObject来完成布局排列和绘制
    - 当需要更新UI的时候，Framework通知Engine，Engine会等到下一个Vsync信号到达的时候通知Framework进行animate、build、layout、paint，最后生成LayerTree提交给Engine，Engine会把Layer进行组合，生成纹理，最后提交数据给GPU，GPU经过处理后在显示器上面显示

- 如果Text中内有发生了变化，会触发哪些操作？
    - Widget是不可改变的，需要重新创建一颗新树，从build开始，然后对上一帧的element树进行遍历，调用updateChild，看子节点类型跟之前是不是一样，不一样的话，就把子节点扔掉，创造一个新的；一样的话就做内容更新。对renderObject做updateRenderObject操作，该操作内部会判断现在的节点跟上一帧是不是有改动，有改动会标记dirty，重新layout、paint，在生成新的layer交给GPU

- 性能分析工具及方法(真机+profile模式下运行，debug没意义)
    - performance overlay，Flutter Inspector
    - Dart DevTool，Andorid studio底部的菜单按钮
    - debug调试工具

- 优化方法
    - 提高build效率，部分刷新，可以降低widgetTree遍历的出发点，将setState刷新数据尽量下发到底层节点。
    - 提高paint效率。利用RepaintBoundary，经常发生显示变化的内容提供一个新的隔离layer，新的layer paint不会影响到其他layer

- 注意点
    - 减少build中逻辑处理，因为widget在页面刷新过程中随时会通知build重建，build调用频繁，应该只处理跟UI相关的逻辑。
    - 减少saveLayer(ShaderMask、ColorFilter、Text Overflow)、clipPath的使用，saveLayer会在GPU中分配一块新的绘图缓冲区，切换绘图目标，这个操作是在GPU中非常耗时的，clipPath会影响每个绘图指令，做相交操作，之外的部分剔除掉，也是个耗时操作
    - 减少Opacity Widget使用，尤其是在动画中，因为它会导致widget每一帧都会被重建，可以用AnimatedOpacity或FadeInImage进行代替