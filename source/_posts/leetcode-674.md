---
title: LeetCode.674-Longest Continuous Increasing Subsequence
date: 2019-10-12 10:41:58
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
	- [674. Longest Continuous Increasing Subsequence](https://leetcode.com/problems/longest-continuous-increasing-subsequence/) 
- Title
	- 674. Longest Continuous Increasing Subsequence 
- Content
	- Given an unsorted array of integers, find the length of longest continuous increasing subsequence (subarray).
<!--more-->

###### Answer
- 思路
	- 连续递增子序列，直接和后一个比较就可以了。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int findLengthOfLCIS(int[] nums) {

        if (nums == null || nums.length == 0) {
            return 0;
        }
        int maxCount = 1;
        int curCount = 1;

        for (int i = 0; i < nums.length - 1; i++) {
            if (nums[i] < nums[i + 1]) {
                curCount++;
            } else {
                curCount = 1;
            }

            maxCount = Math.max(maxCount, curCount);
        }

        return maxCount;
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 99.76% of Java online submissions for Longest Continuous Increasing Subsequence.
	- Memory Usage: 36.7 MB, less than 100.00% of Java online submissions for Longest Continuous Increasing Subsequence. 
