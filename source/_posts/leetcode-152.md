---
title: LeetCode.152-Maximum Product Subarray
date: 2019-10-14 14:38:50
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
	- [152. Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) 
- Title
	- 152. Maximum Product Subarray 
- Content
	- Given an integer array nums, find the contiguous subarray within an array (containing at least one number) which has the largest product.
<!--more-->

###### Answer
- 思路
	- 整数数组，整数相乘，一定大于原来的数，而且又是连续的子序列，则左乘一遍，右乘一遍，就可以获得结果。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int maxProduct(int[] nums) {

        if (nums == null || nums.length == 0) {
            return 0;
        }
        int max = Integer.MIN_VALUE;
        int currentMax = 1;

        for (int i = 0; i < nums.length; i++) {
            currentMax = currentMax * nums[i];

            max = Math.max(currentMax, max);

            if (currentMax == 0) {
                currentMax = 1;
            }
        }

        currentMax = 1;
        for (int i = nums.length - 1; i >= 0; i--) {
            currentMax = currentMax * nums[i];

            max = Math.max(currentMax, max);

            if (currentMax == 0) {
                currentMax = 1;
            }
        }

        return max;
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 98.69% of Java online submissions for Maximum Product Subarray.
	- Memory Usage: 36.9 MB, less than 100.00% of Java online submissions for Maximum Product Subarray. 
