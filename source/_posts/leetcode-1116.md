---
title: LeetCode.1116-Print Zero Even Odd
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-xxx
categories:
  - LeetCode
date: 2019-11-22 10:43:52
---
###### Question
- Source
	- [Print Zero Even Odd](https://leetcode.com/problems/print-zero-even-odd/) 
- Title
	- 1116.Print Zero Even Odd 
- Content
	- Suppose you are given the following code:
	- class ZeroEvenOdd {
  public ZeroEvenOdd(int n) { ... }      // constructor
  public void zero(printNumber) { ... }  // only output 0's
  public void even(printNumber) { ... }  // only output even numbers
  public void odd(printNumber) { ... }   // only output odd numbers
}
The same instance of ZeroEvenOdd will be passed to three different threads:
	- Thread A will call zero() which should only output 0's.
Thread B will call even() which should only ouput even numbers.
Thread C will call odd() which should only output odd numbers.
Each of the threads is given a printNumber method to output an integer. Modify the given program to output the series 010203040506... where the length of the series must be 2n.
<!--more-->

###### Answer
- 思路
	- x 
- 时间复杂度
	- O(x) 	
- 代码实现
	- 方法一：wait/notify
		
		```Java
	class ZeroEvenOdd {
			private int n;
			private boolean isZero = true;
			private int current = 1;
			public ZeroEvenOdd(int n) {
				this.n = n;
			}
    		
    		// printNumber.accept(x) outputs "x", where x is an integer.
    		public void zero(IntConsumer printNumber) throws InterruptedException {
				for (int i = 0; i < n; i++) {
					synchronized (this) {
                		while (!isZero) {
                    		wait();
                		}
                		printNumber.accept(0);
                		isZero = false;
                		notifyAll();
            		}
        		}
    		}
    		public void even(IntConsumer printNumber) throws InterruptedException {
        		for (int i = 2; i <= n; i = i + 2) {
            		synchronized (this) {
                		while (isZero || (current % 2 != 0)) {
                    	wait();
                	}
                	printNumber.accept(current++);
                	isZero = true;
                	notifyAll();
            		}
        		}
    	}
    		public void odd(IntConsumer printNumber) throws InterruptedException {
        		for (int i = 1; i <= n; i = i + 2) {
            		synchronized (this) {
                		while (isZero || (current % 2 == 0)) {
                    	wait();
                		}

                	printNumber.accept(current++);
                	isZero = true;
                	notifyAll();
            		}
        		}
    		}
		}
		``` 	
	- 方法二：CountDownLatch
		
		```Java
		class ZeroEvenOdd {
    		private int n;
    		private int current = 1;
    		CountDownLatch zeroLatch = new CountDownLatch(0);
    		CountDownLatch evenLatch = new CountDownLatch(1);
    		CountDownLatch oddLatch = new CountDownLatch(1);
    		public ZeroEvenOdd(int n) {
        		this.n = n;
    		}
    		// printNumber.accept(x) outputs "x", where x is an integer.
    		public void zero(IntConsumer printNumber) throws InterruptedException {
        		for (int i = 0; i < n; i++) {
            		zeroLatch.await();
            		printNumber.accept(0);
            		zeroLatch = new CountDownLatch(1);
            		if (current % 2 == 0) {
                		evenLatch.countDown();
            		} else {
                		oddLatch.countDown();
            		}
        		}
    		}
    		public void even(IntConsumer printNumber) throws InterruptedException {
        		for (int i = 2; i <= n; i = i + 2) {
            		evenLatch.await();
            		printNumber.accept(current++);
            		evenLatch = new CountDownLatch(1);
            		zeroLatch.countDown();
        		}
    		}
    		public void odd(IntConsumer printNumber) throws InterruptedException {
        		for (int i = 1; i <= n; i = i + 2) {
            		oddLatch.await();
            		printNumber.accept(current++);
            		oddLatch = new CountDownLatch(1);
            		zeroLatch.countDown();
        		}
    		}
		}
		``` 	
	- 方法三：CyclicBarrier
		
		```Java
		``` 	
	- 方法四：Semaphore
		
		```Java
		``` 	
	- 方法五：管程模型(凡是可以用信号量解决的问题，都可以用管程模型来解决)
		
		```Java
		``` 	
	- 方法六：无锁编程(但凡用了锁的，都来试试可否变成无锁的)
		
		```Java
		``` 	
- 提交结果
	- xxx 
