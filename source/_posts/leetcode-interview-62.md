---
title: LeetCode-面试题62.圆圈中最后剩下的数字
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-03-30 10:59:28
---
###### Question
- Source
	- [面试题62.圆圈中最后剩下的数字](https://leetcode-cn.com/problems/yuan-quan-zhong-zui-hou-sheng-xia-de-shu-zi-lcof/) 
- Title
	- 面试题62.圆圈中最后剩下的数字 
- Content
	- 0,1,,n-1这n个数字排成一个圆圈，从数字0开始，每次从这个圆圈里删除第m个数字。求出这个圆圈里剩下的最后一个数字。例如，0、1、2、3、4这5个数字组成一个圆圈，从数字0开始每次删除第3个数字，则删除的前4个数字依次是2、0、4、1，因此最后剩下的数字是3。
<!--more-->

###### Answer
- 思路
	- 约瑟夫环，可以模拟过程实现，属于暴力解决，肯定会超时的。这种的可以找到递推公式：f(n,m) = (f(n-1,m) + m)%n，且f(1,m) = 0，就可以递归实现了。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	   public int lastRemaining(int n, int m) {

        if (n == 1){
            return 0;
        }

        return (lastRemaining(n-1,m) + m) % n;
    }

	```
- 提交结果
	- 执行用时 :11 ms, 在所有 Java 提交中击败了51.76%的用户
	- 内存消耗 :41.1 MB, 在所有 Java 提交中击败了100.00%的用户
