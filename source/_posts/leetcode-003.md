---
title: LeetCode.003-Longest Substring Without Repeating Characters
date: 2019-06-17 17:59:05
tags:
- LeetCode
- Algorithm
- Java
- LeetCode-Medium
categories: LeetCode
visible: hide 
---
###### Question
- Source
	- [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) 
- Title
	- Longest Substring Without Repeating Characters
- Content
	- Given a string, find the length of the longest substring without repeating characters.

<!--more-->
###### Answer
- 思路
	- 滑动窗口，空间换时间
	- ASCII码只有128个，可以创建一个大小为128的数组，里面存放每个字符最后一次存在的位置，遍历字符串，在数组中找到当前字符上一次出现的位置，和当前位置的差值即可能为最长字符串长度。
- 时间复杂度
	- O(n) 
- 空间复杂度
	- O(1) 
- 代码实现

	```
	public int lengthOfLongestSubstring(String s) {
        int[] index = new int[128]; // 128
        int maxCount = 0;
        int start = 0;

        for (int end = 0; end < s.length(); end++) {
            start = Math.max(start, index[s.charAt(end)]);

            maxCount = Math.max(maxCount, end + 1 - start);

            index[s.charAt(end)] = end + 1;
        }

        return maxCount;
    }
	```
- 提交结果	
	- Runtime: 2 ms, faster than 99.85% of Java online submissions for Longest Substring Without Repeating Characters.
	- Memory Usage: 36.8 MB, less than 99.79% of Java online submissions for Longest Substring Without Repeating Characters. 	
