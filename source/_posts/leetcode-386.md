---
title: LeetCode.386-Lexicographical Numbers
tags:
  - LeetCode
  - Algorithm
  - Java
  - LeetCode-Medium
categories:
  - LeetCode
date: 2019-11-26 14:59:48
---
###### Question
- Source
	- [386. Lexicographical Numbers](https://leetcode.com/problems/lexicographical-numbers/) 
- Title
	- 386. Lexicographical Numbers 
- Content
	- Given an integer n, return 1 - n in lexicographical order.
	- For example, given 13, return: [1,10,11,12,13,2,3,4,5,6,7,8,9].
	- Please optimize your algorithm to use less time and space. The input size may be as large as 5,000,000. 
<!--more-->

###### Answer
- 思路
	- 递归实现就可以了
- 时间复杂度
	- O(n) 	
- 代码实现

	```Java
	class Solution {
    	public List<Integer> lexicalOrder(int n) {
        	List<Integer> result = new ArrayList<>();
        	for (int i = 1; i < 10; i++) {
            	lexicalOrder(n, i, result);
        	}
        	return result;
    	}

    	public void lexicalOrder(int n, int pre, List<Integer> result) {
        	if (pre <= n) {
            	result.add(pre);

            	for (int i = 0; i < 10; i++) {

                	int next = pre * 10 + i;
                	if (next > n) {
                    	return;
                	}
                	lexicalOrder(n, next, result);
            	}
        	}
    	}
	}
	```
- 提交结果
	- Runtime: 2 ms, faster than 82.94% of Java online submissions for Lexicographical Numbers.
	- Memory Usage: 38.2 MB, less than 33.33% of Java online submissions for Lexicographical Numbers. 
