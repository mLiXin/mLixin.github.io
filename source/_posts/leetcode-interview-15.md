---
title: LeetCode.面试题15-二进制中1的个数
date: 2020-04-07 09:49:44
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
	- [面试题15. 二进制中1的个数](https://leetcode-cn.com/problems/er-jin-zhi-zhong-1de-ge-shu-lcof/submissions/) 
- Title
	- 面试题15. 二进制中1的个数 
- Content
	- 请实现一个函数，输入一个整数，输出该数二进制表示中 1 的个数。例如，把 9 表示成二进制是 1001，有 2 位是 1。因此，如果输入 9，则该函数输出 2。
<!--more-->

###### Answer
- 思路
	- 从后往前数，无符号右移即可。也可以使用n&(n-1)
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	// you need to treat n as an unsigned value
    public int hammingWeight(int n) {
        int count = 0;
        while(n != 0){
            if((n & 1) == 1){
                count ++;
            }
            n = n >>> 1;
        }
        return count;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了99.66%的用户
	- 内存消耗 :36.8 MB, 在所有 Java 提交中击败了100.00%的用户
