---
title: LeetCode.088-Merge Sorted Array
date: 2019-09-18 10:01:19
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
	- [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) 
- Title
	- Merge Sorted Array 
- Content
	- Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
<!--more-->

###### Answer
- 思路
	- 从后往前比较
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public void merge(int[] nums1, int m, int[] nums2, int n) {
        int resultLength = m+n;
        int nums1Pos = m-1;
        int nums2Pos = n-1;
        for(int i = m+n-1;i>=0;i--){
            if(nums1Pos >=0 && nums2Pos >=0){
                if(nums1[nums1Pos] > nums2[nums2Pos]){
                    nums1[i] = nums1[nums1Pos];
                    nums1Pos --;
                }else{
                    nums1[i] = nums2[nums2Pos];
                    nums2Pos --;
                }  
            }else if(nums1Pos <0){
                nums1[i] = nums2[nums2Pos];
                nums2Pos --;
            }else{
                break;
            }
        }
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Merge Sorted Array.
	- Memory Usage: 36.2 MB, less than 100.00% of Java online submissions for Merge Sorted Array. 
