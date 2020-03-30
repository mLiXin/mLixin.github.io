---
title: LeetCode.041-First Missing Positive
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories: LeetCode
visible: hide
date: 2019-09-13 10:08:03
---
###### Question
- Source
	- [41. First Missing Positive](https://leetcode.com/problems/first-missing-positive/) 
- Title
	- First Missing Positive 
- Content
	- Given an unsorted integer array, find the smallest missing positive integer. 
<!--more-->

###### Answer
- 思路
	- 空间换时间，因为是求最小正整数，建一个nums.length+1大小的countArray，初始是0，遍历nums数组，以符合要求的nums[i]为下标初始化，最后遍历countArray就可以了。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int firstMissingPositive(int[] nums) {
        if(nums == null || nums.length == 0){
            return 1;
        }
         
         int[] countArray = new int[nums.length +1];
         for(int i=0;i<nums.length;i++){
             if(nums[i] > 0 && nums[i] < countArray.length){
                 countArray[nums[i]] = 1;
             }
         }
         int min = 1;
         for(;min<countArray.length;min++){
             if(countArray[min] == 0){
                 return min;
             }
         }
         return min;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for First Missing Positive.
	- Memory Usage: 34.8 MB, less than 100.00% of Java online submissions for First Missing Positive. 
