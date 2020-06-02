---
title: LeetCode.190-Reverse Bits
date: 2019-09-25 10:08:01
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
	- [190. Reverse Bits](https://leetcode.com/problems/reverse-bits/) 
- Title
	- 190. Reverse Bits 
- Content
	- Reverse bits of a given 32 bits unsigned integer. 
<!--more-->

###### Answer
- 思路
	- 从后往前遍历，计算result即可
- 时间复杂度
	- O(1) 	
- 代码实现

	```Java
	public int reverseBits(int n) {
        int result = 0;
        for(int i = 0;i<32;i++){
            result = result * 2 + (n & 1);
            n = n>>>1;
        }
        
        return result;
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 100.00% of Java online submissions for Reverse Bits.
	- Memory Usage: 30.4 MB, less than 7.32% of Java online submissions for Reverse Bits. 
