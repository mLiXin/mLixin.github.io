---
title: LeetCode.001-Two Sum
date: 2019-06-17 16:19:03
tags:
- LeetCode
- Algorithm
- Java
- LeetCode-Easy
categories: LeetCode
visible: hide
---
###### Question
- Source
	- [1.Two Sum](https://leetcode.com/problems/two-sum/)
- Title
	- Two Sum
- Content
	- Given an array of integers, return indices of the two numbers such that they add up to a specific target.You may assume that each input would have exactly one solution, and you may not use the same element twice.

<!--more-->
###### Answer
- 思路
	- 1. 暴力破解，嵌套循环即可，但是这样时间复杂度就是`O(n2)`
	- 2. 使用`HashMap`，遍历一次，将`nums[i]`和`i`放入`hashMap`中一一对应，这样在遍历到第二个整数的时候，就可以通过`target-nums[i]`是否是hashMap中存在的key来找到这两个整数。
- 时间复杂度
	- `O(n)`
- 空间复杂度
	- `O(n)`
- 代码实现

	```
	public int[] twoSum(int[] nums, int target) {

        Map<Integer, Integer> hashMap = new HashMap<>(nums.length);

        for (int i = 0; i < nums.length; i++) {

            if (hashMap.containsKey(target - nums[i])) {
                return new int[] { hashMap.get(target - nums[i]), i };
            }

            hashMap.put(nums[i], i);
        }

        return null;
    }
	```
- 提交结果
	- Runtime: 2 ms, faster than 98.84% of Java online submissions for Two Sum.
	- Memory Usage: 37.9 MB, less than 98.17% of Java online submissions for Two Sum.	
