---
title: Flutter入门(二) Flutter Widget一览
date: 2020-04-09 15:46:51
tags:
- Flutter
- Dart
categories:
- Flutter
---
#### 摘要
总结Flutter都提供哪些原生组件，具体每个组件有什么参数、每个参数有什么作用都可以直接去看源码，这里不特别注明。开发中遇到坑，再来这里提交说明。

youtube上Flutter有个系列：Widget of the week，基本上每个小部件都会有说明，可以参考。地址：[需要搭梯子](https://www.youtube.com/watch?v=b_sQ9bMltGU&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG)

Flutter现在支持Android、Ios、MacOS、Windows、Linux、Web，真香。

<!--more-->

#### Accessibility - 辅助功能Widget
##### ExcludeSemantics
##### mergeSemantics
##### Semantics

#### Animation and motion - 动画和Motion
##### AnimatedBuilder
- 构建动画的组件

##### AnimatedContainer
- 一段时间内会改变值的Container？

##### AnimatedCrossFade
- 在给定的两个Child Widget间淡入淡出？

##### AnimatedDefaultTextStyle
- 文字动画变化？

##### AnimatedListState
- 一个Scrolling container在插入和删除时动画的状态？

##### AnimatedModalBarrier
- 字面意思屏障？防止用户在widget自己变化之前影响widget？

##### AnimatedOpacity
- 透明度动画？

##### AnimatedPhysicalModel
- 物理模型动画？

##### AnimatedPositioned
- 位置变化动画？

##### AnimatedSize
- 尺寸变化动画

##### AnimatedWidget
- 根据给定变化的值重建widget？

##### AnimatedWidgetBaseState
- 基础状态类？

##### DecoratedBoxTransition
- DecoratedBox变化动画

##### FadeTransition
- 淡入淡出变化动画

##### Hero
- 标记一个child widget并成为大页面的动画？

##### PositionedTransition
- 位置变化动画

##### RotationTransition
- 旋转变化动画

##### ScaleTransition
- 收缩、放大动画

##### SizeTransition
- 尺寸变化动画

##### SlideTransition
- 滑动动画？

#### Assets, images, and icon
##### AssetBundle
- 包含可以在app中使用的images和字符串等资源

##### Icon

##### Image

##### RawImage
- 立即展示一个dart:ui的image

#### Async
##### FutureBuilder
- 基于Future最新反馈的数据来构建自己

##### StreamBuilder
- 基于Stream最新反馈的数据来构建自己

#### Basics - 基础Widget
##### Appbar
- ![Basics->Appbar](/images/flutter-basics-appbar.png)
- 说明

##### Column
- 布局排列方式，内部children竖直排列，约等于`orientation=vertical`的`LinearLayout` 

#### Container
- 暂时理解为包裹类，如果需要给类似Text设置padding、margin等都需要外部包裹一个Container，因为Text这些是没有padding、margin这种参数可以配置。
 	
##### FlutterLogo
- 就是FlutterLogo，实际开发用不到感觉

##### Icon
- 就是图标，Flutter内置了很多图标，通过`Icons.xx`使用

##### Image
- 图片

##### Placeholder
- 占位widget，用来在开发过程中表明这里还没有开发完成？好像没有用处

##### RaisedButton
- Material风格的Button

##### Row
- 布局排列方式，内部children横向排列，约等于`orientation=horizontal`的`LinearLayout` 
	
##### Scaffold
- 实现了基本的Material风格的布局结构

##### Text
- 文字

#### Cupertino(iOS-style widgets)
##### CupertinoActionSheet
- ios风格的底部表单弹框

##### CupertinoActivityIndicator
- ios风格的loading

##### CupertinoAlertDialog
- ios风格的提示弹框

##### CupertinoButton
- ios风格的按钮

##### CupertinoContextMenu
- ios风格，长按弹出菜单

##### CupertinoDatePicker
- ios风格时间选择器

##### CupertinoDialog
- ios风格弹框

##### CupertinoDialogAction
- iOS风格弹框按钮

##### CupertinoFullscreenDialogTransition
- ios风格全屏变化动画

##### CupertinoNavigationBar
- ios风格顶部导航栏

##### CupertinoPageScaffod
- ios风格页面布局结构

##### CupertinoPageTransition
- ios风格页面跳转动画

##### CupertinoPicker
- ios风格选择器

##### CupertinoPopupSurface
- ios风格弹框接口

##### CupertinoScrollbar
- ios风格侧滑栏

##### CupertinoSegmentedControl
- ios风格顶部tab

##### CupertinoSlider
- ios风格滑动进度条

##### CupertinoSlidingSegmentedControl
- ios风格滑动tab

##### CupertinoSwitch
- ios风格switch按钮

##### CupertinoTabBar
- ios风格底部tabBar

##### CupertinoTabScaffold
- ios风格tab布局结构

##### CupertinoTabView
- ios风格tabView

##### CupertinoTextField
- ios风格输入框

##### CupertinoTimerPicker
- ios风格时间选择器

#### Input
##### Form
- 可以理解为表单

##### FormField
- 一个表单输入

##### RawKeyboardListener
- 键盘监听器？

#### Interaction Models - 交互类
##### AbsorbPointer
- 吸收属性，阻止触摸事件访问到下面的小部件

##### Dismissible
- 滑动触发删除小部件

##### DragTarget
- 拖拽widget

##### Draggable
- 可拖拽

##### GestureDetector
- 手势识别

##### IgnorePointer
- ？？？

##### LongPressDraggable
- 长按拖拽

##### Scrollable
- 滑动widget

##### Hero
- 标记child并成为新页面的main？

##### Navigator
- 路由跳转


#### Layout
##### Align
##### AspectRatio
##### Baseline
##### Center
##### ConstrainedBox
##### Container
##### CustomSingleChildLayout
##### Expand
##### FittedBox
##### FractionallySize
##### IntrinsicHeight
##### IntrinsicWidth
##### LimitedBox
##### Offstage
##### OverflowBox
##### Padding
##### SizedBox
##### SizedOverflowBox
##### Transform

##### Column
##### CustomMultiChildLayout
##### Flow
##### GridView
##### IndexedStack
##### LayoutBuilder
##### ListBody
##### ListView
##### Row
##### Stack
##### Table
##### Wrap

#### Material Components
##### Appbar
##### BottomNavigationBar
##### Drarwer
##### MaterialApp
##### Scaffold
##### SliverAppBar
##### TabBar
##### TabBarView
##### WidgetsApp
##### ButtonBar
##### DropdownButton
##### FlatButton
##### FloatingActionButton
##### IconButton
##### OutlinButton
##### PopupMenuButton
##### RaisedButton
##### Checkbox
##### Data&Time Pickers
##### Radio
##### Slider
##### Switch
##### TextField
##### AlertDialog
##### BottomSheet
##### ExpansionPanel
##### SimpleDialog
##### SnackBar
##### Card
##### Chip
##### CircularProgressIndicator
##### DataTable
##### GridView
##### Icon
##### Image
##### LinearProgressIndicator
##### Tooltip
##### Divider
##### ListTile
##### Stepper

#### Painting and effects
##### BackdropFilter
##### ClipOval
##### ClipPath
##### ClipRect
##### CustomPaint
##### DecoratedBox
##### FractionalTranslation
##### Opacity
##### RotatedBox
##### Transform

#### Scrolling
##### CustomScrollView
##### GridView
##### ListView
##### NestedScrollView
##### NotificationListener
##### PageView
##### RefreshIndicator
- 下拉刷新loading

##### ScrollConfiguration
##### Scroll
##### Scrollbar
##### SingleChildScrollView

#### Styling
##### MediaQuery
- 媒体查询？啥？

##### Padding
- 给内部child添加padding

##### Theme
- 对下面的所有widget适用

#### Text
##### DefaultTextStyle
- 默认的文字样式，对下面的所有Text Widget有效

##### RichText
- 富文本

##### Text

    