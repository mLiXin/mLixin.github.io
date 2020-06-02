---
title: LeetCode.198-House Robber
date: 2019-09-24 10:41:40
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
	- [198. House Robber](https://leetcode.com/problems/house-robber/submissions/) 
- Title
	- 198. House Robber 
- Content
	- You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
	- Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.
<!--more-->

###### Answer
- 思路
	- 动态规划，方程式：f(n) = Math.max(f(n-2)+current,f(n-1));
	- 可以先用回溯法看看，找找规律，一般这种用回溯法肯定会超时，一定要找到规律，找出动态方程式或者状态转移表
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int rob(int[] nums) {

        if (nums == null || nums.length == 0) {
            return 0;
        }

        if (nums.length == 1) {
            return nums[0];
        }

        if (nums.length == 2) {
            return Math.max(nums[0], nums[1]);
        }

        int[] maxCounts = new int[nums.length];
        maxCounts[0] = nums[0];
        maxCounts[1] = Math.max(maxCounts[0], nums[1]);
        for (int i = 2; i < nums.length; i++) {
            int prePre = nums[i] + maxCounts[i - 2];
            int pre = maxCounts[i - 1];

            maxCounts[i] = Math.max(prePre, pre);
        }

        return maxCounts[maxCounts.length - 1];
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for House Robber.
	- Memory Usage: 33.9 MB, less than 100.00% of Java online submissions for House Robber.
