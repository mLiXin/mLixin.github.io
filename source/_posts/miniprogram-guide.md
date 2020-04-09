---
title: 微信小程序-开发指南-学习笔记
date: 2020-04-09 10:34:03
tags:
- 小程序
- 学习笔记
categories:
- 小程序
---
#### 摘要
[微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/code.html#JSON-%E9%85%8D%E7%BD%AE)
#### 起步
- 代码构成
    - json：静态配置
        - app.json
            - 全局配置，包括了小程序的所有页面路径、界面表现、网络超时时间、底部 tab 等。
        - project.config.json 
            - 开发工具的配置，换电脑开发可以同步更新
        - pages/logs/logs.json
            - 独立定义每个页面的颜色
    - wxml
        - 等同于html，元素标签名不一样，MVVM模式，`{ {}}`将数据和页面绑定
    - wxss
        - rpx尺寸单位用来兼容尺寸
        - 可以新增app.wxss配置全局样式，page.wxss配置当前当前页面样式

- 宿主环境
    - 逻辑层、渲染层
        - 渲染层(wxml/wxss),多个页面，多个webview线程
        - 逻辑层(js)
        - 两层之间通信由Native做中转，逻辑层的网络通信由Native做转发
    - 程序和页面
        - app.json中，pages里面的第一个页面为小程序的首页
        - 加载页面的时候，首先会根据.json配置生成一个页面，然后装载wxml结构和wxss样式，最后加载.js

#### 开发指南
##### 代码组成
###### JSON配置
- 静态配置，小程序运行之前就决定的，无法在运行过程中动态更新。
- key-value形式，key只能由双引号表示，value可以是数字、字符串、bool、数组[]、对象{}和Null

###### WXML模板
- 属性是大小写敏感的
- 通过 `{ {变量名}}` 来绑定 WXML 文件和对应的 JavaScript 文件中的 data 对象属性。
- 可以定义模板代码，使用name属性为名字，`<template/>`内定义代码
    - 两种引用方式：
        - import，引入目标文件的代码段，不具备递归性

###### WXSS样式
- 引入rpx，适配不同宽度的屏幕。宽度为375物理像素的屏幕下，1rpx = 1px。(iPhone6屏幕宽度为375px，共750个物理像素，那么1rpx = 375 / 750 px = 0.5px。) 
- 通过`@import './test_0.wxss'`引用外部的样式；支持内联样式
    - 多种选择器：
        - 类选择器：`.intro`
        - id选择器：`#id`
        - 元素选择器：`view checkbox`
        - 伪元素选择器：`view::after/view::before`,在view组件后面或前面插入内容
- 官网样式库：WeUI.wxss

###### JavaScript脚本  
- JavaScript构成
    - 浏览器中的JavaScript = ECMASript + DOM(文档对象模型) + BOM(浏览器对象模型)
    - NodeJS中的JavaScript = ECMAScript + NPM + Native
    - 小程序中的JavaScript = ECMAScript + 小程序框架 + 小程序API
- 注意勾选ES6转ES5，兼容ios9、10版本。
- 模块化
    - 小程序中可以将任何一个JavaScript 文件作为一个模块，通过`module.exports`或者 exports 对外暴露接口，通过`require(path)`将公共代码引入
- 脚本的执行顺序
    - 小程序的执行的入口文件是`app.js`。并且会根据其中`require`的模块顺序决定文件的运行顺序;当 app.js 执行结束后，小程序会按照开发者在`app.json` 中定义的`pages`的顺序，逐一执行。
- 作用域
    - 在文件中声明的变量和函数只在该文件中有效，不同的文件中可以声明相同名字的变量和函数，不会互相影响
    - 当需要使用全局变量的时，通过使用全局函数 getApp() 获取全局的实例，并设置相关属性值，来达到设置全局变量的目的；当需要保证全局的数据可以在任何文件中安全的被使用到，那么可以在 App() 中进行设置。

##### 理解小程序宿主环境
###### 渲染层和逻辑层
- WXML模板和WXSS样式工作在渲染层，JS脚本工作在逻辑层。
    - 渲染层和数据相关
    - 逻辑层负责产生、处理数据。
    - 逻辑层通过Page实例的setData方法传递数据到渲染层。

- 渲染层和逻辑层分别由两个线程管理：渲染层的界面使用WebView进行渲染；逻辑层采用JsCore线程运行脚本
    - 多个页面存在多个WebView线程
    - 线程间通信、网络请求都由Native中转、转发

- 数据驱动基本原理
    - 对比前后两个JS对象的变化，并将这个差异应用到原来的Dom树上，从而达到更新UI的目的。

###### 程序与页面
- App构造器的参数
    - onLaunch
        - 初始化完成时，会触发onLaunch(全局触发一次)
    - onShow
        - 当小程序启动，或从后台进入前台显示，会触发onShow
    - onHide
        - 当小程序从前台进入后台，会出发onHide
    - onError
        - 当小程序发生脚本错误，或者API调用失败时，会触发onError并带上错误信息
    - 其他字段
        - 可以添加任意函数或数据到Object参数中，在App实例回调用this访问

- 生命周期
    - 初次进入小程序，微信客户端初始化好宿主环境，同时从网络下载或者从本地缓存中拿到小程序的代码包，把它注入到宿主环境，初始化完毕后，微信客户端就会给App实例派发onLaunch事件，App构造器参数所定义的onLaunch方法会被调用。
    - 点击右上角关闭，或者按手机设备的Home键离开小程序，即小程序进入后台状态，App构造器参数所定义的onHide方法会被调用
    - 再次回到微信或再次打开小程序，微信客户端会把后台的小程序唤醒，即进入前台状态，App构造器参数所定义的onShow方法会被调用。

- 全局数据
    - 每个页面各自有一个WebView线程进行渲染，但是逻辑层的JS脚本运行上下文依旧在同一个JsCore线程中。
    - setTimeout或者setInterval的定时器，在页面跳转的时候并没有被清除，需要自己在页面离开的时候进行清理。

- 文件构成和路径
    - 界面：WXML+WXSS
    - 配置：JSON
    - 逻辑：JS脚本

- 页面路径需要在小程序代码根目录app.json中的pages字段声明，否则不会被注册到宿主环境中。

- 页面构造器Page()：Page()在页面脚本page.js中调用
    - data：页面初始数据
    - onLoad：生命周期函数--监听页面加载，触发时机早于onShow和onReady
    - onReady：生命周期函数--监听页面初次渲染完成
    - onShow：生命周期函数--监听页面显示，触发时机早于onReady
    - onHide：生命周期函数--监听页面隐藏
    - onUnload：生命周期函数--监听页面卸载
    - onPullDownRefresh：页面相关事件处理函数--监听用户下拉动作
    - onReachBottom：页面上拉触底事件的处理函数
    - onShareAppMessage：用户点击右上角转发
    - onPageScroll：页面滚动触发事件的处理函数
    - 其他：可以添加热议的函数或数据，在Page实例的其他函数中用this可以访问

- wx.navigateTo切换到其他页面、底部tab切换时候触发onHide
- 当前页面使用wx.redirectTo或者wx.navigateBack返回到其他页的时候，当前页面会被微信客户端销毁回收，onUnload会被调用。
- 小程序把页面的打开路径定义成页面URL，其组成格式和网页的URL类似，在页面路径后使用英文 ? 分隔path和query部分，query部分的多个参数使用 & 进行分隔，参数的名字和值使用 key=value 的形式声明。例如：`wx.navigateTo({ url: 'pages/detail/detail?id=1&other=abc' })`,在Page中使用`option.id/option.other`获取参数

- 可以在Page实例下的方法调用this.setData将数据传递给渲染层，从而达到更新界面的目的。
    - `this.setData({text:'change data'},function(){ // 在这次setData对界面渲染完毕后触发})`

- attention：
    - 只有this.setData来改变页面的状态
    - setData需要两个线程的一些通信消耗，为了提高性能，每次设置的数据不应超过1024kb
    - 不要把data中的任意一项的value设为undefined，否则可能会引起一些不可预料的bug

- 用户行为
    - onPullDownRefresh
        - 需要在app.json的window选项中或页面配置page.json中设置enablePullDownRefresh为true，wx.stopPullDownRefresh可以停止当前页面的下拉刷新
    - onReachBottom
    - onPageScroll
    - onShareAppMessage

- 页面跳转和路由
    - 可以通过wx.navigateTo推入一个新的页面，组成页面栈，页面站的最大层级为10层，达到10层之后就没办法再推入新的页面了。
    - 导航相关api
        - wx.navigateTo({url:"xxx"})：推入新页面
        - wx.navigateBack()：退出当前页面栈最顶上页面
        - wx.redirectTo({url:"xxx"})：替换当前页面为xxx
        - wx.switchTab：打开Tabbar页面
        - wx.reLaunch：重启小程序

###### 组件
- 所有组件名和属性都是小写，多个单词以“-”进行连接

- 组件的共有属性
    - id
    - class
    - style：内联样式
    - hidden
    - data-*：自定义属性，组件上触发的事件时，会发送给事件处理函数
    - bind/catch：事件

- 特有属性：
    - https://mp.weixin.qq.com/debug/wxadoc/dev/component/。

###### API
- 所有小程序的API都挂载在wx对象底下。
    - wx.on*开头的API是监听某个事件发生的API接口，接受一个Callback函数作为参数。
    - 如未特殊约定，多数API接口为异步接口，都接受一个Object作为参数
    - API的Object参数一般由success、fail、complete三个回调来接收接口调用结果。
    - wx.get*开头的API是获取宿主环境数据的接口
    - wx.set*开头的API是写入数据到宿主环境的接口

- 官方API文档：[https://mp.weixin.qq.com/debug/wxadoc/dev/api/](https://mp.weixin.qq.com/debug/wxadoc/dev/api/)

###### 事件
- 将用户在渲染层的行为反馈、组件的部分状态反馈抽象为渲染层传递给逻辑层的事件。
- 常见的事件类型：
    - touchstart
    - touchmove
    - touchcancel
    - touchend
    - tap
    - longpress：手指触摸后，超过350ms再离开
    - longtap
    - transitionend：WXSS transition或wx.createAnimation动画结束后触发
    - animationstart：WXSS animation动画开始时触发
    - animationiteration：WXSSannimation一次迭代结束时触发
    - animationend：WXSS animation动画完成时触发

- 事件对象属性：
    - target和currentTarget的区别：
        - currentTarget为当前事件所绑定的组件，而target则是触发该事件的源头组件。

- bind和capture-bind的含义分别代表事件的冒泡阶段和捕获阶段。
- bind事件绑定不会阻止冒泡事件向上冒泡，catch事件绑定可以阻止冒泡事件向上冒泡。即catch可以阻止事件的传递。

###### 兼容
- 针对不同手机进行程序上的兼容：
    - wx.getSystemInfo或者wx.getSystemInfoSync来获取手机品牌、操作系统版本号、微信版本号以及小程序基础库版本号等。

- 可以通过判断此API是否存在来做程序上的兼容。
- wx.canIUse用于判断接口或者组件在当前宿主环境是否可用：
    - `${API}.${method}.${param}.${options}`
    - `${component}.${attribute}.${option}`

##### 场景应用
- 流程
    - 优先完成WXML+WXSS还原设计稿
    - 梳理出每个页面的data部分，填充WXML的模板语法
    - 完成JS逻辑部分

###### 基本的布局方法-Flex布局
- Flex是更灵活的布局模型，使容器能通过改变里面项目的高宽、顺序，来对可用空间实现最佳的填充，方便适配不同大小的内容区域。
- 容器的属性：
    - display:flex
    - flex-direction:row(default) | row-reverse | column | column-reverse
        - 通过设置坐标轴来设置项目排列方向，默认从左到右
    - flex-wrap:nowrap(defalut) | wrap | wrap-reverse
        - 设置是否允许项目多行排列，以及多行排列时换行的方向，默认不换行，如果单行内容过多，则溢出容器
    - justify-content:flex-start(default) | flex-end | center | space-between | space-around | space-evenly
        - 设置项目在主轴方向上对齐方式，以及分配项目之间及其周围多余的空间，默认项目对齐主轴七店，项目间不留空隙
    - align-items:stretch(default) | center | flex-end | baseline | flex-start
        - 设置项目在行中的对齐方式，默认项目拉伸至填满行高
    - align-content:Stretch(default) | flex-starat | center | flex-end | space-between | space-around | space-evenly
        - 多行排列时，设置行在交叉轴方向上的对齐方式，以及分配行之间及其周围多余的空间，默认当未设置项目尺寸，将各行中的项目拉伸至填满交叉轴。当设置了项目尺寸，项目尺寸不变， 项目行拉伸至填满交叉轴

- 项目的属性：
    - order:0(default) | <integer>
        - 设置项目沿主轴方向上的排列顺序，数值越小，排列越靠前。
    - flex-shrink:1(default) | <number>
        - 项目在主轴方向上溢出时，通过设置项目收缩因子来压缩项目适应容器。
    - flex-grow:0(default) | <number>
        - 项目在主轴方向上还有剩余空间时，通过设置项目扩张因子进行剩余空间的分配。
    - flex-basis:auto(default) | <length>
        - flex-basis和width、height同时存在时，优先级高于width、height，即该属性可以代替项目的width或height属性。当有一个属性为auto时，非auto的优先级更高。
    - flex:none | auto | @flex-grow @flex-shrink @flex-basis
        - 简写方式
    - align-self:auto(default) | flex-start | flex-end | center | baseline | stretch
        - 设置项目在行中交叉轴方向上的对齐方式，用于覆盖容器的align-items

- 默认情况下，水平方向是主轴，垂直方向是交叉轴。项目是在主轴上排列，排满后在交叉轴方向换行。

###### 界面常见的交互反馈
- 触摸反馈
    - view容器组件和button组件提供了hover-class属性，触摸时会往该组件加上对应的class改变组件的样式。
    - button按钮处理耗时操作时，可以使用button组件的loading属性，在按钮文字前面出现一个Loading。

- Toast和模态对话框
    - Toast提示默认1.5秒后自动消失：wx.showToas
    - 模态对话框可以用来提示操作结果状态同时附带下一步操作的指引：wx.showModal

- 界面滚动
    - 如果不想整个页面进行滚动，而只是部分区域可以滚动，可以用scroll-view实现。

###### 发起HTTPS网络通信
- wx.request接口
    - url：开发者服务器接口地址
    - data：请求的参数
    - header：设置请求的header，header不能设置Referer，默认header['content-type'] = 'application/json'
    - method:默认GET，大写
    - dataTYpe：默认json
    - success:收到开发者服务成功返回的回调函数
        - 触发success回调钱，小程序宿主环境会对data字段的值做JSON解析，如果解析成功，则data字段的值会被设置成解析后的Object对象，其他情况data字段都是String类型
    - fail：接口调用失败的回调函数
    - complete：接口调用结束的回调函数

- wx.request请求的域名必须是https，同时需要在小程序管理平台进行配置。使用未配置的域名会报错
    - 开发者工具、小程序的开发版、体验版在某些情况下允许wx.request请求任意域名

- 一般使用技巧：
    - 设置超时时间：在app.json中设置 `{networkTimeout:{"request":3000}}`
    - 请求前后的状态管理：在请求之前showLoading，在请求complete中进行hideLoading，同时添加hasClick锁防止两次点击

###### 微信登录
- 微信登录过程：
    - `小程序`通过wx.login()请求`微信服务器`获取微信登录凭证code
    - `小程序`通过wx.request请求`第三方服务器`把code带到自己服务器
    - `第三方服务器`请求`微信服务器`通过code和其他信息换取用户id
    - `第三方服务器`绑定微信用户ID和自己的业务用户ID
    - `第三方服务器`生成自己的业务凭证sessionID
    - `第三方服务器`返回给`小程序`业务登录凭证sessionID
    - `小程序`下一次wx.request带上sessionID请求`第三方服务器`

###### 本地数据缓存
- 读写本地数据缓存
    - 通过wx.getStorage/wx.getStorageSync读取本地缓存
    - 通过wx.setStorage/wx.setStorageSync写数据到缓存。
    - sync后缀的接口表示是同步接口

- 每个小程序的额缓存空间上限是10MB，如果已经达到10MB，再通过wx.setStorage写入缓存会触发fail回调

- 利用本地缓存提前渲染界面
    - 如果本地有缓存，则优先加载缓存数据渲染页面，再请求网络获取数据后刷新页面。对数据实时性/一致性要求不高的页面可以这样渲染，用来优化体验。

- 缓存用户登录态SessionId

###### 设备能力
- 利用微信扫码能力：`wx.scanCode`调起微信扫一扫
- 获取网络状态：`wx.getNetworkType`

##### 小程序的协同工作和发布
- 发布前检查：
    - 如果使用到Flex布局并且兼容ios8一下系统：检查上传小程序包时，开发者工具是否已经开启“上传代码时自动补齐”
    - 服务器接口使用HTTPS协议，并且对应的网络域名确保已经在小程序管理平台配置好。
    - 调试模式，微信不会校验域名合法性，容易导致开发者误以为测试通过，而正式版小程序因为遇到非法域名而无法工作
    - 检查网络接口已经部署好，并评估好服务器的机器负载情况。

##### 底层框架
###### 双线程模型
- 技术选型
    - 每个小程序页面都用不同的WebView去渲染，可以提供更好的交互体验，更贴近原生体验，也避免单个WebView的任务过于繁重。

- 管控与安全
    - 需要提供一个沙箱环境来运行开发者的代码，这个环境中不能有任何浏览器相关的接口，只提供纯JavaScript的解释执行环境，如HTML5中的ServiceWorker、WebWorker都是启用另一个线程来执行JavaScript。
    - 基于客户端系统有JavaScript的解释引擎(ios是内置的JavaScriptCore框架，安卓是腾讯x5内核提供的JsCore环境)，可以创建一个单独的线程去执行JavaScript，在这个环境下执行有关小程序业务逻辑的所有代码。

- 天生的延时
    - 渲染首屏的时候，逻辑层和渲染层会同时开始初始化工作，但是渲染层需要有逻辑层的数据才能把界面渲染出来，因此逻辑层与渲染层需要有一定的机制保证时序正确。
    - 除了逻辑层与渲染层之间的通信有延时，各层与客户端原生交互同样是有延时的。开发者代码是跑在逻辑层上，而客户端原生是跑在微信主线程智商，所以注册给逻辑层有关客户端能力的接口，实际上也是跟微信主线程之间的通信，所以也是延时的。

###### 组件系统
- Exparser框架
    - Exparser是微信小程序的组件组织框架，内置在小程序基础库中，为小程序的各种组件提供基础的支持。小程序内的所有组件，包括内置组件和自定义组件，都是由Exparser组织管理。
    - Exparser会维护整个页面的节点数相关信息，包括节点的属性、时间的绑定等。相当于一个简化版的Shadow DOM实现。
    - 特点：
        - 不依赖浏览器的原生支持，也没有其他依赖库，实现的时候还针对性地增加了其他API以支持小程序组件编程
        - 可以在纯JS环境中运行，逻辑层也有一定的组件树组织能力
        - 高效轻量：性能表现好，在组件实例极多的环境下表现尤其右移，同时代码尺寸较小。

- 自定义组件
    - ShadowTree，组件内部的实现；最终拼接成的也没节点树被称为Composed Tree，即将页面所有组件节点树合成之后的树。
    - 每个组件都分别拥有自己的独立的数据、setData调用，createSelectorQuery也将运行在ShadowTree的层面上。

- 运行原理
    - Exparser会接管所有的自定义组件注册与实例化。以Component为例，在小程序启动的时候，构造器会将开发者设置的properties、data、methods等顶一段，写入Exparser的组件注册表中。这个组件在被其他组件引用时，就可以根据这些注册信息来创建自定义组件的实例。
    - 在初始化页面的时候，Exparser会创建出页面根组件的一个实例，用到的其他组件也会相应创建组件实例。

- 组件创建过程：
    - 根据组件注册信息，从组件原型上创建出组件节点的JS对象， 即组件的this
    - 将组件注册信息中的data复制一份，作为组件数据，即this.data
    - 将这份数据结合组件WXML，据此创建出Shadow Tree，由于Shadow Tree中可能引用有其他组件，因而这会递归触发其他组件穿件过程
    - 将Shadow Tree拼接到Composed Tree上，并生成一些缓存数据用于优化组件更新性能
    - 触发组件的created生命周期函数
    - 如果不是页面根组件，需要根据组件节点上的属性定义，来设置组件的属性值
    - 当组件实例被展示在页面上时，触发组件的attached生命周期函数，如果Shadow Tree中有其他组件，也会逐个触发它们的生命周期

- 组件间通信
    - WXML属性值传递
        - 父组件向子组件
    - 事件系统
        - 子组件向父组件
    - selectComponent
    - relations

- 自定义组件中使用triggerEvent触发事件时，可以指定事件的bubbles、composed和capturePhase属性，用于标注事件的冒泡行止

###### 原生组件
- 并不完全在Exparser的渲染体系下，而是由客户端原生参与组件的渲染。这类组件就是原生组件。
- 引入原生组件的三个好处：
    - 扩展Web的能力，比如输入框组件，有更好的控制键盘的能力
    - 体验更好，同时减轻WebView的渲染工作。
    - 绕过setData、数据通信和重渲染流程，使渲染性能更好。

- 常用的几个原生组件
    - video
    - map
    - canvas
    - picker

- 交互比较复杂的原生组件都会提供context，用于直接操作组件。

- 原生组件渲染限制
    - 一些CSS样式无法应用于原生组件。
    - 原生组件会浮于页面其他组件智商，使其他组件不能覆盖在原生组件上展示。--考虑使用cover-view和cover-image组件。

###### 小程序与客户端通信原理
- 视图层与客户端的交互通信：
    - ios利用WKWebView提供的messageHandlers特性
    - 安卓是往WebView的window对象注入一个原生方法， 最终会封装成WeiXinJSBridge这样一个兼容层，主要提供调用和监听两种方法，

- 逻辑层与客户端原生通信机制
    - 与渲染层类似
    - 不同在于，iOS平台可以往JavaScriptCore框架注入一个全局的原生方法， 而安卓和渲染层一致。

##### 性能优化
###### 启动
- 小程序启动流程：
    1. 展示启动界面
    2. 判断小程序是否已缓存？否的话，直接进4，否则进3
    3. 判断是否为最新版本？是的话，直接进5，否则进4
    4. 下载小程序代码包
    5. 加载小程序代码包
    6. 初始化小程序首页

- 下载到的小程序代码包不是小程序的源代码，而是编译、压缩、打包之后的代码包。
- 控制代码包大小的方法：
    - 精简代码，去掉不必要的WXML结构和未使用的WXSS定义
    - 减少代码包中直接嵌入的资源文件
    - 压缩图片，使用适当的图片格式。
    
- 如果优化后代码总量仍然比较大，可以采用分包加载的方式进行优化
    - 一个主包：包含小程序启动时会马上打开的页面代码和相关资源。
    - 其余是分包：其余的代码和资源。

- 如何实现分包？
    - app.json中，pages中为主包，subPackages为分包

- 小程序的代码会被加载到适当的线程中执行。此时，所有app.js、页面所在的JS文件和所有其他被require的JS文件会被自动执行一次，小程序基础库会完成所有页面的注册。
- 如果一个页面被多次创建，并不会使得这个页面所在的JS文件被执行多次，而仅仅是根据初始数据多生成了一个页面实例，在页面JS文件中直接定义的变量，在所有这个页面的实例间是共享的。

###### 页面层级准备
- 小程序的每一个页面都独立运行在一个页面层级上。
    - 调用wx.navigateTo会创建一个新的页面层级
    - 调用wx.navigateBack会销毁一个页面层级
    - 调用wx.redirectTo不会打开一个新的页面层级，而是将当前页面层级重新初始化：重新传入页面的初始数据、路径等。

- 页面层级的准备分为三个阶段：
    - 启动一个WebView
    - 在WebView中初始化基础库，还会进行一些基础库内部优化，以提升页面渲染性能
    - 注入小程序WXML结构和WXSS样式，使小程序能在接收到页面初始数据之后马上开始渲染页面。

###### 数据通信
- 进行setData调用时需要遵循的原则：
    - 不要过于频繁调用setData，应考虑将多次setData合并成一次setData调用
    - 数据通信的性能与数据量正相关，因此如果有一些数据字段不在界面中展示且数据结构比较复杂或包含长字符串，则不应使用setData来设置这些数据
    - 与界面渲染无关的数据最好不要设置在data中，可以考虑设置在page对象的其他字段下。

- 视图层将事件反馈给逻辑层时，需要一个通信过程，通信方向是从视图层到逻辑层。这个通信过程是异步的，会产生一定延迟。延迟时间与传输的数据量正相关，数据量小于64kb时在30ms以内。

- 降低延迟事件的两个方法：
    - 去掉不必要的时间绑定(WXML中的bind和catch)，从而减少通信的数据量和次数
    - 事件绑定时需要传输target和currentTarget的dataset，因为不要在节点的data前缀属性中放置过大的数据。

###### 视图层渲染
- 视图层收到初始数据时需要进行初始渲染，每次收到更新数据时需要执行重渲染
- 初始渲染：
    - 初始渲染发生在页面刚刚创建时，将初始数据套用在对应的WXML片段上生成节点树。时间开销大体上与节点树中节点的总量成正比例关系，因而减少WXML中节点的数量可以有效降低初始渲染和重渲染的时间开销，提升渲染性能。

- 重渲染：
    - 每次应用setData数据时，都会执行重渲染来更新界面。
    - 每次重渲染的时候，将data和setData数据套用在WXML片段上，得到一个新节点树，然后将新节点树与当前节点树进行比较，这样就可以得到哪些节点的那些属性需要更新、那些节点需要添加或删除。最后将setData数据合并到data中，并用新节点树替换旧节点树，用于下一次重渲染。
    - 去掉不必要设置的数据、减少setData的数据量，有助于提升这一步骤的性能。

###### 小结
- 优化策略
    - 精简代码，降低WXML结构和JS代码的复杂性
    - 合理使用setData调用，减少setData次数和数据量
    - 必要时使用分包优化

##### 小程序基础库的更新迭代
###### 小程序基础库
- 启动小程序后，先载入基础库，接着再载入业务代码
- 小程序基础库不会被打包在某个小程序的代码包里边，它会被提前内置在微信客户端
    - 降低业务小程序的代码包大小
    - 可以单独修复基础库中的bug，无需修改到业务小程序的代码包。

- 可以通过wx.getSystemInfo()或者wx.getSystemInfoSync()方法获取小程序版本号。

###### 异常
- 捕捉JS异常的方法：
    - try，catch方案。可以针对某个代码块使用try，catch包装
        - 缺点：无法捕捉到全局丶错误事件
    - window.onerror方法。可以通过window.addEventListener("error",function(evt){})这个方法能捕捉到语法错误跟运行时错误，同时知道出错的信息，以及出错的文件，行号，列号等。

#### 配置小程序
- 全局配置:用来对微信小程序进行全局配置，决定页面文件的路径、窗口表现、设置网络超时时间、设置多 tab 等
    - [https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html](https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html)
- 页面配置:对本页面的窗口表现进行配置，页面中配置项会覆盖 app.json 的 window 中相同的配置项。
    - [https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/page.html](https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/page.html)
- sitemap配置:用来配置小程序及其页面是否允许被微信索引
    - [https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/sitemap.html](https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/sitemap.html) 
