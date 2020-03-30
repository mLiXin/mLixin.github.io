---
title: Flutter学习笔记 - 闲鱼公众号
date: 2018-05-10 17:23:05
tags:
- Flutter
- 学习笔记
categories:
- Flutter
---
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
1. Flutter框架
    - FrameWork
        - Material/Cupertino
        - Widgets
        - Rendering
        - Animationg/Painting/Gestures
        - Foundation
    - Engine
        - Skia/Dart/Text

2. Rendering Pipeline
    - GPU发出Vsync信号，会经过四个阶段到达Layer Tree
        - Animate：Tick animations to change widget state
        - Build：Rebuild widgets to account for state changes
        - Layout：Update size and position of render objects
        - Paint：Record display lists for composited layers

3. 三种视图树
    - 组合型：Composer角色，将其他widget进行拼装组合成一个新的widget
        - StatelessWidgt
        - StatefuleWidget/State
    - 代理型：数据传递
        - ProxyWidget
    - 展示型：具有实际展示内容的视图
        - RenderObjectWidget
        - SingleChildRenderObjectWidget
        - LeafRenderObjectWidget
        - MultiChildRenderObjectWidget

4. 创建树的过程
    - 创建Widget树
    - 调用runApp(rootWidget)，将rootWidget传给rootElement，作为rootElement的子节点，生成Element树，再由Element树生成Render树
        - Widget树：存放渲染内容、视图布局信息，widget的属性最好是immutable不变的。
        - Element树：存放上下文，通过Element遍历视图树，Element同时持有Widget和RenderObject
        - RenderObject树：根据Widget的布局属性进行layout，paint Widget传入的内容

5. 为什么widget都是immutable不可变的？
    - flutter界面开发是一种响应式编程，主张simple is fast，flutter设计的初衷希望数据变更时发送通知到对应的可变更节点，由上到下重新create widget树进行刷新，思路简单，不用关心数据变更会影响到哪些节点。

6. widget重新创建，element数和renderObject树是否也重新创建？
    - 不会，widget只是一个配置数据结构，创建非常轻量，官方对widget的创建和销毁做了优化，不用担心整个widget树重新创建所带来的性能问题，但是renderObject涉及到layout、paint等复杂操作，是一个真正渲染的view，整个view树重新创建开销就比较大

7. 树的更新规则
    1. 找到widget对应的element节点，设置element为dirty，触发drawFrame，drawFrame会调用element的performRebuild()进行树重建
    2. widget.build() == null，deactive element.child，删除子树，流程结束
    3. element.child.widget == null，mount新子树，流程结束
    4. element.child.widget == widget.build()，无需重建，否则进入流程5
    5. widget.canUpdate(element.child.widget,newWidget) == true，更新child的slot，element.child.update(newWidget)(如果child还有子节点，则递归上面的流程进行子树更新),流程结束，否则转6
    6. Widget.canUpdate(element.child.widget, newWidget) != true（widget的classtype 或者 key 不相等），deactivew element.child，mount新子树

8. 如何触发树的更新？
    - 全局更新：调用runApp(rootWidget)，flutter启动时候调用后不会再调用
    - 局部子树更新：将该子树做StatefulWidget的一个子widget，并创建对应的State类实例，通过调用state.setState() 触发该子树的刷新

9. StatefuleWidget和StatelessWidget的区别？
    - StatelessWidget：
        - 无中间状态变化的widget，需要更新展示内容就得通过重新new，flutter推荐尽量使用StatelessWidget
    - StatefulWidget：
        - 存在中间状态变化，引入state的类用于存放中间态，通过调用state.setState()进行此节点及以下的整个子树更新

10. State生命周期
    - initState()
        - state create之后被insert到tree的时候调用的
    - didUpdateWidget(newWidget)
        - 祖先节点rebuild widget时调用
    - deactivate()
        - widget被remove的时候调用
        - 一个widget从tree中remove掉，可以在dispose接口被调用前，重新instert到一个新tree中
    - didChangeDependencies()
        - 初始化时，在initState()之后理科调用
        - 当依赖的InheritedWidget rebuild会触发此接口被调用
    - build()
        - initState之后会被调用
        - didUpdateWidget之后被调用
        - setState之后
        - 依赖的State对象改变之后
        - deactivate之后
    - dispose()
        - Widget彻底销毁时调用
    - reassemble()
        - hot reload调用

11. 生命周期注意事项
    - A页面push一个新的B页面，A页面的widget树中所有state会依次调用deactivate、didUpdateWidget、build
    - 当ListView中的item滚动出可现实区域的时候，item会被从树中remove掉，此item子树中所有的state都会被dispose，state记录的数据都会销毁，item滚动回可显示区域时，会重新创建全新的state、element、renderobject
    - 使用hot reload功能的时候，state实例没有重新创建，如果该state中存在一些复杂的资源更新需要重新加载才能生效，那么需要在reassemble()添加处理

