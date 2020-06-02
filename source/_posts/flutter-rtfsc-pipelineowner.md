---
title: Flutter源码浅析 - PipelineOwner
date: 2020-04-28 18:13:08
tags:
- Flutter
- TODO
categories:
- Flutter
- 源码学习
---
#### 摘要
version: Channel dev, v1.18.0-8.0.pre

源码解读PipelineOwner类，忽略try/catch、assert、Semantics相关内容
<!--more-->

#### Constructor

```Dart
  PipelineOwner({
    this.onNeedVisualUpdate,
    this.onSemanticsOwnerCreated,
    this.onSemanticsOwnerDisposed,
  });
```

#### Properties

```Dart
// 当与当前PipelineOwner管理的渲染对象期望update显示的时候调用
final VoidCallback onNeedVisualUpdate;

// 根节点
AbstractNode get rootNode => _rootNode;
AbstractNode _rootNode;

// 需要进行layout的RenderObject列表
List<RenderObject> _nodesNeedingLayout = <RenderObject>[];

final List<RenderObject> _nodesNeedingCompositingBitsUpdate = <RenderObject>[];
// 需要进行paint的RenderObject列表
List<RenderObject> _nodesNeedingPaint = <RenderObject>[];
```
#### Method

```Dart
// 调用onNeedVisualUpdate回调
void requestVisualUpdate(){...;}

// 设置根节点
set rootNode(AbstractNode value){...;}

// 更新所有标记为dirty RenderObject的layout信息
void flushLayout(){...;}

// 调用给定的callback
void _enableMutationsToDirtySubtrees(VoidCallback callback){...;}

// 更新[RenderObject.needsCompositing] bits. TODO 没懂具体是干啥，需要看看RenderObject类，等着我。
void flushCompositingBits(){...;}

// 更新所有RenderObject的显示
void flushPaint(){...;}
```
#### Method Imple
##### `void requestVisualUpdate(){...;}`

```Dart
void requestVisualUpdate() {
   if (onNeedVisualUpdate != null)
      // 调用构造函数中给定的onNeedVisualUpdate回调  
      onNeedVisualUpdate();
}
```

##### `set rootNode(AbstractNode value){...;}`

```Dart
set rootNode(AbstractNode value) {
    if (_rootNode == value)
      return;
    _rootNode?.detach();
    _rootNode = value;
    _rootNode?.attach(this);
  }
```

##### `void flushLayout(){...;}`

```Dart
void flushLayout() {
    while (_nodesNeedingLayout.isNotEmpty) {
      // 将需要进行layout的RenderObject列表赋值给dirtyNodes
      final List<RenderObject> dirtyNodes = _nodesNeedingLayout;
      // 清空nodesNeedingLayout列表置空
      _nodesNeedingLayout = <RenderObject>[];
      // 将dirtyNodes列表按照RenderObject深度从小到大排序，并依次调用RenderObject的_layoutWithoutResize()方法
      for (final RenderObject node in dirtyNodes..sort((RenderObject a, RenderObject b) => a.depth - b.depth)) {
        if (node._needsLayout && node.owner == this)
          node._layoutWithoutResize();
      }
    }
}
```

##### `void _enableMutationsToDirtySubtrees(VoidCallback callback){...;}`
```Dart
void _enableMutationsToDirtySubtrees(VoidCallback callback) {
    callback();
}
```

##### `void flushCompositingBits(){...;}`

```Dart
void flushCompositingBits() {
    // 按照深度从小到大的顺序
    _nodesNeedingCompositingBitsUpdate.sort((RenderObject a, RenderObject b) => a.depth - b.depth);
    // 依次调用RenderObject的_updateCompositingBits()
    for (final RenderObject node in _nodesNeedingCompositingBitsUpdate) {
      if (node._needsCompositingBitsUpdate && node.owner == this)
        node._updateCompositingBits();
    }
    // 清空列表
    _nodesNeedingCompositingBitsUpdate.clear();
}
```

##### `void flushPaint(){...;}`

```Dart
void flushPaint() {
  final List<RenderObject> dirtyNodes = _nodesNeedingPaint;
  _nodesNeedingPaint = <RenderObject>[];

  // 从大到小顺序排列
  for (final RenderObject node in dirtyNodes..sort((RenderObject a, RenderObject b) => b.depth - a.depth)) {
    if (node._needsPaint && node.owner == this) {
      if (node._layer.attached) {
        PaintingContext.repaintCompositedChild(node);
      } else {
        node._skippedPaintingOnLayer();
      }
    }
  }

}
```

#### Question TODO
1. flushLayout中为什么要将RenderObject的列表进行从小到大排序？优先小任务？
2. flushCompositingBits方法具体做什么工作？
3. flushPain方法中具体做哪些工作？