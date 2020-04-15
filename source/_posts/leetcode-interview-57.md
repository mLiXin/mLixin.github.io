---
title: LeetCode.面试题57-和为s的两个数字
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-15 10:37:15
---
###### Question
- Source
	- [面试题57. 和为s的两个数字](https://leetcode-cn.com/problems/he-wei-sde-liang-ge-shu-zi-lcof/) 
- Title
	- 面试题57. 和为s的两个数字 
- Content
	- 输入一个递增排序的数组和一个数字s，在数组中查找两个数，使得它们的和正好是s。如果有多对数字的和等于s，则输出任意一对即可。 
<!--more-->

###### Answer
- 思路
	- 数组是排序好的，给定左右指针，进行相加再和target比较即可 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int[] twoSum(int[] nums, int target) {
        int left =0;
        int right = nums.length -1;
        int currentSum = nums[left] + nums[right];

        while(left < right){
            currentSum = nums[left] + nums[right];
            if(currentSum < target){
                left++;
            }else if(currentSum > target){
                right--;
            }else{
                return new int[]{nums[left],nums[right]};
            }
        }
        return new int[]{-1,-1};
    }
	```
- 提交结果
	- 执行用时 :2 ms, 在所有 Java 提交中击败了99.00%的用户
	- 内存消耗 :57.2 MB, 在所有 Java 提交中击败了100.00%的用户