#### [深入理解flutter的编译原理与优化](https://mp.weixin.qq.com/s/vlHt8jxbdzBqJZDobpsFVw)
#### [深入理解Flutter引擎线程模式](https://mp.weixin.qq.com/s/hZ5PUvPpMlEYBAJggGnJsw)
#### [Flutter Plugin调用Native APIs](https://mp.weixin.qq.com/s/WORru3f5rfABFMoxQ_2nYw)
#### [Flutter混合工程改造实践](https://mp.weixin.qq.com/s/Q1z6Mal2pZbequxk5I5UYA)
#### [Release Flutter的最后一公里](https://mp.weixin.qq.com/s/xV-FGR9o2ODLFJFq4YwnKg)
#### [Flutter React编程范式实践](https://mp.weixin.qq.com/s/GRHvM0BHe2D9Qwb_nW0New)
#### [闲鱼Fultter混合工程持续集成的最佳实践](https://mp.weixin.qq.com/s/5opwrgVr48e0YDYtEWFXZQ)
#### [Flutter新锐专家之路：工程研发体系篇](https://mp.weixin.qq.com/s/YMnzLGrUdjd1PFlkZdFMqQ)
#### [Flutter新锐专家之路：混合开发篇](https://mp.weixin.qq.com/s/1AMvmuckg9bEODqhULVhPQ)
#### [万万没想到-Flutter这样外接纹理](https://mp.weixin.qq.com/s/KkCsBvnRayvpXdI35J3fnw)
#### [深入理解Flutter Platform Channel](https://mp.weixin.qq.com/s/FT7UFbee1AtxmKt3iJgvyg)
#### [Flutter快速上车之Widget](https://mp.weixin.qq.com/s/kAWPj97w5NfiqAYEpi3zVA)
#### [Flutter之禅 内存优化篇](https://mp.weixin.qq.com/s/mHBz56OWKBB_g9YavVKTbQ)
#### [揭秘Flutter Hot Reload（基础篇）](https://mp.weixin.qq.com/s/Z9QPUJ3dZy2btBOlhSfyQw)
#### [Flutter瘦身大作战](https://mp.weixin.qq.com/s/IIoaY2uw6Bqzc9XWI91YFw)
#### [Flutter中嵌入Native组件的正确姿势是...](https://mp.weixin.qq.com/s/JM_AB0vVH0uOY7v0ToDamw)
#### [关于Flutter初始化，我必须告诉你的是...（干货）](https://mp.weixin.qq.com/s/5JYzHWmczimYy3QMlLUJ4w)
#### [做了2个多月的设计和编码，我梳理了Flutter动态化的方案对比及最佳实现](https://mp.weixin.qq.com/s/N5ih-DY5TuKyn_a0P2mz0Q)
#### [Flutter路由管理代码这么长长长长长，阿里工程师怎么高效解决？（实用）](https://mp.weixin.qq.com/s/YgE9lwEHb31WOWyraHL35w)
#### [Flutter Exception降到万分之几的秘密](https://mp.weixin.qq.com/s/JiJ3XwIq_ADM457M6CBSxA)
#### [如何在Flutter上优雅地序列化一个对象（实用）](https://mp.weixin.qq.com/s/W5kQBe0vlnkG7VwIVAmnRA)
#### [已开源|码上用它开始Flutter混合开发——FlutterBoost](https://mp.weixin.qq.com/s/v-wwruadJntX1n-YuMPC7g)
#### [打通前后端逻辑，客户端Flutter代码一天上线](https://mp.weixin.qq.com/s/hFdBtDQo1TvvxBGHLV3Stw)
#### [燃烧我的卡路里——Flutter瘦内存、瘦包之图片渲染组件](https://mp.weixin.qq.com/s/QwNMm0P2z7RGJ_xzhto1RQ)
#### [Fish Redux中的Dispatch是怎么实现的？](https://mp.weixin.qq.com/s/4hJzGPH8OQ6hkthRFuisBQ)
#### [走近科学，探究阿里闲鱼团队通过数据提升Flutter体验的真相](https://mp.weixin.qq.com/s/26kY9rvRxVDkml2UeBnQfw)
#### [在闲鱼，我们如何用Dart做高效后端开发？](https://mp.weixin.qq.com/s/jAD3hacFMVcOv9GnAfCFOw)
#### [Flutter高内聚组件怎么做？闲鱼闲鱼打造开源高效方案！](https://mp.weixin.qq.com/s/hw24XYmMDNj1iWZ2GAxMiQ)
#### [一个优秀的可定制化Flutter相册组件，看这一篇就够了](https://mp.weixin.qq.com/s/ARKAvDn52irJmyw5tEeD0w)
#### [揭秘！一个高准确率的Flutter埋点框架如何设计](https://mp.weixin.qq.com/s/CMYi-f0-6nwZ4ZyV5K_lKA)
#### [如何低成本实现Flutter富文本，看着一篇就够了！](https://mp.weixin.qq.com/s/CGMwDXQbv_YbwEzblwGqRQ)
#### [编程界的“二向箔”——Dart元编程](https://mp.weixin.qq.com/s/-vEha279U54piV8PGKDzbA)


