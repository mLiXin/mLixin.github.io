---
title: LeetCode.面试题21-调整数组顺序使奇数位于偶数前面
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Easy
categories:
  - LeetCode
date: 2020-04-08 10:25:49
---
###### Question
- Source
	- [面试题21. 调整数组顺序使奇数位于偶数前面]() 
- Title
	- 面试题21. 调整数组顺序使奇数位于偶数前面 
- Content
	- 输入一个整数数组，实现一个函数来调整该数组中数字的顺序，使得所有奇数位于数组的前半部分，所有偶数位于数组的后半部分。

<!--more-->

###### Answer
- 思路
	- 左右指针，找到数组左边偶数和右边奇数swap
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int[] exchange(int[] nums) {
        int left = 0;
        int right = nums.length-1;
        int temp = 0;
        while(left < right){
            while(left < right && ((nums[left] & 1) == 1)){
                left++;
            }
            while(left < right && ((nums[right] & 1) == 0)){
                right--;
            }
            if(left < right){
                temp = nums[left];
                nums[left] = nums[right];
                nums[right] = temp;
            }
        }
        return nums;
    }
	```
- 提交结果
	- 执行用时 :2 ms, 在所有 Java 提交中击败了99.98%的用户
	- 内存消耗 :47.9 MB, 在所有 Java 提交中击败了100.00%的用户
