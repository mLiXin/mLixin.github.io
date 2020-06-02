---
title: Flutter源码浅析 - BuildOwner
date: 2020-04-28 17:13:13
tags:
- Flutter
categories:
- Flutter
- 源码学习
---
#### 摘要
version: Channel dev, v1.18.0-8.0.pre

BuildOwner用来管理Element
<!--more-->
#### Constructor

```Dart
BuildOwner({ this.onBuildScheduled });
```

#### Properties

```Dart
// 当第一个可以构建的element被标记为dirty的时候每次build的时候调用
VoidCallback onBuildScheduled;

// 不再活动的Element集合，内部通过hashSet来实现
final _InactiveElements _inactiveElements = _InactiveElements();

// 记录dirtyElement的list
final List<Element> _dirtyElements = <Element>[];

bool _scheduledFlushDirtyElements = false;

// 由于在build期间会有更多的element变为dirty，是否需要再次对_dirtyElements进行排序
bool _dirtyElementsNeedsResorting;

// 负责焦点树的对象
FocusManager focusManager = FocusManager();
```

#### Method

```Dart
// 当WidgetsBinding.drawFrame调用buildScope方法的时候，将元素添加到dirtyElement的列表中，从而实现重建
void scheduleBuildFor(Element element){...;}

// 建立一个禁止调用[State.setState]的范围，并调用给定的callback
void lockState(void callback()){...;}

// 建立更新WidgetTree的范围，并调用给定的callback。然后调用[scheduleBuildFor],按照深度顺序，build所有标记为dirty的element
void buildScope(Element context, [ VoidCallback callback ]){...;}

// 卸载不再活动的element来完成build过程
void finalizeTree(){...;}

// 重建以给定的Element为根的整个子树，一般用于hot Reload的时候。
// 注意，除了开发调试下，这个方法不要调用。
void reassemble(Element root){...;}
```

#### Method Imple
##### `void scheduleBuildFor(Element element){...;}`

```Dart
  void scheduleBuildFor(Element element) {
    if (element._inDirtyList) {
      _dirtyElementsNeedsResorting = true;
      return;
    }
    if (!_scheduledFlushDirtyElements && onBuildScheduled != null) {
      _scheduledFlushDirtyElements = true;
      // WidgetsBinding的initInstances方法中创建BuildOwner并赋值onBuildScheduled = _handleBuildScheduled()，这个handle方法内部调用SchedulerBinding的ensureVisualUpdate();
      // ensureVisualUpdate()方法用于对象还没有生成Frame的时候通过scheduleFrame()方法来计划生成新的Frame
      onBuildScheduled();
    }
    // 将该element添加进dirtyElement列表中
    _dirtyElements.add(element);
    // 将该element的_inDirtyList属性置为true
    element._inDirtyList = true;
  }
```

##### `void lockState(void callback()){...;}`

```Dart
  void lockState(void callback()) {
      callback();
  }
```

##### `void buildScope(Element context, [ VoidCallback callback ]){...;}`

```Dart
void buildScope(Element context, [ VoidCallback callback ]) {
    if (callback == null && _dirtyElements.isEmpty)
      return;

    _scheduledFlushDirtyElements = true;
    // 执行callback回调
    if (callback != null) {
        _dirtyElementsNeedsResorting = false;
        callback();
    }
    // 对dirtyElement列表进行排序
    _dirtyElements.sort(Element._sort);
    _dirtyElementsNeedsResorting = false;
    int dirtyCount = _dirtyElements.length;
    int index = 0;
    while (index < dirtyCount) {
      // 调用每个dirtyElement的rebuild()方法进行重建
      _dirtyElements[index].rebuild();
      index += 1;

      if (dirtyCount < _dirtyElements.length || _dirtyElementsNeedsResorting) {
        // 对dirtyElement列表重新进行排序，并获取最新的dirtyCount
        _dirtyElements.sort(Element._sort);
        _dirtyElementsNeedsResorting = false;
        dirtyCount = _dirtyElements.length;
        // 
        while (index > 0 && _dirtyElements[index - 1].dirty) {
          index -= 1;
        }
      }
    }
    
    // 重建完后，将dirtyElement列表等重置
    for (final Element element in _dirtyElements) {
      element._inDirtyList = false;
    }
    _dirtyElements.clear();
    _scheduledFlushDirtyElements = false;
    _dirtyElementsNeedsResorting = null;
}
```

##### `void finalizeTree(){...;}`

```Dart
void finalizeTree() {
  lockState(() {
    _inactiveElements._unmountAll(); 
  }); 
}
```

##### `void reassemble(Element root){...;}`

```Dart
void reassemble(Element root) {
    root.reassemble();
}
```


