---
title: LeetCode.179-Largest Number
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
  - TODO
categories: LeetCode
visible: hide
date: 2019-09-26 11:04:37
---
###### Question
- Source
	- [179. Largest Number](https://leetcode.com/problems/largest-number/) 
- Title
	- 179. Largest Number 
- Content
	- Given a list of non negative integers, arrange them such that they form the largest number.
<!--more-->

###### Answer
- 思路
	- 快排实现，提交结果不太理想
	- 基数排序(undo)，感觉基数排序是最贴近最优解的
- 时间复杂度
	- O(nlogN) 	
- 代码实现

	```Java
	public String largestNumber(int[] nums) {

        if (nums == null || nums.length == 0) {
            return "";
        }

        quickSort(nums, 0, nums.length - 1);

        if (nums[0] == 0) {
            return "0";
        }
        StringBuilder builder = new StringBuilder();

        for (int i = 0; i < nums.length; i++) {
            builder.append(nums[i]);
        }

        return builder.toString();
    }

    public void quickSort(int[] nums, int start, int end) {
        if (start >= end) {
            return;
        }

        int mid = partition(nums, start, end);

        quickSort(nums, start, mid - 1);
        quickSort(nums, mid + 1, end);
    }

    public int partition(int[] nums, int start, int end) {
        int flag = nums[end];
        int i = start;

        for (int j = start; j < end; j++) {
            if (judge(nums[j], flag)) {
                int temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;

                i++;
            }
        }

        int temp = nums[i];
        nums[i] = nums[end];
        nums[end] = temp;

        return i;
    }

    public boolean judge(int j, int flag) {

        String jStr = String.valueOf(j);
        String flagStr = String.valueOf(flag);

        return (jStr + flagStr).compareTo((flagStr + jStr)) > 0;
    }
	```
- 提交结果
	- Runtime: 4 ms, faster than 92.64% of Java online submissions for Largest Number.
	- Memory Usage: 36.2 MB, less than 82.22% of Java online submissions for Largest Number.
