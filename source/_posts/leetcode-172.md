---
title: LeetCode.172-Factorial Trailing Zeroes
date: 2019-09-26 13:59:56
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
	- [172. Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) 
- Title
	- 172. Factorial Trailing Zeroes 
- Content
	- Given an integer n, return the number of trailing zeroes in n!.
<!--more-->

###### Answer
- 思路
	- 只有2 * 5 == 10，所以就是求1到n分解能得到多少个5 
- 时间复杂度
	- O(x) 	
- 代码实现

	```Java
	public int trailingZeroes(int n) {
        int res = 0;
        while(n > 0){
           res += n/5;
           n /= 5;
        }
        return res;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Factorial Trailing Zeroes.
	- Memory Usage: 33.3 MB, less than 7.69% of Java online submissions for Factorial Trailing Zeroes. 
