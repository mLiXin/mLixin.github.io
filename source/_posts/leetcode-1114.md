---
title: LeetCode.1114-Print in Order
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2019-10-31 10:18:57
---
###### Question
- Source
	- [1114. Print in Order]() 
- Title
	- 1114. Print in Order 
- Content
	- The same instance of Foo will be passed to three different threads. Thread A will call first(), thread B will call second(), and thread C will call third(). Design a mechanism and modify the program to ensure that second() is executed after first(), and third() is executed after second().
<!--more-->

###### Answer
- 思路
	- 解法一：直接使用volatile修饰变量，线程2中如果firstEnable为false，直接等待，为true的时候才执行run方法
	- 解法二：手动建立内存屏障(?)，线程2中如果firstEnable不为true，则进入wait并释放锁，直到线程1获取锁并执行run方法并将firstEnable置为true，然后notifyAll，这时候线程2会和线程3其中一个线程获取锁，同理直到线程2获取锁
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	// 解法一：volatile
	public class Foo {

    volatile boolean firstEnable = false;
    volatile boolean secondEnable = false;

    public Foo() {

    }

    public void first(Runnable printFirst) throws InterruptedException {

        // printFirst.run() outputs "first". Do not change or remove this line.
        printFirst.run();
        firstEnable = true;
    }

    public void second(Runnable printSecond) throws InterruptedException {

        // printSecond.run() outputs "second". Do not change or remove this line.

        while (!firstEnable) {

        }
        printSecond.run();
        secondEnable = true;

    }

    public void third(Runnable printThird) throws InterruptedException {

        // printThird.run() outputs "third". Do not change or remove this line.
        while (!secondEnable) {

        }

        printThird.run();
    	}
	}
	// 解法二：屏障
	class Foo {

    Lock lock = new ReentrantLock();
    boolean firstEnable = false;
    boolean secondEnable = false;

    public Foo() {

    }

    public void first(Runnable printFirst) throws InterruptedException {

        synchronized (lock) {
            printFirst.run();
            firstEnable = true;
            lock.notifyAll();
        }
        // printFirst.run() outputs "first". Do not change or remove this line.

    }

    public void second(Runnable printSecond) throws InterruptedException {

        // printSecond.run() outputs "second". Do not change or remove this line.
        synchronized (lock) {
            while (!firstEnable) {
                lock.wait();
            }

            printSecond.run();
            secondEnable = true;
            lock.notifyAll();
        }
    }

    public void third(Runnable printThird) throws InterruptedException {

        // printThird.run() outputs "third". Do not change or remove this line.
        synchronized (lock) {
            while (!secondEnable) {
                lock.wait();
            }
            printThird.run();
            lock.notifyAll();
        }

    	}
}
	```
- 提交结果
	- Runtime: 8 ms, faster than 98.48% of Java online submissions for Print in Order.
	- Memory Usage: 35.7 MB, less than 100.00% of Java online submissions for Print in Order.
