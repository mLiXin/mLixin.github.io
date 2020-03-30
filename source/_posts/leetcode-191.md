---
title: LeetCode.191-Number of 1 Bits
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories: LeetCode
visible: hide
date: 2019-09-24 14:48:45
---
###### Question
- Source
	- [191. Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) 
- Title
	- 191. Number of 1 Bits 
- Content
	- Write a function that takes an unsigned integer and return the number of '1' bits it has (also known as the Hamming weight).
<!--more-->

###### Answer
- 思路
	- >>> 无符号右移，每次只看最后一位是不是1，和1做与运算
- 时间复杂度
	- O(1)(这里应该只会循环32次)	
- 代码实现

	```Java
	public int hammingWeight(int n) {
        int count = 0;
        while (n != 0) {
            count = count + (n & 1);
            n = n >>> 1;
        }
        return count;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Number of 1 Bits.
	- Memory Usage: 33.2 MB, less than 5.41% of Java online submissions for Number of 1 Bits. 
