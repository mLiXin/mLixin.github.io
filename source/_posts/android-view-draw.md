---
title: Android View绘制流程
date: 2018-09-04 14:56:33
tags:
- Android
- View
- TODO
categories:
- Android
---
#### 摘要
View的绘制流程主要包括三个过程：measure过程计算View的宽高，layout过程计算View的四个顶点的左边和实际的View的宽高，draw过程绘制View，只有draw方法完成以后，view的内容才会呈现在屏幕上。
<!--more-->

#### Tips
Base on API 27

#### Pre
TODO tag - 为什么View的绘制会有三个过程，涉及到ViewRootImpl，这里需要单独写一篇文章分析。

TODO tag - 要花时间把源码分析过程记录下来

这里先记住，View的绘制流程是从ViewRoot的performTraversals方法开始的，它经过measure、layout和draw三个过程，才能最终将一个View绘制出来，performTraversals会依次调用performMeasure、performLayout和performDraw三个方法，这三个方法分别完成顶级View的measure、layout和draw这三大流程，其中在performMeasure中会调用measure方法，在measure方法中又会调用onMeasure方法，在onMeasure方法中则会对所有的子元素进行measure过程，这个时候measure流程就从父容器传递到子元素中了，这样就完成了一次measure过程。依次类推。同理performLayout和performDraw的传递流程和performMeasure是类似的，唯一不同的是，performDraw的传递过程是在draw方法中通过dispatchDraw来实现的，不过这并没有本质区别。

#### Measure过程
|parentSpecMode/childLayoutParams|EXACTLY|AT_MOST|UNSPECIFIED|
|----|----|----|----|
|dp/dx|EXACTLY+childSize|EXACTLY+childSize|EXACTLY+childSize|
|match_parent|EXACTLY+parentSize|AT_MOST+parentSize|UNSPECIFIED+0|
|wrap_content|AT_MOST+parentSize|AT_MOST+parentSize|UNSPECIFIED+0|
1. 一句话总结Measure过程
	- View的measure过程：如果是at_most和exactly两种模式，测量的大小就是MeasureSpec中的specSize；如果是另外的模式，则还和这个View设置的背景有关
	- ViewGroup的measure过程：除了完成自己的measure过程外，还会遍历去调用子元素的measure方法，各个子元素再递归去执行这个过程。
2. View的MeasureSpec由什么决定？
	- DecorView的MeasureSpec由窗口的尺寸和自己的LayoutParams决定
	- 子View的MeasureSpec由父容器的MeasureSpec和自身的LayoutParams决定

#### Layout过程
1. 一句话总结Layout过程
	- 首先通过setFrame方法来设定View的四个顶点的位置，这样View在父容器中的位置也就确定了，接着调用onLayout方法，这样父容器就能确定子元素的位置了。

#### Draw过程
1. 一句话总结Draw过程
	- 绘制背景
	- 绘制自己
	- 绘制children
	- 绘制装饰 

#### Tips
1. 绘制View的时候要让View支持wrap_content
	- 因为View的layoutParams为wrap_content的时候，它的MeasureSpec是AT_MOST+parentSize，这个时候就会填充满了整个父控件，这个时候要自己去计算内部的大小给一个默认的值。
