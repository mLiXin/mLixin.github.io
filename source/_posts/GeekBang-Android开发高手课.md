---
title: Geek Android开发高手课 学习笔记
date: 2019-01-03 09:37:13
tags:
- Android
- GeekBang
categries:
- Android
---
#### 摘要
一遍不行就两遍，看不懂就死磕，一直看不懂就一直死磕。
<!--more-->

#### Pre
1. 质量平台包括：
    - 稳定性
        - 崩溃
        - ANR
    - 性能
        - 内存
        - 卡顿
        - 启动
        - IO
        - 渲染
        - 电量
        - 网络
        - 安装包
        - 存储

2. 应用体验标准：
    - 性能
        - 冷启动时间<1秒
        - 热启动时间<0.5秒
        - 界面帧率>55
        - 界面不存在过度绘制
        - 不存在内存泄露
        - 前台内存用<500M
        - 后台内存用<400M
        - 后台CPU占用<2%
    - 功耗
        - 后台WakeLock占用<5min
        - 后台网络占用<5min
        - 后台Alarm占用<5min
        - 禁止后台传感器占用

#### 第1、2讲 崩溃优化
总结：native崩溃适当了解，需要C++、指令执行机制等的知识，我选择go die。TODO tag -- 等着我，我一定会回来的。
1. Android崩溃分为Java崩溃和Native崩溃
    - Java崩溃是在Java代码中出现了未捕获异常，导致程序异常退出
    - Native崩溃是因为在Native代码中访问非法地址，也可能是地址对齐出现了问题，或者发生了程序主动abort，这些都会产生相应的signal信号，导致程序异常退出

