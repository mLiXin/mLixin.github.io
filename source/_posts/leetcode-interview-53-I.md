---
title: LeetCode.面试题53-I-在排序数组中查找数字 I
date: 2020-04-14 11:32:58
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
	- [面试题53 - I. 在排序数组中查找数字 I]() 
- Title
	- 面试题53 - I. 在排序数组中查找数字 I 
- Content
	- 统计一个数字在排序数组中出现的次数。 
<!--more-->

###### Answer
- 思路
	- 二分查找，找到第一个target位置，然后往后遍历计数即可。 
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public int search(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return 0;
        }

        int left = 0;
        int right = nums.length -1;
        int mid = 0;
        while(left <= right){
            mid = left + ((right - left) >> 1);
            if(nums[mid] < target){
                left = mid + 1;
            }else {
                right = mid -1;
            }
        }

        if(left >= nums.length || nums[left] != target){
            return 0;
        }
        int count = 0;
        while(left < nums.length && nums[left++] == target){
            count++;
        }
        
        return count;
    }
	```
- 提交结果
	- 执行用时 :0 ms, 在所有 Java 提交中击败了100.00%的用户
	- 内存消耗 :42.7 MB, 在所有 Java 提交中击败了100.00%的用户
