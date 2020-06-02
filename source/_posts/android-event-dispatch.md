---
title: 伪代码看懂Android事件分发机制
date: 2019-07-29 17:29:31
tags:
- Android
categories:
- Android
- 内部机制
---
#### 分发事件伪代码
```Java
// 步骤1：调用dispatchTouchEvent（）
public boolean dispatchTouchEvent(MotionEvent ev) {

	boolean consume = false; //代表 是否会消费事件
    
	// 步骤2：判断是否拦截事件
	if (onInterceptTouchEvent(ev)) {
		// a. 若拦截，则将该事件交给当前View进行处理
		// 即调用onTouchEvent (）方法去处理点击事件
		consume = onTouchEvent (ev) ;

	} else {
      // b. 若不拦截，则将该事件传递到下层
      // 即 下层元素的dispatchTouchEvent（）就会被调用，重复上述过程
      // 直到点击事件被最终处理为止
      consume = child.dispatchTouchEvent (ev) ;
    }

    // 步骤3：最终返回通知 该事件是否被消费（接收 & 处理）
    return consume;

}

```
##### Activity的分发伪代码
```Java
public boolean dispatchTouchEvent(MotionEvent event){
	if(PhoneWindow.superDispatchTouchEvent(event)){
		// 这里的调用链是
		// PhoneWindow.superDispatchTouchEvent
		// ->> DecorView.superDispatchTouchEvent
		// ->> ViewGroup.dispatchTouchEvent
		return true;
	}
	return onTouchEvent(event);
}

public boolean onTouchEvent(MotionEvent event){
	if(点击位置在界面外){
		return true;
	}
	return false;
}
```
##### ViewGroup的分发伪代码
```Java
public boolean dispatchTouchEvent(MotionEvent event){
	boolean flag_事件已经消费掉 = false;
	boolean result = false;

	if(!onInterceptTouchEvent(event)){
		flag_事件已经消费掉 = 遍历子View并调用子View的dispatchTouchEvent();
	}

	if (!flag_事件已经消费掉){
		// super是View，所以是View的dispatchTouchEvent
		result = super.dispatchTouchEvent(event);
	}
	return result;
}

public boolean onInterceptTouchEvent(MotionEvent event){
	// 默认为false
	return false;
}

// 没有自己实现onTouchEvent，而是调用父类的onTouchEvent
public boolean onTouchEvent(MotionEvent event){
	return super.onTouchEvent(event);
}
```
##### View的分发伪代码
```Java
public boolean dispatchTouchEvent(MotionEvent event){
	if (设置了onTouchListener 
			&& 按钮可点击 
			&& OnTouchListener里面的onTouch方法返回值){
		return true;
	}
	return onTouchEvent(event);
}

public boolean onTouchEvent(MotionEvent event){

	if (按钮可以点击){
		// 在event = MotionEvent.ACTION_UP中
		performClick();
		return true;
	}
	return false;
}

public void performClick(){
	if (当前View设置了onClickListener){
		调用onClickListener.onClick()
		return true;
	}
	return false;
}
```

