---
title: Hexo配置相关
date: 2020-03-30 15:04:45
tags:
---
#### 多设备切换

#### 置顶
1. 安装库

	```
	npm uninstall hexo-generator-index --save
	npm install hexo-generator-index-pin-top --save
	```
2. 然后在需要置顶的文章中添加`top:true`
3. 设置置顶标志：在`/themes/next/layout/_macro`中找到`post.swig`，在`<div class="post-meta">`标签中添加如下代码：
	
	```
	{% if post.top %}
    	<i class="fa fa-thumb-tack"></i>
    	<font color="red">置顶</font>
    	<span class="post-meta-divider">|</span>
	{% endif %}
	```

