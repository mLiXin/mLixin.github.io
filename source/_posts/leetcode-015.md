---
title: LeetCode.015-3Sum
date: 2019-09-18 10:24:49
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
	- [15. 3Sum](https://leetcode.com/problems/3sum/) 
- Title
	- 15. 3Sum 
- Content
	- Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.
<!--more-->

###### Answer
- 思路
	- 直接遍历循环，会超时。拿到第一个数之后，剩下的就是计算两个值的sum = 0-nums[first]，可以用左右指针，根据sum的大小来判断怎么移动左右指针，注意过滤重复情况
- 时间复杂度
	- O(n2) 	
- 代码实现

	```Java
	public List<List<Integer>> threeSum(int[] nums) {

        Arrays.sort(nums);

        List<List<Integer>> result = new ArrayList<>();
        
        for(int i = 0 ; i < nums.length -2;i++){
            if(nums[i]>0){
                break;
            }
            
            if(i >0 && nums[i] == nums[i-1]){
                continue;
            }
            
            int leftPos = i +1;
            int rightPos = nums.length-1;
            
            while(leftPos < rightPos){
                int currentSum = nums[i] + nums[leftPos]+nums[rightPos];
                if(currentSum > 0){
                    rightPos--;
                }else if(currentSum <0){
                    leftPos++;
                }else{
                    result.add(Arrays.asList(nums[i], nums[leftPos], nums[rightPos]));
                    while (leftPos < rightPos && nums[leftPos] == nums[leftPos + 1]) {
                        leftPos++;
                    }

                    while (leftPos < rightPos && nums[rightPos] == nums[rightPos - 1]) {
                        rightPos--;
                    }

                    leftPos++;
                    rightPos--;
                }
            }
        }
        
        return result;
    }
	```
- 提交结果
	- Runtime: 24 ms, faster than 99.30% of Java online submissions for 3Sum.
	- Memory Usage: 48.3 MB, less than 80.56% of Java online submissions for 3Sum. 
