---
title: LeetCode.070-Climbing Stairs
date: 2019-09-17 10:12:20
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
	- [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) 
- Title
	- Climbing Stairs 
- Content
	- You are climbing a stair case. It takes n steps to reach to the top.Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
<!--more-->

###### Answer
- 思路
	- 可以用递归实现：f(n) = f(n-1)+f(n-2)，其中f(0)=1;f(1) = 1;
	- 也可以用数组循环实现,steps[n] = steps[n-1] = steps[n-2]
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	public int climbStairs(int n) {
        
        if(n==1){
            return 1;
        }
        
        int[] steps = new int[n+1];
        steps[0] = 1;
        steps[1] = 1;
        
        for(int i = 2;i<steps.length;i++){
            steps[i] = steps[i-1]+steps[i-2];
        }
        
        return steps[n];
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Climbing Stairs.
	- Memory Usage: 32.9 MB, less than 5.26% of Java online submissions for Climbing Stairs.
