---
title: LeetCode.1115-Print FooBar Alternately
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2019-10-31 10:48:36
---
###### Question
- Source
	- [1115. Print FooBar Alternately](https://leetcode.com/problems/print-foobar-alternately/) 
- Title
	- 1115. Print FooBar Alternately 
- Content
	- The same instance of FooBar will be passed to two different threads. Thread A will call foo() while thread B will call bar(). Modify the given program to output "foobar" n times.
<!--more-->

###### Answer
- 思路
	- synchronized加锁
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	class FooBar {
    	private int n;

    	Lock lock = new ReentrantLock();
    	boolean printFooFlag = true;

    	public FooBar(int n) {
        this.n = n;
    	}

    	public void foo(Runnable printFoo) throws InterruptedException {

        	for (int i = 0; i < n; i++) {

            	synchronized (lock){
                	while (!printFooFlag) {
                    	lock.wait();
                	}

                	// printFoo.run() outputs "foo". Do not change or remove this line.
                	printFoo.run();
                	printFooFlag = false;
                	lock.notifyAll();
            	}

        	}
    	}

    	public void bar(Runnable printBar) throws InterruptedException {

        	for (int i = 0; i < n; i++) {

            	synchronized (lock){
                	while (printFooFlag) {
                    	lock.wait();
                	}
                	// printBar.run() outputs "bar". Do not change or remove this line.
                	printBar.run();
                	printFooFlag = true;
                	lock.notifyAll();
            	}

        	}
    	}
	}
	```
- 提交结果
	- Runtime: 16 ms, faster than 86.33% of Java online submissions for Print FooBar Alternately.
	- Memory Usage: 36.3 MB, less than 100.00% of Java online submissions for Print FooBar Alternately.
