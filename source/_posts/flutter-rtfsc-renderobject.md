---
title: Flutter源码浅析 - RenderObject
date: 2020-04-29 17:24:41
tags:
- Flutter
- TODO
categories:
- Flutter
- 源码学习
---
#### 摘要
version: Channel dev, v1.18.0-8.0.pre

源码解读RenderObject类，忽略try/catch、assert、Semantics等相关内容
<!--more-->

#### Constructor
#### Properties

```Dart
// 父类RenderObject使用
ParentData parentData;

bool _needsLayout = true;
RenderObject _relayoutBoundary;
bool _doingThisLayoutWithCallback = false;

// 父类给定的布局约束
Constraints _constraints;

// 该renderObject是否和其parent分开绘制
bool get isRepaintBoundary => false;

// 该renderObject是否总是需要合成
bool get alwaysNeedsCompositing => false;

// set to true when a child is added
bool _needsCompositingBitsUpdate = false; 

// 是否有compositingLayout
bool _needsCompositing;
```
#### Method
- [`void reassemble(){...;}`](#reassemble)
  - 刷新整颗RenderTree，主要用在调试时候的HotReload时候调用

- [`void setupParentData(covariant RenderObject child){...;}`](#setupParentData)
  - 为给定的child初始化parentData

- [`void adoptChild(RenderObject child){...;}`](#adoptChild)
  - 当其子类将一个renderObject作为其child的时候调用


- [`void dropChild(RenderObject child){...;}`](#dropChild)
  - 当子类决定该child不再是其child的时候调用

- [`void visitChildren(RenderObjectVisitor visitor) { }`](#visitChildren)
  - 调用每个child的visitor

- [`void attach(PipelineOwner owner){...;}`](#attach)
  - 将当前RenderObject和给定的pipelineOwner绑定
  - 根据当前renderOBject的各种属性参数判断是否需要layout、compositingBitsUpdate、paint等操作

- [`void markNeedsLayout() {...;}`](#markNeedsLayout)
  - 标记该renderObject的布局信息为dirty，并在下一帧绘制的时候刷新该renderObject

- [`void markParentNeedsLayout() {...;}`](#markParentNeedsLayout)
  - 如果子类在layout过程中影响到了父类，则父类renderObject同样需要重新layout

- [`void _cleanRelayoutBoundary() {...;}`](#cleanRelayoutBoundary)
  - 清除当前object及其子类的relayoutBoundary

- [`void scheduleInitialLayout() {...;}`](#scheduleInitialLayout)
  - 通过规划第一个layout来引导rendering pipeline

- [`void _layoutWithoutResize() {...;}`](#layoutWithoutResize)
  - 重新计算并绘制renderObejct

- [`void layout(Constraints constraints, { bool parentUsesSize = false }){...;}`](#layout)
  - 计算该renderObject的layout
  - 这个方法主要用于parents请求child来更新child的layout信息

- [`void invokeLayoutCallback<T extends Constraints>(LayoutCallback<T> callback){...;}`](#invokeLayoutCallback)
  - 在进行layout的时候执行给定的callback回调

- [`void markNeedsCompositingBitsUpdate() {...;}`](#markNeedsCompositingBitsUpdate)
  - 将该renderObject的compositingState标记为dirty

- [`void _updateCompositingBits() {...;}`](#updateCompositingBits)
  - TODO 这个compositingBits还没看明白是干啥的，等着我。

- [`void markNeedsPaint() {...;}`](#markNeedsPaint)
  - 标记该renderObject已经改变其外观

- [`void _skippedPaintingOnLayer() {...;}`](#skippedPaintingOnLayer)
  - 当flushPaint()方法试图绘制但是layer已经detached的时候调用

- [`void scheduleInitialPaint(ContainerLayer rootLayer) {...;}`](#scheduleInitialPaint)
  - 通过第一次paint来引导renderPipeline

- [`void replaceRootLayer(OffsetLayer rootLayer) {...;}`](#replaceRootLayer)
  - 替换layer。只对renderObject的root有效
  - 可能在设备的像素比改变的时候调用

- [`void handleEvent(PointerEvent event, covariant HitTestEntry entry) { }`](#handleEvent)
  - 重写该方法来处理renderObject的pointer event

#### Method Imple
##### <a name = "reassemble" />`void reassemble(){...;}`

```Dart
// 刷新整颗RenderTree，主要用在调试时候的HotReload时候调用
void reassemble() {
    markNeedsLayout();
    markNeedsCompositingBitsUpdate();
    markNeedsPaint();
    markNeedsSemanticsUpdate();
    visitChildren((RenderObject child) {
      child.reassemble();
    });
  }
```

##### <a name="setupParentData" />`void setupParentData(covariant RenderObject child){...;}`

```Dart
// 为给定的child初始化parentData
void setupParentData(covariant RenderObject child) {
    if (child.parentData is! ParentData)
      child.parentData = ParentData();
}
```

##### <a name="adoptChild" />`void adoptChild(RenderObject child){...;}`

```Dart
// 当其子类将一个renderObject作为其child的时候调用
void adoptChild(RenderObject child) {
    // 初始化parentData
    setupParentData(child);
    // TODO
    markNeedsLayout();
    // TODO
    markNeedsCompositingBitsUpdate();
    // TODO 
    markNeedsSemanticsUpdate();
    // 调用父类的adoptChild方法
    super.adoptChild(child);
}
```

##### <a name="dropChild" />`void dropChild(RenderObject child){...;}`

```Dart
// 当子类决定该child不再是其child的时候调用
void dropChild(RenderObject child) {
    // 
    child._cleanRelayoutBoundary();
    //
    child.parentData.detach();
    // 将其parentData置空
    child.parentData = null;
    // 调用其父类？？？ TODO
    super.dropChild(child);
    // 
    markNeedsLayout();
    // 
    markNeedsCompositingBitsUpdate();
    // 
    markNeedsSemanticsUpdate();
}
```

##### <a name="visitChildren" />`void visitChildren(RenderObjectVisitor visitor) { }`

```Dart
// 调用每个child的visitor
void visitChildren(RenderObjectVisitor visitor) { }
```

##### <a name="attach" />`void attach(PipelineOwner owner){...;}`

```Dart
// 将当前RenderObject和给定的pipelineOwner绑定
// 根据当前renderOBject的各种属性参数判断是否需要layout、compositingBitsUpdate、paint等操作
void attach(PipelineOwner owner) {
    super.attach(owner);
    if (_needsLayout && _relayoutBoundary != null) {
      _needsLayout = false;
      markNeedsLayout();
    }
    if (_needsCompositingBitsUpdate) {
      _needsCompositingBitsUpdate = false;
      markNeedsCompositingBitsUpdate();
    }
    if (_needsPaint && _layer != null) {
      _needsPaint = false;
      markNeedsPaint();
    }
    if (_needsSemanticsUpdate && _semanticsConfiguration.isSemanticBoundary) {
      _needsSemanticsUpdate = false;
      markNeedsSemanticsUpdate();
    }
}
```

##### <a name="markNeedsLayout"/>`void markNeedsLayout() {...;}`

```Dart
// 标记该renderObject的布局信息为dirty，并在下一帧绘制的时候刷新该renderObject
void markNeedsLayout() {
    if (_needsLayout) {
      return;
    }
    // 判断自己是不是relayoutBoundary
    if (_relayoutBoundary != this) {
      // 不是的话，需要标记父类需要重新layout
      markParentNeedsLayout();
    } else {
      // 是的话，将自身标记_needsLayout，并将该renderObject添加到pipelineOwner的_nodesNeedingLayout列表中，并调用刷新
      _needsLayout = true;
      if (owner != null) {
        owner._nodesNeedingLayout.add(this);
        owner.requestVisualUpdate();
      }
    }
}
```

##### <a name="markParentNeedsLayout"/>`void markParentNeedsLayout() {...;}`

```Dart
// 如果子类在layout过程中影响到了父类，则父类renderObject同样需要重新layout
void markParentNeedsLayout() {
    _needsLayout = true;
    final RenderObject parent = this.parent as RenderObject;
    if (!_doingThisLayoutWithCallback) {
      parent.markNeedsLayout();
    } 
}
```

##### <a name="cleanRelayoutBoundary"/>`void _cleanRelayoutBoundary() {...;}`

```Dart
// 清除当前object及其子类的relayoutBoundary
void _cleanRelayoutBoundary() {
    if (_relayoutBoundary != this) {
      _relayoutBoundary = null;
      _needsLayout = true;
      visitChildren(_cleanChildRelayoutBoundary);
    }
}
```

##### <a name="scheduleInitialLayout"/>`void scheduleInitialLayout() {...;}`

```Dart
// 通过规划第一个layout来引导rendering pipeline
void scheduleInitialLayout() {
    // 将当前renderObject添加到pipelineOwner的_nodesNeedingLayout列表中
    owner._nodesNeedingLayout.add(this);
}
```

##### <a name="layoutWithoutResize"/>`void _layoutWithoutResize() {...;}`

```Dart
// 重新计算并绘制renderObejct
void _layoutWithoutResize() {

    // 完成renderObject的layout工作，抽象方法，子类实现
    performLayout();
    // 辅助功能相关的，先忽略
    markNeedsSemanticsUpdate();
    // 将当前renderObject置为不再需要重新layout
    _needsLayout = false;
    // 标记需要重新绘制？ TODO
    markNeedsPaint();
}
```

##### <a name="layout"/>`void layout(Constraints constraints, { bool parentUsesSize = false }){...;}`

```Dart
// 计算该renderObject的layout
// 这个方法主要用于parents请求child来更新child的layout信息
void layout(Constraints constraints, { bool parentUsesSize = false }) {

    RenderObject relayoutBoundary;
    if (!parentUsesSize || sizedByParent || constraints.isTight || parent is! RenderObject) {
      relayoutBoundary = this;
    } else {
      relayoutBoundary = (parent as RenderObject)._relayoutBoundary;
    }

    // 如果当前rendeObject不需要重新layout，并且constraints和relayoutBoundary都一直，则不需要重新计算
    if (!_needsLayout && constraints == _constraints && relayoutBoundary == _relayoutBoundary) {
      return;
    }

    _constraints = constraints;

    // 清除所有child的relayoutBoundary数据
    if (_relayoutBoundary != null && relayoutBoundary != _relayoutBoundary) {
      visitChildren(_cleanChildRelayoutBoundary);
    }

    _relayoutBoundary = relayoutBoundary;

    // constraints是不是唯一决定该size的参数
    if (sizedByParent) {
        // 子类实现的抽象方法，仅仅根据constraints类更新renderObject的size
        performResize();
    }

    // 调用子类实现的performLayout计算
    performLayout();
    markNeedsSemanticsUpdate();
    _needsLayout = false;
    // 标记该renderObject需要重新绘制？
    markNeedsPaint();
  }
```

##### <a name="invokeLayoutCallback"/>`void invokeLayoutCallback<T extends Constraints>(LayoutCallback<T> callback){...;}`

```Dart
// 在进行layout的时候执行给定的callback回调
void invokeLayoutCallback<T extends Constraints>(LayoutCallback<T> callback) {
    _doingThisLayoutWithCallback = true;
    owner._enableMutationsToDirtySubtrees(() { callback(constraints as T); });
    _doingThisLayoutWithCallback = false;
}
```

##### <a name="markNeedsCompositingBitsUpdate"/>`void markNeedsCompositingBitsUpdate() {...;}`

```Dart
// 将该renderObject的compositingState标记为dirty
void markNeedsCompositingBitsUpdate() {
    // 已经标记，则直接return
    if (_needsCompositingBitsUpdate)
      return;
    _needsCompositingBitsUpdate = true;
    // 
    if (parent is RenderObject) {
      final RenderObject parent = this.parent as RenderObject;
      if (parent._needsCompositingBitsUpdate)
        return;
      // 递归调用，将parent的compositingState也标记为dirty  
      if (!isRepaintBoundary && !parent.isRepaintBoundary) {
        parent.markNeedsCompositingBitsUpdate();
        return;
      }
    }
    // 添加到pipelineOwner的对应list中
    if (owner != null)
      owner._nodesNeedingCompositingBitsUpdate.add(this);
}
```

##### <a name="updateCompositingBits"/>`void _updateCompositingBits() {...;}`

```Dart
// TODO 这个compositingBits还没看明白是干啥的，等着我。
void _updateCompositingBits() {
    if (!_needsCompositingBitsUpdate)
      return;
    final bool oldNeedsCompositing = _needsCompositing;
    _needsCompositing = false;
    // 递归调用child的该方法
    visitChildren((RenderObject child) {
      child._updateCompositingBits();
      if (child.needsCompositing)
        _needsCompositing = true;
    });

    if (isRepaintBoundary || alwaysNeedsCompositing)
      _needsCompositing = true;
    if (oldNeedsCompositing != _needsCompositing)
      markNeedsPaint();
    _needsCompositingBitsUpdate = false;
}
```

##### <a name="markNeedsPaint"/>`void markNeedsPaint() {...;}`

```Dart
// 标记该renderObject已经改变其外观
void markNeedsPaint() {
    if (_needsPaint)
      return;
    _needsPaint = true;
    if (isRepaintBoundary) {
      // 该renderObject和其父类分开repaint
      if (owner != null) {
        owner._nodesNeedingPaint.add(this);
        owner.requestVisualUpdate();
      }
    } else if (parent is RenderObject) {
      // 该object的parent也是renderObject，调用parent的方法进行repaint
      final RenderObject parent = this.parent as RenderObject;
      parent.markNeedsPaint();
    } else {
      // 直接调用pipelineOwner进行repaint
      if (owner != null)
        owner.requestVisualUpdate();
    }
}
```

##### <a name="skippedPaintingOnLayer"/>`void _skippedPaintingOnLayer() {...;}`

```Dart
// 当flushPaint()方法试图绘制但是layer已经detached的时候调用
void _skippedPaintingOnLayer() {
    AbstractNode ancestor = parent;
    while (ancestor is RenderObject) {
      final RenderObject node = ancestor as RenderObject;
      if (node.isRepaintBoundary) {
        if (node._layer == null)
          break; // looks like the subtree here has never been painted. let it handle itself.
        if (node._layer.attached)
          break; // it's the one that detached us, so it's the one that will decide to repaint us.
        node._needsPaint = true;
      }
      ancestor = node.parent;
    }
}
```

##### <a name="scheduleInitialPaint"/>`void scheduleInitialPaint(ContainerLayer rootLayer) {...;}`

```Dart
// 通过第一次paint来引导renderPipeline
void scheduleInitialPaint(ContainerLayer rootLayer) {
    _layer = rootLayer;
    owner._nodesNeedingPaint.add(this);
}
```

##### <a name="replaceRootLayer"/>`void replaceRootLayer(OffsetLayer rootLayer) {...;}`

```Dart
// 替换layer。只对renderObject的root有效
// 可能在设备的像素比改变的时候调用
void replaceRootLayer(OffsetLayer rootLayer) {
    // detach当前layout
    _layer.detach();
    // 将layer指定为给定的layer
    _layer = rootLayer;
    // 标记需要重新绘制
    markNeedsPaint();
}
```

##### <a name="handleEvent"/>`void handleEvent(PointerEvent event, covariant HitTestEntry entry) { }`

```Dart
// 重写该方法来处理renderObject的pointer event
void handleEvent(PointerEvent event, covariant HitTestEntry entry) { }
```

#### Question
1. visitChildren这个用法有点意思，TODO，看完这个类，去熟悉熟悉。



