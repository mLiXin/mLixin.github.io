---
title: LeetCode.026-Remove Duplicates from Sorted Array
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories: LeetCode
visible: hide
date: 2019-09-11 11:36:15
---
###### Question
- Source
	- [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) 
- Title
	- Remove Duplicates from Sorted Array
- Content
	- Given a sorted array nums, remove the duplicates in-place such that each element appear only once and return the new length.Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory. 
<!--more-->

###### Answer
- 思路
	- 加一个pre的变量，存储上一个未重复的数字 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int removeDuplicates(int[] nums) {
        if(nums == null || nums.length == 0){
            return 0;
        }
        int pre = nums[0];
        int result = 1;
        for(int i = 1;i<nums.length;i++){
            if(nums[i] != pre){
                nums[result++] = nums[i];
                pre = nums[i];
            }
        }
        return result;
    }
	```
- 提交结果
	- Runtime: 1 ms, faster than 96.89% of Java online submissions for Remove Duplicates from Sorted Array.
	- Memory Usage: 39.2 MB, less than 99.47% of Java online submissions for Remove Duplicates from Sorted Array.
