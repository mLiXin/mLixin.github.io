---
title: LeetCode.005-Longest Palindromic Substring
date: 2019-07-12 15:27:50
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
	- [5.Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring)
- Title
	- Longest Palindromic Substring
- Content
	- Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
<!--more-->

###### Answer
- 思路
	- Manacher算法
		- 将字符中间都添加一个标记符号，可以将奇、偶数两种情况的判断统一为一种
		- 利用数组存储当前字符最大回文半径
		- google之
- 时间复杂度
	- O(n) 
- 空间复杂度
	- O(n) 
- 代码实现

	```
	// Manacher
    public String longestPalindrome(String s) {
        StringBuilder afterStr = new StringBuilder();
        afterStr.append("#");
        for (int i = 0; i < s.length(); i++) {
            afterStr.append(s.charAt(i));
            afterStr.append("#");
        }

        int centerPos = -1;
        int right = -1;
        int[] radiusArray = new int[afterStr.length()];

        for (int i = 0; i < afterStr.length(); i++) {
            // init min radius
            int currentRadius = 1;
            if (i <= right) {
                currentRadius = Math.min(radiusArray[2 * centerPos - i], right - i);
            }
            // try longer radius
            while (i - currentRadius >= 0
                    && i + currentRadius < afterStr.length()
                    && afterStr.charAt(i - currentRadius) == afterStr.charAt(i + currentRadius)) {
                currentRadius++;
            }

            // update state
            if (i + currentRadius - 1 > right) {
                right = i + currentRadius - 1;
                centerPos = i;
            }

            radiusArray[i] = currentRadius;
        }

        int maxLength = 0;
        int cenPos = 0;
        for (int i = 0; i < radiusArray.length; i++) {
            if (maxLength < radiusArray[i]) {
                maxLength = radiusArray[i];
                cenPos = i;
            }
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < afterStr.length(); i++) {
            if (i > cenPos - maxLength && i < cenPos + maxLength && afterStr.charAt(i) != '#') {
                result.append(afterStr.charAt(i));
            }
        }

        return result.toString();
    }
	```
- 提交结果
	- Runtime: 5 ms, faster than 96.45% of Java online submissions for Longest Palindromic Substring.
	- Memory Usage: 36.2 MB, less than 99.98% of Java online submissions for Longest Palindromic Substring. 