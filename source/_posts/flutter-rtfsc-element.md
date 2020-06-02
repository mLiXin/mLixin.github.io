---
title: Flutter源码浅析 - Element
date: 2020-04-29 10:26:10
tags:
- Flutter
- TODO
categories:
- Flutter
- 源码学习
---
#### 摘要
version: Channel dev, v1.18.0-8.0.pre

源码解读Element类，忽略try/catch、assert、Semantics相关内容
<!--more-->

#### Constructor
```Dart
  Element(Widget widget)
    : assert(widget != null),
      _widget = widget;
```

#### Properties

```Dart
Element _parent;
int get hashCode => _cachedHash;
final int _cachedHash = _nextHashCode = (_nextHashCode + 1) % 0xffffff;
static int _nextHashCode = 1;

// parent设置的信息，用来定义该child在父类childList中的合适位置
dynamic get slot => _slot;
dynamic _slot;

int get depth => _depth;
int _depth;

// 对应的widget，element的配置信息
Widget get widget => _widget;
Widget _widget;

// 管理element生命周期的对象
BuildOwner get owner => _owner;
BuildOwner _owner;

bool _active = false;

RenderObject findRenderObject() => renderObject;

Map<Type, InheritedElement> _inheritedWidgets;
Set<InheritedElement> _dependencies;
bool _hadUnsatisfiedDependencies = false;

bool get dirty => _dirty;
bool _dirty = true;
bool _inDirtyList = false;
```

