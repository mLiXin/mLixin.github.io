---
title: Android JsBridge的原理与实现
date: 2019-05-24 18:06:36
tags:
- Android
- Hybrid
- JsBridge
categories:
- Android
---
##### Native调用Js
- api19之前
	
	```
	public void loadUrl(String url)
	```
	
- api19及之后（效率更高）
	
	```
	/**
     * Compatibility note. Applications targeting {@link android.os.Build.VERSION_CODES#N} or
     * later, JavaScript state from an empty WebView is no longer persisted across navigations like
     * {@link #loadUrl(String)}. For example, global variables and functions defined before calling
     * {@link #loadUrl(String)} will not exist in the loaded page. Applications should use
     * {@link #addJavascriptInterface} instead to persist JavaScript objects across navigations.
     */
	public void evaluateJavascript(String script, ValueCallback<String> resultCallback)
	
	```
	不同于上面的`loadUrl`，执行完以后就结束了，这种方法可以在执行完以后立即拿到Js返回的结果，但是这个方法有兼容性的要求，所以在`minSDK<19`的app上，一般还是用的`loadUrl`。
	
<!--more-->
   
##### Js调用Native
- webview.addJavascriptInterface
	
	```
  /**
     * For applications targeted to API
     * level {@link android.os.Build.VERSION_CODES#JELLY_BEAN_MR1}
     * and above, only public methods that are annotated with
     * {@link android.webkit.JavascriptInterface} can be accessed from JavaScript.
     * For applications targeted to API level {@link android.os.Build.VERSION_CODES#JELLY_BEAN} or below,
     * all public methods (including the inherited ones) can be accessed, see the
     * important security note below for implications.
     */
     public void addJavascriptInterface(Object object, String name)
     
	```
	Native通过这个api可以提供Js可以执行的本地方法，但是在`api<=16`即`Android 4.1`及以前的版本中，这个方法会有远程执行安全漏洞，Js可以通过Java的反射等机制调用Native中的任何方法。不过在`Android 4.2`及以后这个漏洞修复了，只有添加了` @JavascriptInterface`注解的方法才能被Js调用。
	
- URL劫持 --- webviewClient.shouldOverrideUrlLoading
	
	```
	public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request)
	```
	这个方法是`webview`拦截`url`的一种回调，当`webview`发生`url`跳转的时候会触发该回调。通常情况下，web端采用加载不可见​`iframe​`的方式传递​`url​`到`​Native`，`Native`通过获取约定好的`scheme`来执行web端需要的操作。
	但是这种方法有一个比较严重的问题是，无法在短时间内回调多次​`shouldOverrideUrlLoading`​方法，也就是说频繁交互的情况下，会有较大概率多次`​url​`跳转只回调一次该方法。
	
- 方法劫持
	- Js -- alert `VS` Native -- webChromeClient.onJsAlert
	- Js -- prompt `VS` Native -- webChromeClient.onJsPrompt
	- Js -- confirm `VS` Native -- webChromeClient.onJsConfirm
	- Js -- console.log `VS` Native -- webChromeClient.onConsoleMessage

##### 常用第三方库及底层实现方式	
- [lzyzsd/JsBridge](https://github.com/lzyzsd/JsBridge)
	- 实现方式:
		- URL劫持
		
			```
			// BridgeWebView中
    private void init(){
        ......
        this.setWebViewClient(generateBridgeWebViewClient());
    }
    
    protected BridgeWebViewClient generateBridgeWebViewClient(){
        return new BridgeWebViewClient (this);
    }
    
    // BridgeWebViewClient中    
    public boolean shouldOverrideUrlLoading(WebView view, String url){
        try {
            url = URLDecoder.decode(url, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        if (url.startsWith(BridgeUtil.YY_RETURN_DATA)) { // 如果是返回数据
            webView.handlerReturnData(url);
            return true;
        } else if (url.startsWith(BridgeUtil.YY_OVERRIDE_SCHEMA)) { //
            webView.flushMessageQueue();
            return true;
        } else {
            return this.onCustomShouldOverrideUrlLoading(url)?true:super.shouldOverrideUrlLoading(view, url);
        }
    }
			```
			
- [wendux/DSBridge-Android](https://github.com/wendux/DSBridge-Android)
	- 实现方式:
		- 4.2以下使用方法劫持，通过Js的prompt实现
		- 4.2及以上使用addJavascriptInterface
		
		```
		private void init(){
			......
			if (Build.VERSION.SDK_INT > Build.VERSION_CODES.JELLY_BEAN) {
            	super.addJavascriptInterface(innerJavascriptInterface, BRIDGE_NAME);
        	} else {
            	// add dsbridge tag in lower android version
            	settings.setUserAgentString(settings.getUserAgentString() + " _dsbridge");
        	}
		}
		
		......
		
		public boolean onJsPrompt(WebView view, String url, final String message,
                                  String defaultValue, final JsPromptResult result) {

            if (Build.VERSION.SDK_INT <= Build.VERSION_CODES.JELLY_BEAN) {
                String prefix = "_dsbridge=";
                if (message.startsWith(prefix)) {
                    result.confirm(innerJavascriptInterface.call(message.substring(prefix.length()), defaultValue));
                    return true;
                }
            }
            ......
       }
            
		```
