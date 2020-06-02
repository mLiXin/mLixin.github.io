---
title: LeetCode.034-Find First and Last Position of Element in Sorted Array
date: 2019-09-20 10:14:37
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
	- [34. Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) 
- Title
	- Find First and Last Position of Element in Sorted Array 
- Content
	- Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target value.Your algorithm's runtime complexity must be in the order of O(log n).If the target is not found in the array, return [-1, -1].
<!--more-->

###### Answer
- 思路
	- 二分查找，找到nums[mid] == target的时候，往前往后找第一个和最后一个值等于这个的target的下表。我这里是直接遍历的，其实也可以再次使用二分查找来找。
- 时间复杂度
	- O(logN) 	
- 代码实现

	```Java
	public int[] searchRange(int[] nums, int target) {
        
        int leftPos = 0;
        int rightPos = nums.length -1;
        int mid = leftPos + ((rightPos - leftPos) >>1);
        int firstPos = -1;
        int lastPos = -1;
        while(leftPos <= rightPos){
            if(nums[mid] < target){
                leftPos = mid + 1;
            }else if(nums[mid] > target){
                rightPos = mid - 1;
            }else { // nums[mid] == target
                firstPos = mid;
                lastPos = mid;
                while(firstPos > 0 && nums[firstPos-1] == target){
                    firstPos --;
                }
                
                while(lastPos < nums.length -1 && nums[lastPos +1] == target){
                    lastPos ++;
                }
                break;
            }
            mid = leftPos + ((rightPos - leftPos) >>1);
        }
        
        return new int[]{firstPos,lastPos};
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Find First and Last Position of Element in Sorted Array.
	- Memory Usage: 39.2 MB, less than 100.00% of Java online submissions for Find First and Last Position of Element in Sorted Array.
