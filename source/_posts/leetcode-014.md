---
title: LeetCode.014-Longest Common Prefix
date: 2019-08-08 15:44:39
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
	- [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/)
- Title
	- Longest Common Prefix
- Content 
	- Write a function to find the longest common prefix string amongst an array of strings.
	- If there is no common prefix, return an empty string "".
<!--more-->

###### Answer
- 思路
	- 暴力破解，直接遍历就好了
- 时间复杂度
	- O(n)
- 空间复杂度
	- O(1)
- 代码实现
	
	```Java
	public String longestCommonPrefix(String[] strs) {
        if (strs == null || strs.length == 0) {
            return "";
        }

        String longestPrefix = strs[0];

        for (int i = 1; i < strs.length; i++) {

            while (strs[i].indexOf(longestPrefix) != 0) {

                longestPrefix = longestPrefix.substring(0, longestPrefix.length() - 1);
            }

        }

        return longestPrefix;
    }
	```
- 提交结果
	- Runtime: 0 ms, faster than 100.00% of Java online submissions for Longest Common Prefix.
	- Memory Usage: 36.8 MB, less than 99.42% of Java online submissions for Longest Common Prefix.
