---
title: LeetCode.面试题39-数组中出现次数超过一半的数字
date: 2020-04-13 11:46:27
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
	- [面试题39. 数组中出现次数超过一半的数字](https://leetcode-cn.com/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/) 
- Title
	- 面试题39. 数组中出现次数超过一半的数字 
- Content
	- 数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。
	- 你可以假设数组是非空的，并且给定的数组总是存在多数元素。 
<!--more-->

###### Answer
- 思路
	- 摩尔投票法 
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int majorityElement(int[] nums) {
        int count = 0;
        int target = nums[0];
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != target) {
                count--;
            } else {
                count++;
            }

            if (count == 0 && i < nums.length - 1) {
                target = nums[i + 1];
            }
        }
        return target;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :43.1 MB, 在所有 Java 提交中击败了100.00%的用户