#### Method
- [`static int _sort(Element a, Element b){...;}`](#sort)
    - 将两个element根据depth从小到大，dirty从false到true的顺序排序
- [`void reassemble(){...;}`](#reassemble)
    - 只能在调试阶段调用，刷新整棵树
- [`void visitChildren(ElementVisitor visitor) { }`](#visitChildren)
    - Element中空实现，注释中标注其子类必须实现该方法
- [`void visitChildElements(ElementVisitor visitor){...;}`](#visitChildElements)
    - BuildContext的visitChildren的包装
- [`Element updateChild(Element child, Widget newWidget, dynamic newSlot){...;}`](#updateChild)
    - 更改用于配置当前element的widget
- [`void mount(Element parent, dynamic newSlot){...;}`](#mount)
    - 将当前Element根据parent给定的slot添加到树中
- [`void update(covariant Widget newWidget){...;}`](#update)
    - 更新当前Element对应的widget对象
- [`void updateSlotForChild(Element child, dynamic newSlot){...}`](#updateSlotForChild)
    - 更新child的slot
- [`void _updateSlot(dynamic newSlot){...;}`](#updateSlot)
    - 更新当前Element的slot
- [`void _updateDepth(int parentDepth){...;}`](#updateDepth)
    - 根据给定的parentDepth更新当前element的depth
- [`void detachRenderObject(){...;}`](#detachRenderObject)
    - 从RenderTree中移除renderObject
- [`void attachRenderObject(dynamic newSlot){...;}`](#attachRenderObject)
    - 将renderObject通过_slot添加到renderTree指定的位置
- [`Element _retakeInactiveElement(GlobalKey key, Widget newWidget){...;}`](#retakeInactiveElement)
    - TODO 猜测可能是复用，通过key重新获取widget对应的element
- [`Element inflateWidget(Widget newWidget, dynamic newSlot){...;}`](#inflateWidget)
    - 根据给定的widget生成对应的element，并根据给定的slot将该element插入到指定的位置
- [`void deactivateChild(Element child){...;}`](#deactivateChild)
    - 将该元素从element移至inactiveElements列表中，并将其对应的renderObject从renderTree中移除
- [`void _activateWithParent(Element parent, dynamic newSlot){...;}`](#activateWithParent)
    - active给定的parent及其child
- [`static void _activateRecursively(Element element){...;}`](#activateRecursively)
    - 递归active给定的element及其child
- [`void activate(){...;}`](#activate)
    - 将当前element从inactive状态改为active状态
- [`void deactivate(){...;}`](#deactivate)
    - 将当前element从active状态改为inactive
- [`Size get size{...;}`](#getSize)
    - 返回该element对应renderObject的size，只有是RenderBox的时候才有效，否则返回null
- [`InheritedWidget dependOnInheritedElement(InheritedElement ancestor, { Object aspect }) {...;}`](#dependOnInheritedElement)
    - TODO denpendencies还没清楚有什么作用
- [`T dependOnInheritedWidgetOfExactType<T extends InheritedWidget>({Object aspect}) {...;}`](#dependOnInheritedWidgetOfExactType)
    - TODO denpendencies还没清楚有什么作用
- [`InheritedElement getElementForInheritedWidgetOfExactType<T extends InheritedWidget>() {...;}`](#getElementForInheritedWidgetOfExactType)
    - TODO
- [`void _updateInheritance() {...;}`](#updateInheritance)
    - TODO
- [`T findAncestorWidgetOfExactType<T extends Widget>() {...;}`](#findAncestorWidgetOfExactType)
    - TODO
- [`T findAncestorStateOfType<T extends State<StatefulWidget>>() {...;}`](#findAncestorStateOfType)
    - 寻找当前element最近的StatefulElement祖先，并返回其State
- [`T findRootAncestorStateOfType<T extends State<StatefulWidget>>() {...;}`](#findRootAncestorStateOfType)
    - 寻找根祖先，并返回其state
- [`T findAncestorRenderObjectOfType<T extends RenderObject>() {...;}`](#findAncestorRenderObjectOfType)
    - 寻找并返回最近祖先节点的renderObject
- [`void visitAncestorElements(bool visitor(Element element)) {...;}`](#visitAncestorElements)
    - 遍历祖先element，并执行visitor方法
- [`void didChangeDependencies() {...;}`](#didChangeDependencies)
    - 当dependency改变的时候会被调用
- [`void markNeedsBuild() {...;}`](#markNeedsBuild)
    - 标记需要重新build的element
- [`void rebuild() {...;}`](#rebuild)
    - 调用子类实现的performRebuild方法进行rebuild
    - 当buildOwner已经标记当前element为dirty后被buildOwner调用；或当前element第一次build的mount方法之后；或widget有变化的update方法之后
- [`void performRebuild();`](#performRebuild)
    - 抽象方法，Element并没有实现，所有子类必须实现的方法。


#### MethodImple
##### <a name="sort"/>`static int _sort(Element a, Element b){...;}`

```Dart
// 优先depth从小到大，其实dirty为false、true
static int _sort(Element a, Element b) {
    if (a.depth < b.depth)
      return -1;
    if (b.depth < a.depth)
      return 1;
    if (b.dirty && !a.dirty)
      return -1;
    if (a.dirty && !b.dirty)
      return 1;
    return 0;<u></u>
}
```

##### <a name="reassemble"/>`void reassemble(){...;}`

```Dart
// 只能在debug的时候调用
void reassemble() {
    markNeedsBuild();
    visitChildren((Element child) {
      child.reassemble();
    });
  }
```
##### <a name="getRenderObject"/>`RenderObject get renderObject{...;}`

```Dart
// TODO
RenderObject get renderObject {
    RenderObject result;
    void visit(Element element) {
      if (element is RenderObjectElement)
        result = element.renderObject;
      else
        element.visitChildren(visit);
    }
    visit(this);
    return result;
}
```

##### <a name="visitChildren"/>`void visitChildren(ElementVisitor visitor) { }`

```Dart
// 未实现，子类必须实现该方法  TODO，为什么这么写？
void visitChildren(ElementVisitor visitor) { }
```


##### <a name="visitChildElements"/>`void visitChildElements(ElementVisitor visitor){...;}`

```Dart
// BuildContext的visitChildren的包装
void visitChildElements(ElementVisitor visitor) {
    visitChildren(visitor);
}
```

##### <a name="updateChild"/>`Element updateChild(Element child, Widget newWidget, dynamic newSlot){...;}`

```Dart
// 更改用于配置当前element的widget
Element updateChild(Element child, Widget newWidget, dynamic newSlot) {
    if (newWidget == null) {
      // 如果newWidget为空，child不为空，则直接deactivateChild给定的child
      if (child != null)
        deactivateChild(child);
      return null;
    }
    Element newChild;
    
    if (child != null) {
      // 如果newWidget不为空，child不为空
      bool hasSameSuperclass = true; 
      // assert((){ hasSameSuperclass = oldElementClass == newWidgetClass;})
      if (hasSameSuperclass && child.widget == newWidget) {
        // 如果child对应的widget对象等于newWidget对象，
        if (child.slot != newSlot)
          // 新旧slot不一致，更新slot，并将newChild指向当前child
          updateSlotForChild(child, newSlot);
        newChild = child;
      } else if (hasSameSuperclass && Widget.canUpdate(child.widget, newWidget)) { 
        if (child.slot != newSlot)
          // 新旧widget对象不相等，但是两个widget的runtimeType和key一致，slot不一致，则更新slot
          updateSlotForChild(child, newSlot);
        // 更新当前childElement对应的widget为newWidget  
        child.update(newWidget);
        // 将newChild指向当前child
        newChild = child;
      } else {
        deactivateChild(child);
        newChild = inflateWidget(newWidget, newSlot);
      }
    } else {
      // newWidget为空，child为空，直接通过inflateWidget生成newChildElement
      newChild = inflateWidget(newWidget, newSlot);
    }

    return newChild;
}
```

##### <a name="mount"/>`void mount(Element parent, dynamic newSlot){...;}`

```Dart
// 将当前Element根据parent给定的slot添加到树中
void mount(Element parent, dynamic newSlot) {
    _parent = parent;
    _slot = newSlot;
    _depth = _parent != null ? _parent.depth + 1 : 1;
    _active = true;
    if (parent != null) // Only assign ownership if the parent is non-null
      _owner = parent.owner;
    final Key key = widget.key;
    if (key is GlobalKey) {
      key._register(this);
    }
    _updateInheritance();
}
```

##### <a name="update"/>`void update(covariant Widget newWidget){...;}`

```Dart
// 更新当前Element对应的widget对象
void update(covariant Widget newWidget) {
    _widget = newWidget;
}
```

##### <a name="updateSlotForChild"/>`void updateSlotForChild(Element child, dynamic newSlot){...}`

```Dart
// 更新child的slot
void updateSlotForChild(Element child, dynamic newSlot) {
    void visit(Element element) {
      element._updateSlot(newSlot);
      if (element is! RenderObjectElement)
        // 如果当前element不是RenderObjectElement，TODO 访问子类
        element.visitChildren(visit);
    }
    // 更新给定child的slot
    visit(child);
}
```
##### <a name="updateSlot"/>`void _updateSlot(dynamic newSlot){...;}`

```Dart
// 更新当前Element的slot
void _updateSlot(dynamic newSlot) {
    _slot = newSlot;
}
```

##### <a name="updateDepth"/>`void _updateDepth(int parentDepth){...;}`

```Dart
// 根据给定的parentDepth更新当前element的depth
void _updateDepth(int parentDepth) {
    final int expectedDepth = parentDepth + 1;
    if (_depth < expectedDepth) {
      _depth = expectedDepth;
      // 遍历访问child，更新每个child的depth
      visitChildren((Element child) {
        child._updateDepth(expectedDepth);
      });
    }
}
```
##### <a name="detachRenderObject"/>`void detachRenderObject(){...;}`

```Dart
// 从RenderTree中移除renderObject
void detachRenderObject() {
    visitChildren((Element child) {
      child.detachRenderObject();
    });
    _slot = null;
  }
```

##### <a name="attachRenderObject"/>`void attachRenderObject(dynamic newSlot){...;}`

```Dart
// 将renderObject通过_slot添加到renderTree指定的位置
void attachRenderObject(dynamic newSlot) {
    visitChildren((Element child) {
      child.attachRenderObject(newSlot);
    });
    _slot = newSlot;
}
```
##### <a name="retakeInactiveElement"/>`Element _retakeInactiveElement(GlobalKey key, Widget newWidget){...;}`

```Dart
// TODO 猜测可能是复用，通过key重新获取widget对应的element
Element _retakeInactiveElement(GlobalKey key, Widget newWidget) {
    final Element element = key._currentElement;
    if (element == null)
      return null;
    if (!Widget.canUpdate(element.widget, newWidget))
      return null;

    // 将该element从其parent中移除  
    final Element parent = element._parent;
    if (parent != null) {
      parent.forgetChild(element);
      parent.deactivateChild(element);
    }
    // 从_inactiveElements列表中移除该element
    owner._inactiveElements.remove(element);
    return element;
}
```

##### <a name="inflateWidget"/>`Element inflateWidget(Widget newWidget, dynamic newSlot){...;}`

```Dart
// 根据给定的widget生成对应的element，并根据给定的slot将该element插入到指定的位置
Element inflateWidget(Widget newWidget, dynamic newSlot) {
    final Key key = newWidget.key;
    if (key is GlobalKey) {
      // 如果有给widget指定GlobalKey，通过该key拿到widget对应的element
      final Element newChild = _retakeInactiveElement(key, newWidget);
      if (newChild != null) {
        // 如果存在这种element，
        newChild._activateWithParent(this, newSlot);
        final Element updatedChild = updateChild(newChild, newWidget, newSlot);
        return updatedChild;
      }
    }
    // 如果没有指定key，则直接通过createELement生成element
    final Element newChild = newWidget.createElement();
    // 将生成的element通过newSlot添加到指定的位置
    newChild.mount(this, newSlot);
    return newChild;
}
```

##### <a name="deactivateChild"/>`void deactivateChild(Element child){...;}`

```Dart
// 将该元素从element移至inactiveElements列表中，并将其对应的renderObject从renderTree中移除
void deactivateChild(Element child) {
    // 将该element从ElementTree中移除
    child._parent = null;
    // 将该element对应的renderObject从RenderObjectTree中移除
    child.detachRenderObject();
    // 将该element添加到_inactiveElements列表中
    owner._inactiveElements.add(child); // this eventually calls child.deactivate()
}
```

##### <a name="activateWithParent"/>`void _activateWithParent(Element parent, dynamic newSlot){...;}`

```Dart
// active给定的parent及其child
void _activateWithParent(Element parent, dynamic newSlot) {
    _parent = parent;
    // 更新depth
    _updateDepth(_parent.depth);
    // 递归active当前element及其child
    _activateRecursively(this);
    // 将当前元素通过slot添加到renderTree中
    attachRenderObject(newSlot);
}
```
##### <a name="activateRecursively"/>`static void _activateRecursively(Element element){...;}`

```Dart
// 递归active给定的element及其child
static void _activateRecursively(Element element) {
    // 将给定element activate
    element.activate();
    // 将该element的child activate
    element.visitChildren(_activateRecursively);
}
```
##### <a name="activate"/>`void activate(){...;}`

```Dart
// 将当前element从inactive状态改为active状态
void activate() {
    final bool hadDependencies = (_dependencies != null && _dependencies.isNotEmpty) || _hadUnsatisfiedDependencies;
    _active = true;
    _dependencies?.clear();
    _hadUnsatisfiedDependencies = false;
    // 更新_inheritedWidgets
    _updateInheritance();
    if (_dirty)
      // 如果当前element._dirty为true，调用其buildOwner的scheduleBuildFor方法准备重建
      owner.scheduleBuildFor(this);
    if (hadDependencies)
      // 如果该element存在依赖关系  TODO 这里的依赖关系是如何建立的？
      didChangeDependencies();
}
```

##### <a name="deactivate"/>`void deactivate(){...;}`

```Dart
// 将当前element从active状态改为inactive
void deactivate() {
    // 移除依赖关系
    if (_dependencies != null && _dependencies.isNotEmpty) {
      for (final InheritedElement dependency in _dependencies)
        dependency._dependents.remove(this);
    }
    // 将_inheritedWidgets置为空
    _inheritedWidgets = null;
    // _active置为false
    _active = false;
}
```
##### <a name="unmount"/>`void unmount(){...;}`

```Dart
// 将该element状态从inactive转为defunct
void unmount() {
    // 通过key处理？ TODO key到底有什么用？
    final Key key = _widget.key;
    if (key is GlobalKey) {
      key._unregister(this);
    }
}
```

##### <a name="getSize"/>`Size get size{...;}`

```Dart
// 返回该element对应renderObject的size，只有是RenderBox的时候才有效，否则返回null
Size get size {
    final RenderObject renderObject = findRenderObject();
    if (renderObject is RenderBox)
      return renderObject.size;
    return null;
}
```

##### <a name="dependOnInheritedElement"/>`InheritedWidget dependOnInheritedElement(InheritedElement ancestor, { Object aspect }) {...;}`

```Dart
InheritedWidget dependOnInheritedElement(InheritedElement ancestor, { Object aspect }) {
    _dependencies ??= HashSet<InheritedElement>();
    // 将给定的InheritedElement添加到_dependencies的set中
    _dependencies.add(ancestor);
    // 更新依赖？TODO
    ancestor.updateDependencies(this, aspect);
    return ancestor.widget;
}
```

##### <a name="dependOnInheritedElement"/>`T dependOnInheritedWidgetOfExactType<T extends InheritedWidget>({Object aspect}) {...;}`
TODO

##### <a name="getElementForInheritedWidgetOfExactType"/>`InheritedElement getElementForInheritedWidgetOfExactType<T extends InheritedWidget>() {...;}`
##### <a name="updateInheritance"/>`void _updateInheritance() {...;}`
TODO

##### <a name="findAncestorWidgetOfExactType"/>`T findAncestorWidgetOfExactType<T extends Widget>() {...;}`
TODO

```Dart
// 寻找当前element最近的祖先
T findAncestorWidgetOfExactType<T extends Widget>() {
    Element ancestor = _parent;
    while (ancestor != null && ancestor.widget.runtimeType != T)
      ancestor = ancestor._parent;
    return ancestor?.widget as T;
}
```

##### <a name="findAncestorStateOfType"/>`T findAncestorStateOfType<T extends State<StatefulWidget>>() {...;}`

```Dart
// 寻找当前element最近的StatefulElement祖先，并返回其State
T findAncestorStateOfType<T extends State<StatefulWidget>>() {
    Element ancestor = _parent;
    while (ancestor != null) {
      if (ancestor is StatefulElement && ancestor.state is T)
        break;
      ancestor = ancestor._parent;
    }
    final StatefulElement statefulAncestor = ancestor as StatefulElement;
    return statefulAncestor?.state as T;
}
```
##### <a name="findRootAncestorStateOfType"/>`T findRootAncestorStateOfType<T extends State<StatefulWidget>>() {...;}`

```Dart
// 寻找根祖先，并返回其state
T findRootAncestorStateOfType<T extends State<StatefulWidget>>() {
    Element ancestor = _parent;
    StatefulElement statefulAncestor;
    while (ancestor != null) {
      if (ancestor is StatefulElement && ancestor.state is T)
        statefulAncestor = ancestor;
      ancestor = ancestor._parent;
    }
    return statefulAncestor?.state as T;
}
```

##### <a name="findAncestorRenderObjectOfType"/>`T findAncestorRenderObjectOfType<T extends RenderObject>() {...;}`

```Dart
// 寻找并返回最近祖先节点的renderObject
T findAncestorRenderObjectOfType<T extends RenderObject>() {
    Element ancestor = _parent;
    while (ancestor != null) {
      if (ancestor is RenderObjectElement && ancestor.renderObject is T)
        return ancestor.renderObject as T;
      ancestor = ancestor._parent;
    }
    return null;
}
```
##### <a name="visitAncestorElements"/>`void visitAncestorElements(bool visitor(Element element)) {...;}`

```Dart
// 遍历祖先element，并执行visitor方法
void visitAncestorElements(bool visitor(Element element)) {
    Element ancestor = _parent;
    while (ancestor != null && visitor(ancestor))
      ancestor = ancestor._parent;
}
```
##### <a name="didChangeDependencies"/>`void didChangeDependencies() {...;}`

```Dart
// 当dependency改变的时候会被调用
void didChangeDependencies() {
    // 标记当前element为dirty，将其添加到widget列表中，在下一帧的时候进行rebuild
    markNeedsBuild();
}
```

##### <a name="markNeedsBuild"/>`void markNeedsBuild() {...;}`

```Dart
// 标记需要重新build的element
void markNeedsBuild() {
    // 当前element不是active状态
    if (!_active)
      return;
    // 当前element已被标记为dirty  
    if (dirty)
      return;
    // 标记当前element的dirty为true  
    _dirty = true;
    // 通过buildOwner将该element添加到dirtyElement列表中，在下一帧进行rebuild
    owner.scheduleBuildFor(this);
}
```
##### <a name="rebuild"/>`void rebuild() {...;}`

```Dart
// 调用子类实现的performRebuild方法进行rebuild
// 当buildOwner已经标记当前element为dirty后被buildOwner调用；或当前element第一次build的mount方法之后；或widget有变化的update方法之后
void rebuild() {
    performRebuild();
}
```
##### <a name="performRebuild"/>`void performRebuild();`
抽象方法，由个子类去实现。


#### Question
1. dependencies有什么用？