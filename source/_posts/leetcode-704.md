---
title: LeetCode.704-Binary Search
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2019-10-28 09:58:38
---
###### Question
- Source
	- [](https://leetcode.com/problems/binary-search/) 
- Title
	- 704. Binary Search
- Content
	- Given a sorted (in ascending order) integer array nums of n elements and a target value, write a function to search target in nums. If target exists, then return its index, otherwise return -1.
<!--more-->

###### Answer
- 思路
	- 普通的二分查找，注意临界条件 
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public int search(int[] nums, int target) {

        if (nums == null || nums.length ==0){
            return -1;
        }
        int left = 0;
        int right = nums.length - 1;

        int mid;
        while (left <= right) {
            mid = left + ((right - left) >> 1);

            if (nums[mid] < target) {
                left = mid + 1;
            } else if (nums[mid] > target) {
                right = mid - 1;
            } else {
                return mid;
            }
        }

        return -1;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Binary Search.
	- Memory Usage: 39.1 MB, less than 100.00% of Java online submissions for Binary Search.
