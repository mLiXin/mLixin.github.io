---
title: LeetCode.189-Rotate Array
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories: LeetCode
visible: hide
date: 2019-09-25 10:25:19
---
###### Question
- Source
	- [189. Rotate Array](https://leetcode.com/problems/rotate-array/) 
- Title
	- 189. Rotate Array 
- Content
	- Given an array, rotate the array to the right by k steps, where k is non-negative. 
<!--more-->

###### Answer
- 思路
	- 用临时数组存后面的部分，将数组前面部分后移，然后将临时数组补充到数组前面。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public void rotate(int[] nums, int k) {
        if(nums.length < k){
            k = k % nums.length;
        }
        
        int[] temp = new int[k];
        for(int i = 0 ; i < temp.length;i++){
            temp[i] = nums[nums.length - k + i];
        }
        
        for(int i = nums.length -1;i>=k;i--){
            nums[i] = nums[i-k];
        }
        
        for(int i = 0 ; i < temp.length;i++){
            nums[i] = temp[i];
        }
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Rotate Array.
	- Memory Usage: 37.2 MB, less than 100.00% of Java online submissions for Rotate Array.
