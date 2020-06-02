---
title: LeetCode.面试题10-II-青蛙跳台阶问题
date: 2020-03-31 10:44:05
tags:
- 数据结构与算法
- LeetCode
categories:
- 数据结构与算法
- LeetCode
visible: hide
---
###### Question
- Source
	- [面试题10- II. 青蛙跳台阶问题]() 
- Title
	- 面试题10- II. 青蛙跳台阶问题x 
- Content
	- 一只青蛙一次可以跳上1级台阶，也可以跳上2级台阶。求该青蛙跳上一个 n 级的台阶总共有多少种跳法。
	- 答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

<!--more-->

###### Answer
- 思路
	- f(0) = 1;f(1) = 1;f(n) = f(m-1) + f(n-2); 循环实现即可
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int numWays(int n) {
        if(n == 0 || n == 1){
            return 1;
        }

        int pre = 1;
        int prePre = 1;
        int currentTemp = 1;
        for(int i = 2;i<=n;i++){
            currentTemp = (pre + prePre) % 1000000007;
            prePre = pre;
            pre = currentTemp;
        }
        return pre;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :36.6 MB, 在所有 Java 提交中击败了100.00%的用户
