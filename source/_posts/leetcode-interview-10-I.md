---
title: LeetCode.面试题10-I-斐波那契数列
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-03-31 10:37:12
---
###### Question
- Source
	- [面试题10- I. 斐波那契数列](https://leetcode-cn.com/problems/fei-bo-na-qi-shu-lie-lcof/) 
- Title
	- 面试题10- I. 斐波那契数列 
- Content
	- 写一个函数，输入 n ，求斐波那契（Fibonacci）数列的第 n 项。斐波那契数列的定义如下：
		- F(0) = 0,   F(1) = 1
		- F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
	- 斐波那契数列由 0 和 1 开始，之后的斐波那契数就是由之前的两数相加而得出。
	- 答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

<!--more-->

###### Answer
- 思路
	- 递归实现，代码简单，但是一般会超时，重复计算了很多元素
	- 循环实现，设置pre = f(n-1),prePre = f(n-2),暂存这两个元素，循环遍历并更新即可。这里需要注意结果需要对1e9+7取模 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	// // 递归实现
    // public int fib(int n) {
    //     if(n == 0 || n == 1){
    //         return n;
    //     }
    //     return fib(n-1) + fib(n-2);
    // }

    // 循环实现
    public int fib(int n) {
        if(n == 0 || n == 1){
            return n;
        }

        int pre = 1;
        int prePre = 0;
        int currentTemp;
        for(int i = 2;i<=n;i++){
            currentTemp = (pre + prePre)%1000000007;
            prePre = pre;
            pre = currentTemp;
        }
        return pre;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :36.7 MB, 在所有 Java 提交中击败了100.00%的用户
