---
title: LeetCode.016-3Sum Closest
date: 2019-09-18 10:57:04
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
	- [16. 3Sum Closest](https://leetcode.com/problems/3sum-closest/) 
- Title
	- 3Sum Closest 
- Content
	- Given an array nums of n integers and an integer target, find three integers in nums such that the sum is closest to target. Return the sum of the three integers. You may assume that each input would have exactly one solution.
<!--more-->

###### Answer
- 思路
	- 和015的思路一致，TODO，这里提交结果不太理想，应该还有优化的空间
- 时间复杂度
	- O(n2) 	
- 代码实现

	```Java
	public int threeSumClosest(int[] nums, int target) {
        Arrays.sort(nums);
        int result = nums[0]+nums[1]+nums[2];
        
        for(int i = 0;i<nums.length -1;i++){
            
            if(i >0 && nums[i] == nums[i-1]){
                continue;
            }
            
            int leftPos = i+1;
            int rightPos = nums.length -1;
            while(leftPos < rightPos){
                int currentSum = nums[i] + nums[leftPos] + nums[rightPos];
                
                if(currentSum == target){
                    return currentSum;
                }else if(currentSum < target){
                    if(Math.abs(currentSum - target) < Math.abs(result - target)){
                        result = currentSum;
                    }
                    leftPos++;
                }else if(currentSum > target){
                    if(Math.abs(currentSum - target) < Math.abs(result - target)){
                        result = currentSum;
                    }
                    rightPos--;
                }
            }
        }
        return result;
    }
	```
- 提交结果
	- Runtime: 5 ms, faster than 62.09% of Java online submissions for 3Sum Closest.
	- Memory Usage: 37.3 MB, less than 96.67% of Java online submissions for 3Sum Closest. 
