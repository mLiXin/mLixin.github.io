---
title: LeetCode.面试题42-连续子数组的最大和
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-13 13:44:19
---
###### Question
- Source
	- [面试题42. 连续子数组的最大和](https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/) 
- Title
	- 面试题42. 连续子数组的最大和 
- Content
	- 输入一个整型数组，数组里有正数也有负数。数组中的一个或连续多个整数组成一个子数组。求所有子数组的和的最大值。
	- 要求时间复杂度为O(n)。 
<!--more-->

###### Answer
- 思路
	- 动态规划，f(n) = f(n-1) + Math(nums[i],0);
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int maxSubArray(int[] nums) {
        int maxSum = nums[0];
        int sum = 0;
        for(int num: nums) {
            if(sum > 0) {
                sum += num;
            } else {
                sum = num;
            }
            maxSum = Math.max(maxSum, sum);
        }
        return maxSum;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了98.69%的用户
	- 内存消耗 :46.5 MB, 在所有 Java 提交中击败了100.00%的用户