2. Native崩溃的捕获流程
    - [pre - Android 平台 Native 代码的崩溃捕获机制及实现](https://mp.weixin.qq.com/s/g-WzYF3wWAljok1XjPoo7w?)
    - 编译端，编译C/C++代码的时候，需要将带符号信息的文件保留下来
    - 客户端，捕获到崩溃的时候，将收集到尽可能多的有用信息写入日志文件，然后选择合适的时机上传到服务器
        - 文件句柄泄露，导致创建日志文件失败？
            - 提前申请文件句柄fd预留，防止出现这种情况
        - 因为栈溢出，导致日志生成失败？
            - 防止栈溢出导致进程没有空间创建调用栈执行处理函数，通常会使用常见的singnalstack，在一些特殊情况，可能还需要直接替换当前栈，所以这里也需要在堆中预留部分空间
        - 整个堆的内存都耗尽了，导致日志生成失败？
            - 这个时候无法安全地分派内存，也不敢使用stl或libc的函数，因为它们内部实现会分配堆内存。这个时候如果继续分配内存，会导致出现堆破坏或者二次崩溃的情况。Breakpad做的比较彻底，重新封装了Linux Syscall Support，来避免直接调用libc 
        - 堆破坏或二次崩溃导致日志生成失败？
            - Breakpad会从原进程fork出子进程去手机崩溃线程，此外涉及与Java相关的，一般也会用子进程去操作。这样即使出现二次崩溃，只是这部分信息丢失，我们的父进程后面还可以继续获取其他的信息，在一些特殊情况，我们还可能需要从子进程fork出孙进程  
    - 服务端，读取客户端上传的日志文件，寻找适合的符号文件，生成可读的C/C++调用栈

3. 国内平台，腾讯bugly产品和和社区维护更好，阿里啄木鸟平台技术深度跟捕获能力更好

4. 如何发现应用中的ANR异常？
    - 使用FileObserver监听/data/anr/tracs.txt的变化(微信使用Hardcoder框架)
    - 监控消息队列的运行时间。(无法准确的判断是否真正出现了ANR一场，也无法得到完整的ANR日志。)

5. 应用退出的情形？
    - 主动自杀，Process.killProcess()/exit()等
    - 崩溃，出现了Java或Native崩溃
    - 系统重启，出现异常、断电、用户主动重启等，可以通过比较应用开机运行时间是否比之前记录的值更小
    - 被系统杀死，被low memory killer杀死，从系统的任务管理器中划掉等
    - ANR

6. 崩溃现场应该采集的信息：
    - 崩溃信息
        - 进程名、线程名。崩溃的进程是前台进程还是后台进程，崩溃是不是发生在UI线程
        - 崩溃堆栈和类型。属于Java崩溃还是Native崩溃，还是ANR，不同类型的崩溃，关注点不一样
    - 系统信息
        - Logcat。包括应用、系统的运行日志
        - 机型、系统、厂商、CPU、ABI、Linux版本等
        - 设备状态：是否root，是否是模拟器。一些问题是有Xposed或多开软件造成的，这部分问题要区别对待
    - 内存信息
        - 系统剩余内存：直接读取文件/proc/meminfo。当系统可用内存很小，OOM、大量GC、系统频繁自杀拉起等问题都非常容易出现
        - 应用使用内存：包括Java内存、RSS(Resident Set Size)、PSS(Proportional Set Size)，我们可以得出应用本身内存的占用大小和分布。
        - 虚拟内存：通过/proc/self/status得到，通过/proc/self/maps文件可以得到具体的分布情况。
    - 资源信息
        - 文件句柄fd:可以通过/proc/self/limits获得，一般单个进程语序打开的最大文件句柄个数为1024，但是如果文件句柄超过800个就比较危险，需要将所有的fd以及对应的文件名输出到日志中，进一步排查是否出现了有文件或者线程的泄露。
        - 线程数：可以通过上面的status文件获得，一个线程可能就占2mb的虚拟内存，过多的线程会怼虚拟内存和文件句柄带来压力。如果线程数超过400个就比较危险。
        - JNI：容易出现引用失效、引用爆表等一些崩溃。
    - 应用信息
        - 崩溃场景，发生在哪个Activity或Fragment
        - 关键操作路径，记录关键的用户操作路径，对复现崩溃有比较大的帮助
        - 其他自定义信息，不同的应用关心不一样的重点。

#### 第3、4讲 内存优化
1. 内存优化主要包括两方面的工作：
    - 优化Ram，即降低运行时内存，防止程序发生OOM，降低程序由于内存过大而被LMK机制杀死的概率，另一方面，不合理的内存使用会使GC大大增多，从而导致程序变卡。
    - 优化Rom，即降低程序占ROM的体积。这里主要是为了降低程序占用的空间，防止由于ROM空间不足导致程序无法安装。

2. Leakcanary，通过弱引用的方式侦查Activity或对象的生命周期，若发现内存泄露，自动dump Hprof文件，通过HAHA库得到泄露的最短路径，最后通过notification展示。

3. 通过兜底回收内存，Activity泄露会导致Activit引用到的Bitmap、DrawingCache等无法释放，对内存造成大的压力，兜底是指对于已泄漏的Activity，尝试回收其持有的资源，泄漏的仅仅是一个Activity空壳，从而降低对内存的压力。在Activity的onDestroy里面从view的rootView开始，递归释放所有子View设计的图片、背景、DrawingCache、监听器等资源，让Activity成为一个不占资源的空壳。

4. 降低运行时内存的一些方法
    - 减少bitmap占用的内存
        - 防止bitmap占用资源过大导致OOM：Android4.X系统，可以采用fresco库的方案，将图片资源放于native中
        - 图片按需加载，inJustDecodeBounds+inSampleSize
        - 统一bitmap加载器，降低format
    - 自身内存占用监控
        - 通过Runtime获得内存，然后定期去监控这个值，达到为限制的时候，主动释放各种cache资源，同时显示的去Trim应用的memory，加速内存收集
    - 使用多进程
        - webview、图库等，由于存在内存系统泄露或占用内存过多的问题，可以采用单独的进程。
    - 上报OOM详细信息

5. 内存抖动，是因为在短时间内大量的对象被创建又马上被释放。通过Memory Monitor，可以跟踪整个app的内存变化情况。若短时间发生了多次内存的涨跌，就意味着发生了内存抖动。

6. 通过Heap Viewer，可以查看当前内存快照，便于对比分析哪些对象有可能发生了泄露。Allocation Tracker，追踪内存对象的类型、堆栈、大小等。

7. 内存抖动需要注意的点：
    - 字符串拼接优化：减少字符串使用加号拼接，改用StringBuilder
    - 读文件优化：使用ByteArrayPool，初始设置capacity，减少expand
    - 资源重用：建立缓存池
    - 减少不必要或不合理的对象：在onDraw、getView中减少对象申请，尽量重用。
    - 选用合理的数据格式：使用SparseArray、SparseBooleanArray，LongSparseArray来代替HashMap

8. 内存造成两个问题：异常和卡顿。

9. 2.3之前的像素存储需要的内存是在native上分配的，并且生命周期不太可控，可能需要用户自己回收。  2.3-7.1之间，Bitmap的像素存储在Dalvik的Java堆上，当然，4.4之前的甚至能在匿名共享内存上分配（Fresco采用），而8.0之后的像素内存又重新回到native上去分配，不需要用户主动回收，8.0之后图像资源的管理更加优秀，极大降低了OOM。

10. 当系统物理内存不足的时候，Lmk开始杀进程，从后台、桌面、服务、前台，直到手机重启。(mark，进程优先级应该是：前台进程、可见进程、服务进程、后台进程)

11. Dalvik GC日志分析：
    - GC_CONCURRENT
        - 在堆开始占用内存时可以释放内存的并发垃圾回收
    - GC_FOR_MALLOC
        - 堆已满而系统不得不停止您的应用并回收内存时，您的应用尝试分配内存而引起的垃圾回收。
    - GC_HPROF_DUMP_HEAP
        - 当请求创建HPROF文件来分析堆时出现的垃圾回收
    - GC_EXPLICIT
        - 显式垃圾回收，当您调用gc()时
    - GC_EXTERNAL_ALLOC
        - API10及更低级别，可以忽略

12. [Art GC日志分析](https://developer.android.com/studio/profile/investigate-ram?hl=zh-cn)：不会为未明确请求的垃圾回收记录消息，只有在认为垃圾回收速度较慢时才会打印垃圾回收(垃圾回收暂停时间超过5ms或垃圾回收持续时间超过100ms时)。
    - Concurrent
        - 不会暂停应用线程的并发垃圾回收
    - Alloc
        - 应用在堆已满时尝试分配内存引起的垃圾回收
    - Explicit
        - 由应用明确请求的垃圾回收，如调用gc()
    - NativeAlloc
        - 原生分配导致出现原生内存压力，进而引起的回收
    - CollectorTransition
        - 由堆转换引起的回收(TODO ，没懂啥场景)
    - HomogeneousSpaceCompact
        - 齐性空间压缩是空闲列表空间到空闲列表空间压缩，通常在应用进入到可察觉的暂停进程状态时发生。这样做的主要原因是减少 RAM 使用量并对堆进行碎片整理。(TODO 没懂)
    - DisableMovingGc
    - HeapTrim

13. 内存分析方法：
    1. Java内存分配，常用的工具是Allocation Tracker和MAT
    2. Native内存分配，Malloc调试(帮助调试Native内存的一些使用问题，例如堆破坏、内存泄露、非法地址等)和Malloc钩子(Android P之后，Android的libc支持拦截在程序执行期间发生的所有分配、释放调用，这样我们就可以构建出自定义的内存检测工具。)

14. 内存优化方法：
    - 设备分级
        - 让高端设备使用更多的内存，做到针对性能的好坏使用不同的内存分配和回收策略
        - 使用类似device-year-class的策略对设备分级，对于低端机用户可以关闭复杂的动画，或者是某些功能；使用565格式的图片，使用更小的缓存内存等。开发过程考虑功能要不要对低端机开启、在系统资源吃紧的时候能不能做降级
    - Bitmap优化
        - 统一图片库
        - 统一监控
            - 大图片监控
            - 重复图片监控
            - 图片总内存
    - 内存泄露
        - Java内存泄露

#### 第5、6讲 卡顿优化 (TODO need Linux)
1. Android卡顿排查工具
    - TraceView
        - 对release包支持不好，无法反混淆
        - 性能损耗大
    - Nanoscope
        - 性能损耗小
        - trace结束生成结果文件时间较长
        - 当前只支持Nexus 6P，或采用其提供的x86架构的模拟器
        - 默认值支持主线程采集
    - systrace
    - Simpleperf
    - 如果需要分析Native代码的耗时，可以选择Simpleperf；如果想分析系统调用，可以选择systrace；如果想分析整个程序执行流程的耗时，可以选择TraceView或者插桩版本的systrace。

2. 可视化方法Profiler：
    - Sample Java Methods的功能类似于Traceview的sample类型
    - Trace Java Methods的功能类似于Traceview的instrument类型
    - Trace System Calls的功能类似于systrace
    - SampleNative的功能类似于Simpleperf

3. Call Chart、Flame Chart
    - Call Chart适合分析整个流程的调用
    - Flame Chart直观看出那些代码路径话费的CPU时间较多。

4. 卡顿监控
    - 消息队列监控
        - 通过一个监控线程，每隔一秒向主线程消息队列的头部插入一条空消息，加入一秒后这个消息并没有被主线程消费掉，说明阻塞消息运行的时间在0~1秒之间。
    - 插桩，Inline Hook技术，实现类似Nnoscope先写内存的方案。
    - [Profilo](https://github.com/facebookincubator/profilo) 
        - 看不懂
        - 继承atrace功能
        - 快速获取Java堆栈
    - Android Vitals 

#### 第7、8讲 启动优化 (TODO need 并发编程)
1. 回顾一下Activity的启动流程
2. 启动优化
    - 优化工具
        - systrace+函数插桩
    - 优化方式
        - 闪屏优化
            - 只在Android6.0或者Android7.0以上才启用预览闪屏方案，让手机性能好的用户可以有更好的体验
        - 业务梳理
            - 梳理启动过程正在运行的每一个模块，那些是一定需要的，那些可以砍掉，哪些可以懒加载。
            - 懒加载要防止集中化，否则容易出现首页显示后用户无法操作的情形
        - 业务优化
            - 看看主线程满在哪里，然后通过算法今星期优化。
        - 线程优化
            - 减少CPU调度带来的波动，让应用的启动时间更加稳定。
            - 控制线程数量，太多会相互竞争CPU资源，因此要有统一的线程池，并且根据机器性能来控制数量。
            - 检查线程间的锁，systrace可以看到锁等待的事件。
            - [alpha](https://github.com/alibaba/alpha)
        - GC优化
            - 尽量减少GC的次数，避免造成主线程长时间的卡顿。可以通过systrace单独查看整个启动过程GC的时间。
        - 系统调用优化  
3. 启动进阶方法(TODO 没看懂，留着啃)：
    - I/O优化
    - 数据重排
    - 类的加载
    - 其他黑科技
        - 保活
        - 插件化和热修复

#### 第9、10、11讲 I/O优化 (TODO need 操作系统 文件系统)
1. Android的文件系统是Linux常用的ext4文件系统，未来可能是F2FS系统。
2. 什么是文件损坏？为什么会损坏？
    - 文件内容丢失，结果不是程序写入时期望的结果。SharedPreference跨进程读写就非常容易出现数据丢失的情况。
    - 原因：
        - 应用程序：I/O操作都不是原子操作，跨进程或者多线程写入、使用一个已经关闭的文件描述符fd来操作文件，都有可能导致数据被覆盖或者删除。大部分是这个原因。
        - 文件系统：断点导致的写入丢失，为了提升I/O性能，文件系统把数据写入到Page Cache中，然后等待何时的实际才会真正的写入磁盘。
        - 磁盘：在资料传输过程可能会发生电子遗失等现象导致数据错误。

3. I/O有时候为什么会突然很慢？
    - 内存不足
        - 内存不足的时候，系统会回收Page Cache和Buffer Cache的内存，大部分的写操作会直接落盘，导致性能底下。
     - 写入放大
         - 闪存重复写入需要先进行擦除操作，但是这个擦除操作的基本单元是block块，一个page页的写入操作将会引起整个块数据的迁移。
     - 低端机的CPU和闪存性能比较差，在高负载的情况下容易出现瓶颈。 

#### 第12、13、14讲存储优化
1. 存储的几种方式？
    - SharedPreferences
        - 性能问题：
            - 跨进程不安全
            - 加载缓慢
            - 全量写入
            - 卡顿
        - 替代存储方案：[MMKV](https://github.com/Tencent/MMKV) 
            - 利用文件锁保证进程的安全、使用mmap保证数据不会丢失、选用性能和存储空间更好的Protocol Buffer代替xml、支持增量更新等。
    - ContentProvider
        - 提供了不同进程甚至是不同应用程序之间共享数据的机制。
        - 实现相对笨重，适合传输大的数据。
    - 文件
    - 数据库

2. 序列化的几种方式和优缺点
    - Serializable
    - Parcelable
    - [Serial](https://github.com/twitter/Serial)
### 第15、16、17讲 网络优化(TODO need 网络)

#### 第18、19讲 耗电优化
1. 电池的关键指标
    - 电池容量
    - 充电时间
    - 寿命
    - 安全性

2. 应用程序不会直接消耗电池，而是通过硬件模块消耗相应的电能
3. Android耗电的演进历程
    - Pre Android5.0 野蛮生长
    - 逐步收紧 Android5.0~Android8.0
        - Volta项目
        - dumpsys batteryst
    - 最严限制 Android9.0
        - 应用待机分组
            - 分组决定后台被限制的程度：不常用的引用在后台将被限制地更加严格
        - 应用后台限制
            - 停止后台运行：提示用户后台耗电严重的应用，用户可选择停止它们的后台运行
        - 省电模式
            - 所有应用程序进入待机模式：更加严格的后台限制，而且无视应用的Target API

4. 耗电优化方式
    - 优化应用的后台耗电
        - 不在后台长时间获取WakeLock、WiFi和蓝牙扫描等
    - 符合系统的规则，让系统认为你的耗电是正常的。
        - 符合Vitals的规则：
            - Alarm Manager wakeup唤醒过多
            - 频繁使用局部唤醒锁
            - 后台网络使用量过高
            - 后台WiFi scans过多

#### 第20、21讲 UI优化
1. UI优化的两个方面？
    - 效率提升
    - 性能提升
2. UI适配的方式？
    - 通过dp加上自适应布局可以基本解决屏幕碎片化的问题
    - 限制符适配方案：主要有宽高限定符与smallestWidth限定符适配方案
    - 今日头条适配方案：通过反射修正系统的density值
3. Android中都有哪些图形组件？的各个图形组件的作用？
    - 画笔：Skia或者OpenGL
        - 我们可以用Skia画笔绘制2D图形，也可以用O喷GL来绘制2D、3D图形，前者用CPU绘制，后台使用GPU绘制
    - 画纸：Surface
        - 所有元素都在Surface这张画纸上进行绘制和渲染。Window是View的容器，每个窗口都关联一个Surface。而WindowManager则负责管理这些窗口，并且把它们的数据传递给SurfaceFlinger
    - 画板：Graphic Buffer
        - Graphic Buffer缓冲用于应用程序图形的绘制，在Android4.1之前使用的是双缓冲机制；在Android4.1之后，使用的是三缓冲机制
    - 显示：SurfaceFlinger
        - 它将WindowManager提供的所有Surface，通过硬件合成器Hardware Composer合成并输出到显示屏。

4. UI优化的进阶手段？
    - Litho：异步布局
        - 异步布局：把measure和layout都放到了后台线程，留下了必须要在住线程完成的draw，降低UI线程的负载
        - 界面扁平化：检测不必要的层级、减少ViewGroups
        - 优化RecyclerView中UI组件的缓存和回收方法
            - RecyclerView按照viewType来进行缓存和回收，Litho按照text、image和video独立回收，提高缓存命中率、降低内存使用率、提高滚动帧率
    - Flutter：自己的布局+渲染引擎 

5. UI优化的所有手段？
    - 在系统的框架下优化
        - 布局优化、使用代码创建、View缓存
    - 利用系统新的特性
        - 使用硬件加速、RenderThread、RenderScript
    - 突破系统的限制
        - Litho、Flutter等
#### 第22、23讲 包体积优化
1. 安装包包括哪些内容？
    - Dex
    - Resource
    - Assets
    - Library
    - 签名信息
2. 优化方式
    - 代码
        - ProGuard：检查最终合并的ProGuard配置文件，是否存在过度keep的现象
        - 去掉Debug信息或者去掉行号
        - Dex分包
        - Dex压缩
    - Native Library
        - Library压缩
        - Library合并与裁剪
    - 包体积监控 