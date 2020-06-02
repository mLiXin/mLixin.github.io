---
title: 源码角度浅析Flutter App启动过程（一） Android平台做了哪些工作？
date: 2020-04-26 17:51:32
tags:
- Flutter
categories:
- Flutter
- 源码学习
---

#### 摘要
version: Channel dev, v1.18.0-8.0.pre

从源码角度来分析Flutter应用启动过程，Android平台都做了哪些工作？熟悉Android开发的同学都知道，Android启动后会调用Application和Activity的onCreate方法，本文即从这两个方法入口去分析。
<!--more-->

#### FlutterApplication#onCreate()
```Dart
// [FlutterAolication.java#onCreate]
public void onCreate() {
    super.onCreate();
    FlutterMain.startInitialization(this);
}

// [FlutterMain.java]
public static void startInitialization(@NonNull Context applicationContext) {
    FlutterLoader.getInstance().startInitialization(applicationContext);
}

// [FlutterLoader.java]
public void startInitialization(@NonNull Context applicationContext) {
    startInitialization(applicationContext, new Settings());
}

public void startInitialization(@NonNull Context applicationContext, @NonNull Settings settings) {
    // 保证只会执行一次
    if (this.settings != null) {
        return;
    }
    // 保证在主线程中执行
    if (Looper.myLooper() != Looper.getMainLooper()) {
        throw new IllegalStateException("startInitialization must be called on the main thread");
    }

    this.settings = settings;

    // 记录开始执行时间
    long initStartTimestampMillis = SystemClock.uptimeMillis();
    // 从manifest的文件中获取一些值用于Flutter初始化配置
    initConfig(applicationContext);
    // 首先清理因为不正常关闭而导致的无法触及的资源(TODO，剩下的代码都是基于BuildConfig.DEBUG或BuildConfig.JIT_RELEASE的)
    initResources(applicationContext);
    // 加载libflutter.so
    System.loadLibrary("flutter");
    // 初始化VsyncWaiter，通过FlutterJNI设置Vsync信号回调和当前display的刷新频率(fps)
    VsyncWaiter.getInstance((WindowManager) applicationContext.getSystemService(Context.WINDOW_SERVICE)).init();
    // 计算获取init执行时长
    long initTimeMillis = SystemClock.uptimeMillis() - initStartTimestampMillis;
    // 通过FlutterJNI记录init执行时长。
    FlutterJNI.nativeRecordStartTimestamp(initTimeMillis);
}
```

#### FlutterActivity
##### onCreate
```Java
  // [FlutterActivity.java]
@Override
protected void onCreate(@Nullable Bundle savedInstanceState) {
    switchLaunchThemeForNormalTheme();

    super.onCreate(savedInstanceState);
    
    // 注明生命周期为onCreate lifecycle.handleLifecycleEvent(Lifecycle.Event.ON_CREATE);
    lifecycle.handleLifecycleEvent(Lifecycle.Event.ON_CREATE);

    // 创建代理类实例，将Activity的所有操作都放到代理类去处理，参数this，即当前FlutterActivity实现的Host接口
    delegate = new FlutterActivityAndFragmentDelegate(this);
    delegate.onAttach(this);
    delegate.onActivityCreated(savedInstanceState);

    // 如果backgroundMode为transparent，将背景设置为透明，这个mode通过intent获取。
    configureWindowForTransparency();
    // 生成FlutterView和FlutterSplashView，并返回FlutterSplashView实例，将其设置为mainActivity的view
    setContentView(createFlutterView());
    // 设置状态栏
    configureStatusBarForFullscreenFlutterExperience();
}
  
  // [FlutterActivityAndFragmentDelegate]
void onAttach(@NonNull Context context) {
    // 确保当前代理类没有被release
    ensureAlive();
    // 如果flutterEngine为空，初始化FlutterEngine，这里代码细看，可以发现1.如果存在cachedEngineId，则从FlutterEngineCache中获取；2.如果实现了host的provideFutureEngine，则为该Engine；3.根据host提供的参数new一个flutterEngine实例。前两种方式isFlutterEngineFromHost为true，最后这种为false
    if (flutterEngine == null) {
      setupFlutterEngine();
    }
    platformPlugin = host.providePlatformPlugin(host.getActivity(), flutterEngine);

    if (host.shouldAttachEngineToActivity()) {
      // 将引擎和这个Activity绑定？TODO 这块先留着
      flutterEngine
          .getActivityControlSurface()
          .attachToActivity(host.getActivity(), host.getLifecycle());
    }
    // 配置Flutter引擎，这里主要是注册pubspec.yaml注册的所有plugins
    host.configureFlutterEngine(flutterEngine);
}  
  
```

##### `onStart()`
```Java
// [FlutterActivityAndFragmentDelegate.java]
void onStart() {
    ensureAlive();
    doInitialFlutterViewRun();
}
  
private void doInitialFlutterViewRun() {
    // 如果是从缓存中获取的FlutterEngine实例，则不用走走下去。
    if (host.getCachedEngineId() != null) {
      return;
    }
    // 确保现在没有正在执行Dart代码
    if (flutterEngine.getDartExecutor().isExecutingDart()) {
      return;
    }
    // 设置initialRoute
    if (host.getInitialRoute() != null) {
      flutterEngine.getNavigationChannel().setInitialRoute(host.getInitialRoute());
    }

    // 执行Dart代码，这里一系列的操作最后应该会执行main.dart中的main()方法
    DartExecutor.DartEntrypoint entrypoint =
        new DartExecutor.DartEntrypoint(
            host.getAppBundlePath(), host.getDartEntrypointFunctionName());
    flutterEngine.getDartExecutor().executeDartEntrypoint(entrypoint);
}
  
```

- Tips：
    - createFlutterView()方法：
        - 先根据RenderMode是不是surface决定创建FlutterView是FlutterSurfaceView类型还是FlutterTextureView类型
        - 添加首帧渲染listener
        - 创建FlutterSplashView用于首帧渲染出来之前展示的页面
        - 将FlutterView绑定到FlutterEngine中去。具体细节就不去看了，深挖都是坑。
    - setupFlutterEngine()方法：
        - 三种创建FlutterEngine实例的方法
            - 通过cachedId获取
            - 通过host的`provideFlutterEngine`获取
            - 根据配置new
        - 这里第二种方法配置可能是为了混合开发的时候可以指定FlutterEngine？TODO 

#### 总结
##### FlutterApplication
1. 从manifest的文件中获取一些值用于Flutter初始化配置
2. 提取Assets中的资源
3. 加载libflutter.so
4. 设置Vsync回调和刷新的fps

##### FlutterActivity
1. 创建代理类实例
2. 创建FlutterEngine实例并进行相关的初始化操作，如绑定所有的pubspec.yaml中配置的第三方plugins等。
2. 初始化app的背景、状态栏等
3. 创建FlutterView
4. 创建FlutterSplashView用于首帧渲染前显示
5. 配置initRoute，并开始执行Dart代码。

#### 参考
- [深入理解Flutter引擎启动](http://gityuan.com/2019/06/22/flutter_booting/)