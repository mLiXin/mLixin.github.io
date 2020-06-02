---
title: LeetCode.面试题53-II-0～n-1中缺失的数字
date: 2020-04-14 11:50:09
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
	- [面试题53 - II. 0～n-1中缺失的数字](https://leetcode-cn.com/problems/que-shi-de-shu-zi-lcof/) 
- Title
	- 面试题53 - II. 0～n-1中缺失的数字 
- Content
	- 一个长度为n-1的递增排序数组中的所有数字都是唯一的，并且每个数字都在范围0～n-1之内。在范围0～n-1内的n个数字中有且只有一个数字不在该数组中，请找出这个数字。
<!--more-->

###### Answer
- 思路
	- 数组从头开始遍历，如果下标i和nums[i]不相等，则i缺失
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int missingNumber(int[] nums) {
        if(nums == null || nums.length == 0){
            return 0;
        }
        for(int i = 0 ;i < nums.length;i++){
            if(i != nums[i]){
                return i;
            }
        }
        return nums[nums.length -1]+1;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :40.6 MB, 在所有 Java 提交中击败了100.00%的用户
