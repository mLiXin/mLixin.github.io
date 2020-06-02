---
title: LeetCode.面试03-数组中重复的数字
date: 2020-03-30 16:13:28
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
	- [面试题03.数组中重复的数字](https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/) 
- Title
	- 面试题03.数组中重复的数字 
- Content
	- 找出数组中重复的数字。在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

<!--more-->

###### Answer
- 思路
	- 数字范围在0~n-1之间，那就简单了，创建一个长度为n的布尔数组flagArray，从nums的第0个开始遍历，以nums[i]的值作为flagArray的下标，如果flagArray[nums[i]]为false，说明该数字之前没出现过，将其置为true；如果为true，说明之前存在过，可以直接返回该nums[i]
- 更优解思路
	- 原地置换，从前往后遍历，当前位置的值nums[i]和i不一致的时候，将num[i]放到位置nums[i]中，即i和nums[i]进行交换，直到i的位置上nums[i] == i。如果数组中有重复的数字，则必定有当前位置的值nums[i]和index=nums[i]的值相等，即nums[i] == nums[nums[i]]，说明该值是重复的，返回即可。
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	// 基础解
	public int findRepeatNumber(int[] nums) {
        if(nums == null || nums.length == 0){
            return -1;
        }
        boolean[] flagArray = new boolean[nums.length];
        for(int i = 0;i<nums.length;i++){
            if(flagArray[nums[i]]){
                return nums[i];
            }else{
                flagArray[nums[i]] = true;
            }
        }
        return -1;
    }
    
    // 更优解
    public int findRepeatNumber(int[] nums) {
        if(nums == null || nums.length == 0){
            return -1;
        }
        for(int i = 0;i<nums.length;i++){
            while(i != nums[i]){
                if(nums[i] == nums[nums[i]]){
                    return nums[i];
                }
                swap(nums,i,nums[i]);
            }
        }
        return -1;
    }

    public void swap(int[] array,int left,int right){
        int temp = array[left];
        array[left] = array[right];
        array[right] = temp;
    }
	```
- 提交结果
	- 执行用时 :1 ms, 在所有 Java 提交中击败了92.68%的用户
	- 内存消耗 :50.3 MB, 在所有 Java 提交中击败了100.00%的用户
