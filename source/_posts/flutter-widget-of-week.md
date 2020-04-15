---
title: Flutter Widget-of-Week
date: 2020-04-14 18:21:11
tags:
- Flutter
- Dart
categories:
- Flutter
---
#### 摘要
YouTube上Flutter-Widget of week提到的所有组件一览

<!--more-->
#### 001 SafeArea
- [YouTube](https://www.youtube.com/watch?v=lkF0TQJO0bA&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=2)
- 适用MediaQuery来检测屏幕尺寸，使应用程序的大小能与屏幕匹配
- 外部包裹SafeArea即可

#### 002 Expanded
- [YouTube](https://www.youtube.com/watch?v=_rnZaagadyo&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=3)
- ![Layout->Expanded](/images/flutter-guide/flutter-layout-expanded.gif)
- {% iframe /images/flutter-guide/flutter-layout-expanded.gif %}
- tips
    - Row、Column中，使其中一个child伸展并填补额外的空间。当Row和Column布置它的子项的时候，会首先执行不灵活的子项，然后将剩余空间划分给灵活的子项，如Expanded。
    - 可以设置灵活因子`flex:2`防止竞争，类似Android里面的weight

#### 003 Wrap
- [YouTube](https://www.youtube.com/watch?v=z5iw2SeFx2M&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=4)
- ![Layout->Wrap](/images/flutter-guide/flutter-layout-wrap.gif)
- tips
    - 当Row或者Column一行放不下的时候，就会溢出屏幕，就可以使用wrap替换，当一行放不下的时候，自动新增一行。
    - `direction`：配置横向还是纵向
    - `spacing`:横向padding
    - `runspacing`：纵向padding

#### 004 AnimatedContainer
- [YouTube](https://www.youtube.com/watch?v=yI-8QHpGIP4&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=5)
- ![Animation->AnimatedContainer](/images/flutter-guide/flutter-animation-animatedcontainer.gif)
- tips
    - 对color、borders、border-radius、background-image、shadows、gradients等等实施线性插值法进行动画变化，
    - `duration`：配置动画持续时间

#### 005 Opacity 透明度
- [YouTube](https://www.youtube.com/watch?v=9hltevOHQBw&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=6)
- ![Painting->Opacity](/images/flutter-guide/flutter-painting-opacity.gif)
- tips
    - 可以理解为控制透明度
    - 不显示某个部件，但是又保留它的位置
    - 将两个部件重叠，同时设置AnimatedOpacity，可以创建动画
    
#### 006 FutureBuilder
- [YouTube](https://www.youtube.com/watch?v=ek8ZPdWj4Qo&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=7)
- ![Async->Futurebuilder](/images/flutter-guide/flutter-async-futurebuilder.gif)
- tips
    - 异步获取数据后构建widget
    - 注意对snapshot数据状态进行判断

#### 007 FadeTransition
- [YouTube](https://www.youtube.com/watch?v=rLwWVbv3xDQ&list=PLjxrf2q8roU23XGwz3Km7sQZFTdB996iG&index=8)
- ![Animation->FadeTransition](/images/flutter-guide/flutter-animation-fadetransition.gif)
- tips
    - 淡入淡出动画的简单版
    - 需要controller，注意回收
